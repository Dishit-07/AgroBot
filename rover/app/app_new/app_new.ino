#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <ESP32Servo.h>
#include <HardwareSerial.h>
#include <MPU6050.h>
#include <TinyGPSPlus.h>
#include <WebServer.h>
#include <WiFi.h>
#include <Wire.h>
#include "SoilSensor.h"

// ======================== PIN MAP ============================
#define DHTPIN          27  // Moved from 4
#define DHTTYPE         DHT11
#define MQ135_PIN       34  // ADC input-only
#define LDR_DIGITAL_PIN 26
#define LDR_LEFT_PIN    36  // ADC1
#define LDR_RIGHT_PIN   39  // ADC1
#define SOLAR_DEADBAND  50

#define I2C_SDA 21
#define I2C_SCL 22

#define GPS_RX 23 // UART1
#define GPS_TX 5  // UART1

#define RS485_RX 16 // UART2
#define RS485_TX 17 // UART2
#define RS485_EN 4

#define SERVO_SOLAR_PIN 18
#define SERVO_ARM_PIN   19

#define IN1 32
#define IN2 33
#define IN3 25
#define IN4 14

#define BUZZER_PIN 13

// ======================== TIMING =============================
#define SENSOR_INTERVAL  500
#define AUTO_MOVE_TIME   3000
#define AUTO_TURN_TIME   1000
#define BUZZER_BEEP_MS   200
#define MAX_SAMPLES      50
#define SOLAR_INTERVAL   150

#define TILT_THRESHOLD   35.0
#define TEMP_HIGH        40.0
#define GAS_ABNORMAL     2500
#define PRESSURE_HIST_SZ 5

#define SERVO_STEP_MS    15     // 8ms provides smooth fast easing without power brownouts
#define PROBE_INSERT_ANGLE    0
#define PROBE_RETRACT_ANGLE   180
#define SENSOR_STABILIZE_MS   4000

// ======================== OBJECTS =============================
WebServer server(80);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;
MPU6050 mpu;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);
HardwareSerial RS485Serial(2);
Servo solarServo;
Servo armServo;

const char *staSSID = "AGRO-BOT"; // <--- CHANGE THIS
const char *staPASS = "agro12345"; // <--- CHANGE THIS

bool debugModbus = true;

// ======================== STATE ==============================
float sTemp = 0, sHum = 0, sPressure = 0;
int   sGas  = 0;
bool  sIsDay = true;
bool  bmpOk  = false;

float mpuPitch = 0, mpuRoll = 0, mpuYaw = 0;

int    gpsSat = 0;
double gpsLat = 0, gpsLng = 0, gpsAlt = 0;
char   gpsTime[28] = "N/A";

int solarAngleCur = 90, solarAngleTgt = 90;
int armAngleCur   = PROBE_RETRACT_ANGLE, armAngleTgt   = PROBE_RETRACT_ANGLE;
unsigned long lastServoStepMs = 0;

bool buzzerOn = false;

// ======================== PRECISION AG ==================
float pressHist[PRESSURE_HIST_SZ] = {0};
int   pressHistIdx  = 0;
bool  pressHistFull  = false;

bool  alertActive    = false;
char  alertMsg[64]   = "";
bool  unsafeTerrain  = false;
String samplePriority = "NORMAL";

bool solarAutoTrack = false;
int  solarLdrLeft   = 0;
int  solarLdrRight  = 0;
unsigned long lastSolarMs = 0;
unsigned long lastSensorMs = 0;

SoilData currentSoilData;

// ======================== AUTOMATION =========================
enum AutoState {
  AUTO_IDLE,
  AUTO_MOVE_FORWARD,
  AUTO_STOP_SAMPLE,
  AUTO_INSERTING_PROBE,
  AUTO_STABILIZING,
  AUTO_READING_SENSOR,
  AUTO_RETRACTING_PROBE,
  AUTO_BUZZER_BEEP,
  AUTO_BUZZER_OFF,
  AUTO_TURN,
  AUTO_DONE
};

AutoState autoState  = AUTO_IDLE;
unsigned long autoTimer = 0;
int gridRows = 0, gridCols = 0;
int curRow   = 0, curCol  = 0;
bool serpentineFwd = true;

// ======================== SAMPLE STORAGE =====================
struct SoilSample {
  int    row, col;
  float  moisture;
  float  soilTemp;
  float  ph;
  int    n, p, k;
  float  ambientTemp;
  float  ambientHum;
  double lat, lng;
  unsigned long timestamp;
  bool   gpsValid;
};

SoilSample samples[MAX_SAMPLES];
int sampleCount = 0;

// ============================================================
// LOGIC FUNCTIONS
// ============================================================
String irrigationDecision() {
  if (!currentSoilData.valid) return "UNKNOWN";
  if (currentSoilData.moisture < 30 && sTemp > 30) return "HIGH";
  if (currentSoilData.moisture < 30) return "HIGH";
  if (currentSoilData.moisture < 60) return "MEDIUM";
  return "LOW";
}

int soilHealthScore() {
  if (!currentSoilData.valid) return 0;
  int score = 0;
  // Moisture (0-30 pts): optimal 40-70%
  if (currentSoilData.moisture >= 40 && currentSoilData.moisture <= 70) score += 30;
  else if (currentSoilData.moisture >= 25 && currentSoilData.moisture <= 85) score += 20;
  else if (currentSoilData.moisture >= 10) score += 10;
  
  // pH (0-30 pts): optimal 6.0-7.5
  if (currentSoilData.ph >= 6.0 && currentSoilData.ph <= 7.5) score += 30;
  else if (currentSoilData.ph >= 5.5 && currentSoilData.ph <= 8.0) score += 20;
  else if (currentSoilData.ph >= 4.5 && currentSoilData.ph <= 8.5) score += 10;

  // NPK basic presence (0-20 pts)
  int totalNutrients = currentSoilData.nitrogen + currentSoilData.phosphorus + currentSoilData.potassium;
  if (totalNutrients > 150) score += 20;
  else if (totalNutrients > 80) score += 15;
  else if (totalNutrients > 30) score += 5;

  // Air quality (0-20 pts)
  if (sGas < 800) score += 20;
  else if (sGas < 1500) score += 14;
  else if (sGas < 2500) score += 7;

  return constrain(score, 0, 100);
}

void updatePressureHistory() {
  if (!bmpOk || sPressure < 1) return;
  pressHist[pressHistIdx] = sPressure;
  pressHistIdx = (pressHistIdx + 1) % PRESSURE_HIST_SZ;
  if (pressHistIdx == 0) pressHistFull = true;
}

String weatherPrediction() {
  if (!pressHistFull) return "Collecting Data";
  int oldest = (pressHistIdx) % PRESSURE_HIST_SZ;
  float diff = pressHist[(pressHistIdx - 1 + PRESSURE_HIST_SZ) % PRESSURE_HIST_SZ] - pressHist[oldest];
  if (diff < -1.5f) return "Rain Likely";
  if (diff < -0.5f) return "Possible Change";
  return "Stable Weather";
}

bool checkFieldAlerts() {
  alertActive = false;
  alertMsg[0] = '\0';
  if (currentSoilData.valid && currentSoilData.moisture < 15) {
    alertActive = true;
    strncpy(alertMsg, "Low Moisture Detected", sizeof(alertMsg));
  } else if (sTemp > TEMP_HIGH) {
    alertActive = true;
    strncpy(alertMsg, "High Temperature Alert", sizeof(alertMsg));
  } else if (sGas > GAS_ABNORMAL) {
    alertActive = true;
    strncpy(alertMsg, "Abnormal Gas Level", sizeof(alertMsg));
  } else if (abs(mpuPitch) > TILT_THRESHOLD || abs(mpuRoll) > TILT_THRESHOLD) {
    alertActive = true;
    strncpy(alertMsg, "Dangerous Tilt Detected", sizeof(alertMsg));
  }
  return alertActive;
}

bool checkTerrainSafety() {
  if (abs(mpuPitch) > TILT_THRESHOLD || abs(mpuRoll) > TILT_THRESHOLD) {
    unsafeTerrain = true;
    digitalWrite(IN1,LOW); digitalWrite(IN2,LOW); digitalWrite(IN3,LOW); digitalWrite(IN4,LOW);
    return false;
  }
  unsafeTerrain = false;
  return true;
}

String calcSamplePriority() {
  if (!currentSoilData.valid) return "NORMAL";
  if (currentSoilData.moisture < 20 || sTemp > 38 || sGas > GAS_ABNORMAL) return "HIGH";
  return "NORMAL";
}

String cropRecommendation() {
  if (!currentSoilData.valid) return "Unknown";
  float m = currentSoilData.moisture;
  float p = currentSoilData.ph;
  if (m >= 65 && p >= 5.5 && p <= 7.0 && sTemp >= 22) return "Rice";
  if (m >= 50 && p >= 6.0 && p <= 7.5 && sTemp >= 15) return "Wheat";
  if (m >= 45 && p >= 5.8 && p <= 7.0 && sTemp >= 20) return "Maize";
  if (m >= 40 && p >= 5.0 && p <= 6.5 && sTemp >= 12) return "Potato";
  if (m >= 55 && p >= 6.0 && p <= 7.5 && sTemp >= 25) return "Sugarcane";
  if (m >= 30) return "Millet";
  return "Drought-Resistant";
}

void sendCORS(int code, const char *type, const String &body) {
  server.sendHeader("Access-Control-Allow-Origin",  "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "*");
  server.sendHeader("Access-Control-Allow-Private-Network", "true");
  server.send(code, type, body);
}
void handleOptions() {
  sendCORS(204, "text/plain", "");
}

// ============================================================
// MOTOR CONTROL
// ============================================================
void stopMotors()    { digitalWrite(IN1,LOW);  digitalWrite(IN2,LOW);  digitalWrite(IN3,LOW);  digitalWrite(IN4,LOW);  }
void moveForward()   { digitalWrite(IN1,LOW);  digitalWrite(IN2,HIGH); digitalWrite(IN3,HIGH); digitalWrite(IN4,LOW);  }
void moveBackward()  { digitalWrite(IN1,HIGH); digitalWrite(IN2,LOW);  digitalWrite(IN3,LOW);  digitalWrite(IN4,HIGH); }
void turnLeft()      { digitalWrite(IN1,HIGH); digitalWrite(IN2,LOW);  digitalWrite(IN3,HIGH); digitalWrite(IN4,LOW);  }
void turnRight()     { digitalWrite(IN1,LOW);  digitalWrite(IN2,HIGH); digitalWrite(IN3,LOW);  digitalWrite(IN4,HIGH); }

// ============================================================
// SENSOR READING
// ============================================================
void readSensors() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  
  if (!isnan(t)) sTemp = t;
  if (!isnan(h)) sHum  = h;
  if (bmpOk)     sPressure = bmp.readPressure() / 100.0f;
  sGas   = analogRead(MQ135_PIN);
  sIsDay = (digitalRead(LDR_DIGITAL_PIN) == LOW);
}

void readMPU() {
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  float accX = ax / 16384.0f, accY = ay / 16384.0f, accZ = az / 16384.0f;
  mpuPitch = atan2(-accX, sqrt(accY*accY + accZ*accZ)) * RAD_TO_DEG;
  mpuRoll  = atan2(accY, accZ) * RAD_TO_DEG;
  mpuYaw   = atan2(accX, accY) * RAD_TO_DEG;
}

void updateGpsCache() {
  gpsSat = gps.satellites.isValid() ? (int)gps.satellites.value() : 0;
  gpsLat = gps.location.isValid()   ? gps.location.lat()          : 0.0;
  gpsLng = gps.location.isValid()   ? gps.location.lng()          : 0.0;
  gpsAlt = gps.altitude.isValid()   ? gps.altitude.meters()       : 0.0;
  if (gps.date.isValid() && gps.time.isValid()) {
    snprintf(gpsTime, sizeof(gpsTime), "%04d-%02d-%02d %02d:%02d:%02d UTC",
             gps.date.year(), gps.date.month(), gps.date.day(),
             gps.time.hour(), gps.time.minute(), gps.time.second());
  }
}

// ============================================================
// SERVO EASING
// ============================================================
void servoEasingTick() {
  unsigned long now = millis();
  if (now - lastServoStepMs < SERVO_STEP_MS) return;
  lastServoStepMs = now;

  if (!solarAutoTrack) {
    if (solarAngleCur < solarAngleTgt) { solarAngleCur++; solarServo.write(solarAngleCur); } 
    else if (solarAngleCur > solarAngleTgt) { solarAngleCur--; solarServo.write(solarAngleCur); }
  }

  // Arm servo eases to prevent power brownouts
  if (autoState == AUTO_IDLE || autoState == AUTO_DONE) {
    if (armAngleCur < armAngleTgt) { armAngleCur++; armServo.write(armAngleCur); } 
    else if (armAngleCur > armAngleTgt) { armAngleCur--; armServo.write(armAngleCur); }
  }
}

// ============================================================
// BUILD JSON
// ============================================================
String buildJSON() {
  samplePriority = calcSamplePriority();
  String j = "{";
  j += "\"sat\":"    + String(gpsSat);
  j += ",\"lat\":"   + String(gpsLat, 6);
  j += ",\"lng\":"   + String(gpsLng, 6);
  j += ",\"alt\":"   + String(gpsAlt, 1);
  j += ",\"time\":\"" + String(gpsTime) + "\"";
  j += ",\"roll\":"  + String(mpuRoll,  1);
  j += ",\"pitch\":" + String(mpuPitch, 1);
  j += ",\"yaw\":"   + String(mpuYaw,   1);
  j += ",\"temp\":"  + String(sTemp,    1);
  j += ",\"hum\":"   + String(sHum,     1);
  j += ",\"gas\":"   + String(sGas);
  j += ",\"press\":" + String(sPressure,  1);
  j += ",\"day\":"   + String(sIsDay ? "true" : "false");
  
  // SN-3002 Fields
  if (currentSoilData.valid) {
      j += ",\"soilMoisture\":" + String(currentSoilData.moisture, 1);
      j += ",\"soilTemp\":" + String(currentSoilData.soilTemp, 1);
      j += ",\"ph\":" + String(currentSoilData.ph, 1);
      j += ",\"nitrogen\":" + String(currentSoilData.nitrogen);
      j += ",\"phosphorus\":" + String(currentSoilData.phosphorus);
      j += ",\"potassium\":" + String(currentSoilData.potassium);
  } else {
      j += ",\"soilMoisture\":0,\"soilTemp\":0,\"ph\":0,\"nitrogen\":0,\"phosphorus\":0,\"potassium\":0";
  }
  j += ",\"sensorStatus\":\"" + currentSoilData.status + "\"";
  j += ",\"lastSensorRead\":" + String(currentSoilData.timestamp);
  j += ",\"probeState\":\"" + String((armAngleCur == PROBE_INSERT_ANGLE) ? "INSERTED" : ((armAngleCur == PROBE_RETRACT_ANGLE) ? "RETRACTED" : "MOVING")) + "\"";
  j += ",\"probeCommandedAngle\":" + String(armAngleTgt);
  j += ",\"probeCurrentAngle\":" + String(armAngleCur);
  j += ",\"physicalFeedback\":false";
  j += ",\"sensorQuality\":\"" + String((currentSoilData.status == "VALID") ? "HIGH_VALID" : ((currentSoilData.status == "TIMEOUT") ? "TIMEOUT" : "DEGRADED")) + "\"";
  j += ",\"sensorStabilized\":" + String((autoState == AUTO_READING_SENSOR || (autoState == AUTO_IDLE && currentSoilData.valid)) ? "true" : "false");

  j += ",\"solarAngle\":" + String(solarAngleCur);
  j += ",\"solarAuto\":"  + String(solarAutoTrack ? "true" : "false");
  j += ",\"ldrL\":"       + String(solarLdrLeft);
  j += ",\"ldrR\":"       + String(solarLdrRight);
  j += ",\"armAngle\":"   + String(armAngleCur);
  j += ",\"buzzer\":"     + String(buzzerOn ? "true" : "false");
  
  bool autoRunning = (autoState != AUTO_IDLE && autoState != AUTO_DONE);
  j += ",\"auto\":"    + String(autoRunning ? "true" : "false");
  j += ",\"aRow\":"   + String(curRow);
  j += ",\"aCol\":"   + String(curCol);
  j += ",\"aTotalR\":" + String(gridRows);
  j += ",\"aTotalC\":" + String(gridCols);
  j += ",\"samples\":" + String(sampleCount);
  
  j += ",\"irrigation\":\"" + irrigationDecision() + "\"";
  j += ",\"health\":"      + String(soilHealthScore());
  j += ",\"weather\":\""    + weatherPrediction() + "\"";
  j += ",\"alert\":"       + String(alertActive ? "true" : "false");
  j += ",\"alertMessage\":\"" + String(alertMsg) + "\"";
  j += ",\"unsafeTerrain\":" + String(unsafeTerrain ? "true" : "false");
  j += ",\"samplePriority\":\"" + samplePriority + "\"";
  j += ",\"crop\":\""       + cropRecommendation() + "\"";
  j += "}";
  return j;
}

// ============================================================
// AUTOMATION STATE MACHINE
// ============================================================
void autoTick() {
  unsigned long now = millis();

  switch (autoState) {

  case AUTO_MOVE_FORWARD:
    if (now - autoTimer >= AUTO_MOVE_TIME) {
      stopMotors();
      autoState = AUTO_STOP_SAMPLE;
      autoTimer = now;
    }
    break;

  case AUTO_STOP_SAMPLE: {
    armAngleTgt  = PROBE_INSERT_ANGLE;
    autoState    = AUTO_INSERTING_PROBE;
    autoTimer    = now;
    break;
  }

  case AUTO_INSERTING_PROBE:
    if (now - autoTimer >= SERVO_STEP_MS) {
        autoTimer = now;
        if (armAngleCur > armAngleTgt) armAngleCur--;
        else if (armAngleCur < armAngleTgt) armAngleCur++;
        armServo.write(armAngleCur);
        
        if (armAngleCur == armAngleTgt) {
            autoState = AUTO_STABILIZING;
            autoTimer = now;
        }
    }
    break;

  case AUTO_STABILIZING:
    if (now - autoTimer >= SENSOR_STABILIZE_MS) {
        autoState = AUTO_READING_SENSOR;
    }
    break;

  case AUTO_READING_SENSOR:
    readSoilSensor(currentSoilData);
    if (currentSoilData.valid && sampleCount < MAX_SAMPLES) {
        SoilSample &s = samples[sampleCount++];
        s.row      = curRow;
        s.col      = curCol;
        s.moisture = currentSoilData.moisture;
        s.soilTemp = currentSoilData.soilTemp;
        s.ph       = currentSoilData.ph;
        s.n        = currentSoilData.nitrogen;
        s.p        = currentSoilData.phosphorus;
        s.k        = currentSoilData.potassium;
        s.ambientTemp = sTemp;
        s.ambientHum  = sHum;
        s.lat      = gpsLat;
        s.lng      = gpsLng;
        s.timestamp = now;
        s.gpsValid  = (gpsLat != 0 || gpsLng != 0);
    }
    armAngleTgt = PROBE_RETRACT_ANGLE;
    autoState = AUTO_RETRACTING_PROBE;
    autoTimer = now;
    break;

  case AUTO_RETRACTING_PROBE:
    if (now - autoTimer >= SERVO_STEP_MS) {
        autoTimer = now;
        if (armAngleCur > armAngleTgt) armAngleCur--;
        else if (armAngleCur < armAngleTgt) armAngleCur++;
        armServo.write(armAngleCur);
        
        if (armAngleCur == armAngleTgt) {
            autoState = AUTO_BUZZER_BEEP;
            buzzerOn = true;
            digitalWrite(BUZZER_PIN, HIGH);
            autoTimer = now;
        }
    }
    break;

  case AUTO_BUZZER_BEEP:
    if (now - autoTimer >= BUZZER_BEEP_MS) {
      buzzerOn = false;
      digitalWrite(BUZZER_PIN, LOW);
      autoState = AUTO_BUZZER_OFF;
      autoTimer = now;
    }
    break;

  case AUTO_BUZZER_OFF:
    if (now - autoTimer >= BUZZER_BEEP_MS) {
      if (serpentineFwd) {
        if (curCol < gridCols - 1) { curCol++; moveForward(); autoState = AUTO_MOVE_FORWARD; autoTimer = now; }
        else { if (curRow < gridRows - 1) { turnRight(); autoState = AUTO_TURN; autoTimer = now; } else { autoState = AUTO_DONE; } }
      } else {
        if (curCol > 0) { curCol--; moveForward(); autoState = AUTO_MOVE_FORWARD; autoTimer = now; }
        else { if (curRow < gridRows - 1) { turnLeft(); autoState = AUTO_TURN; autoTimer = now; } else { autoState = AUTO_DONE; } }
      }
    }
    break;

  case AUTO_TURN:
    if (now - autoTimer >= AUTO_TURN_TIME) {
      stopMotors();
      curRow++;
      serpentineFwd = !serpentineFwd;
      autoState = AUTO_STOP_SAMPLE;
      autoTimer = now;
    }
    break;

  default:
    break;
  }
}

// ============================================================
// WEB HANDLERS
// ============================================================
void handleRoot() {
  sendCORS(200, "text/plain", "AgroBot v5.0 API Server\nDashboard should be loaded separately.");
}

void handleData() {
  sendCORS(200, "application/json", buildJSON());
}

void handleSoilApi() {
  String j = "{";
  if (currentSoilData.valid) {
      j += "\"status\":\"valid\",";
      j += "\"moisture\":" + String(currentSoilData.moisture, 1) + ",";
      j += "\"temperature\":" + String(currentSoilData.soilTemp, 1) + ",";
      j += "\"ph\":" + String(currentSoilData.ph, 1) + ",";
      j += "\"nitrogen\":" + String(currentSoilData.nitrogen) + ",";
      j += "\"phosphorus\":" + String(currentSoilData.phosphorus) + ",";
      j += "\"potassium\":" + String(currentSoilData.potassium) + ",";
      j += "\"timestamp\":" + String(currentSoilData.timestamp);
  } else {
      j += "\"status\":\"" + currentSoilData.status + "\"";
  }
  j += "}";
  sendCORS(200, "application/json", j);
}

void handleControl() {
  if (server.hasArg("move")) {
    String dir = server.arg("move");
    if (!unsafeTerrain || dir == "stop") {
      if (dir == "forward")  moveForward();
      if (dir == "backward") moveBackward();
      if (dir == "left")     turnLeft();
      if (dir == "right")    turnRight();
      if (dir == "stop")     stopMotors();
    }
  }
  sendCORS(200, "text/plain", "OK");
}

void handleServo() {
  if (server.hasArg("solar")) { solarAngleTgt = constrain(server.arg("solar").toInt(), 0, 180); solarAutoTrack = false; }
  if (server.hasArg("arm"))   { armAngleTgt   = constrain(server.arg("arm").toInt(), 0, 180); }
  sendCORS(200, "text/plain", "OK");
}

void handleSolar() {
  if (server.hasArg("mode")) {
    String m = server.arg("mode");
    solarAutoTrack = (m == "auto");
  }
  sendCORS(200, "text/plain", "OK");
}

void handleBuzzer() {
  if (server.hasArg("state")) {
    String s = server.arg("state");
    buzzerOn = (s == "on");
    digitalWrite(BUZZER_PIN, buzzerOn ? HIGH : LOW);
  }
  sendCORS(200, "text/plain", "OK");
}

void handleAutoStart() {
  if (server.hasArg("length") && server.hasArg("width")) {
    gridRows = server.arg("length").toInt();
    gridCols = server.arg("width").toInt();
    sampleCount = 0; curRow = 0; curCol = 0; serpentineFwd = true;
    
    // Start by moving to the very first node
    moveForward();
    autoState = AUTO_MOVE_FORWARD;
    autoTimer = millis();
  }
  sendCORS(200, "text/plain", "OK");
}

void handleAutoStop() {
  autoState = AUTO_IDLE;
  stopMotors();
  sendCORS(200, "text/plain", "OK");
}

void handleSamples() {
  String j = "[";
  for (int i = 0; i < sampleCount; i++) {
    SoilSample &s = samples[i];
    j += "{\"row\":" + String(s.row) + ",\"col\":" + String(s.col);
    j += ",\"moisture\":" + String(s.moisture, 1);
    j += ",\"temp\":" + String(s.soilTemp, 1);
    j += ",\"hum\":" + String(s.ambientHum, 1);
    j += ",\"ph\":" + String(s.ph, 1);
    j += ",\"n\":" + String(s.n);
    j += ",\"p\":" + String(s.p);
    j += ",\"k\":" + String(s.k);
    j += ",\"lat\":" + String(s.lat, 6);
    j += ",\"lng\":" + String(s.lng, 6);
    j += ",\"ambientTemp\":" + String(s.ambientTemp, 1);
    j += ",\"gpsValid\":" + String((s.lat != 0 || s.lng != 0) ? "true" : "false");
    j += ",\"sampleId\":\"SMP-" + String(i, DEC) + "\"";
    j += ",\"quality\":\"HIGH_VALID\"";
    j += "}";
    if (i < sampleCount - 1) j += ",";
  }
  j += "]";
  sendCORS(200, "application/json", j);
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== AgroBot v5.0 — SN-3002 Precision Agriculture ===");

  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LDR_DIGITAL_PIN, INPUT);
  
  stopMotors();
  digitalWrite(BUZZER_PIN, LOW);

  solarServo.attach(SERVO_SOLAR_PIN);
  armServo.attach(SERVO_ARM_PIN);
  solarServo.write(solarAngleCur);
  armServo.write(armAngleCur);

  Wire.begin(I2C_SDA, I2C_SCL);
  mpu.initialize();
  if (mpu.testConnection()) Serial.println("MPU6050 OK");
  if (bmp.begin()) { Serial.println("BMP180 OK"); bmpOk = true; }
  dht.begin();

  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  initSoilSensor(RS485_RX, RS485_TX, RS485_EN);

  // Initialize WiFi in Dual Mode: SoftAP (Fallback) + Station (Hotspot)
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP("AGRO-ROVER", "agro12345");
  Serial.print("\n[WIFI] SoftAP started: 'AGRO-ROVER' | IP: http://");
  Serial.println(WiFi.softAPIP());

  WiFi.begin(staSSID, staPASS);
  Serial.print("[WIFI] Connecting to Hotspot: "); Serial.print(staSSID);
  
  // Wait for connection
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected to Hotspot!");
    Serial.print("[WIFI] Rover Station IP: http://"); Serial.println(WiFi.localIP());
    Serial.println("*** ENTER THIS IP IN THE DASHBOARD SETTINGS ***");
  } else {
    Serial.println("\n[WIFI] Hotspot not connected. Using fallback SoftAP!");
    Serial.println("*** Connect PC to WiFi 'AGRO-ROVER' (pass: agro12345) and use 192.168.4.1 in Dashboard ***");
  }

  server.on("/", HTTP_OPTIONS, handleOptions);
  server.on("/data", HTTP_OPTIONS, handleOptions);
  server.on("/control", HTTP_OPTIONS, handleOptions);
  server.on("/servo", HTTP_OPTIONS, handleOptions);
  server.on("/solar", HTTP_OPTIONS, handleOptions);
  server.on("/buzzer", HTTP_OPTIONS, handleOptions);
  server.on("/auto/start", HTTP_OPTIONS, handleOptions);
  server.on("/auto/stop", HTTP_OPTIONS, handleOptions);
  server.on("/samples", HTTP_OPTIONS, handleOptions);
  server.on("/api/soil", HTTP_OPTIONS, handleOptions);

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.on("/control", handleControl);
  server.on("/servo", handleServo);
  server.on("/solar", handleSolar);
  server.on("/buzzer", handleBuzzer);
  server.on("/auto/start", handleAutoStart);
  server.on("/auto/stop", handleAutoStop);
  server.on("/samples", handleSamples);
  server.on("/api/soil", handleSoilApi);

  server.onNotFound([]() {
    if (server.method() == HTTP_OPTIONS) {
      sendCORS(204, "text/plain", "");
    } else {
      sendCORS(404, "text/plain", "Not Found");
    }
  });

  server.begin();
  Serial.println("Web server running.");
}

// ============================================================
// MAIN LOOP
// ============================================================
static unsigned long lastSoilMs = 0;
#define SOIL_READ_INTERVAL 2500

void loop() {
  while (gpsSerial.available() > 0)
    gps.encode(gpsSerial.read());

  server.handleClient();

  unsigned long now = millis();

  // Decoupled Modbus RS485 soil probe polling (2.5s) so server.handleClient() is never starved
  if (now - lastSoilMs >= SOIL_READ_INTERVAL) {
    lastSoilMs = now;
    if (autoState == AUTO_IDLE || autoState == AUTO_DONE) {
      readSoilSensor(currentSoilData);
      if (debugModbus) {
        if (WiFi.status() == WL_CONNECTED) {
          Serial.print("[NET] Active Rover IP: http://"); Serial.println(WiFi.localIP());
        } else {
          Serial.print("[NET] AP Mode Rover IP: http://"); Serial.println(WiFi.softAPIP());
        }
      }
    }
  }

  // Fast sensors and alerts (500ms)
  if (now - lastSensorMs >= SENSOR_INTERVAL) {
    lastSensorMs = now;
    readSensors();
    readMPU();
    updateGpsCache();
    updatePressureHistory();
    checkFieldAlerts();
    checkTerrainSafety();
  }

  if (solarAutoTrack && (now - lastSolarMs >= SOLAR_INTERVAL)) {
    lastSolarMs   = now;
    solarLdrLeft  = analogRead(LDR_LEFT_PIN);
    solarLdrRight = analogRead(LDR_RIGHT_PIN);
    int diff = solarLdrLeft - solarLdrRight;
    if (diff > SOLAR_DEADBAND) {
      solarAngleCur = max(0, solarAngleCur - 1);
      solarServo.write(solarAngleCur);
      solarAngleTgt = solarAngleCur;
    } else if (diff < -SOLAR_DEADBAND) {
      solarAngleCur = min(180, solarAngleCur + 1);
      solarServo.write(solarAngleCur);
      solarAngleTgt = solarAngleCur;
    }
  }

  if (!solarAutoTrack && (now - lastSolarMs >= SENSOR_INTERVAL)) {
    lastSolarMs   = now;
    solarLdrLeft  = analogRead(LDR_LEFT_PIN);
    solarLdrRight = analogRead(LDR_RIGHT_PIN);
  }

  servoEasingTick();

  if (autoState != AUTO_IDLE && autoState != AUTO_DONE) {
    autoTick();
  }
}