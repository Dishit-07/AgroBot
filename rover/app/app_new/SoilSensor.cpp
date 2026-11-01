#include "SoilSensor.h"
#include "ModbusRS485.h"

extern bool debugModbus;

void initSoilSensor(int rxPin, int txPin, int enPin) {
    modbusInit(rxPin, txPin, enPin);
}

bool readSoilSensor(SoilData &data) {
    data.valid = false;
    uint8_t buffer[32];
    
    if (debugModbus) {
        Serial.println("[SENSOR] Requesting Moisture/Temp/pH...");
    }
    
    // 1. Read Moisture, Temp, (skip EC), pH
    // Registers 0x0000 to 0x0003 (4 registers) -> 13 bytes response
    // Response format: 01 03 08 [Moist_H] [Moist_L] [Temp_H] [Temp_L] [EC_H] [EC_L] [pH_H] [pH_L] [CRC_L] [CRC_H]
    sendModbusRequest(1, 0x0000, 4);
    int count = readModbusResponse(buffer, 13, 1000);
    
    if (count != 13 || buffer[0] != 1 || buffer[1] != 0x03 || buffer[2] != 8) {
        data.status = (count == 0) ? "TIMEOUT" : "INVALID_RESPONSE";
        return false;
    }
    
    uint16_t crc = modbusCRC(buffer, 11);
    uint16_t recvCRC = buffer[11] | (buffer[12] << 8);
    if (crc != recvCRC) {
        data.status = "CRC_ERROR";
        return false;
    }
    
    int rawMoisture = (buffer[3] << 8) | buffer[4];
    int rawTemp = (buffer[5] << 8) | buffer[6];
    int rawPH = (buffer[9] << 8) | buffer[10];
    
    data.moisture = rawMoisture / 10.0f;
    data.soilTemp = (rawTemp > 0x7FFF) ? ((rawTemp - 65536) / 10.0f) : (rawTemp / 10.0f); // Handle negative temp
    data.ph = rawPH / 10.0f;
    
    delay(100); // slight delay between Modbus requests
    
    if (debugModbus) {
        Serial.println("[SENSOR] Requesting NPK...");
    }
    
    // 2. Read N, P, K
    // Registers 0x0004 to 0x0006 (3 registers) -> 11 bytes response
    // Response format: 01 03 06 [N_H] [N_L] [P_H] [P_L] [K_H] [K_L] [CRC_L] [CRC_H]
    sendModbusRequest(1, 0x0004, 3);
    count = readModbusResponse(buffer, 11, 1000);
    
    if (count != 11 || buffer[0] != 1 || buffer[1] != 0x03 || buffer[2] != 6) {
        data.status = (count == 0) ? "TIMEOUT" : "INVALID_RESPONSE";
        return false;
    }
    
    crc = modbusCRC(buffer, 9);
    recvCRC = buffer[9] | (buffer[10] << 8);
    if (crc != recvCRC) {
        data.status = "CRC_ERROR";
        return false;
    }
    
    data.nitrogen = (buffer[3] << 8) | buffer[4];
    data.phosphorus = (buffer[5] << 8) | buffer[6];
    data.potassium = (buffer[7] << 8) | buffer[8];
    
    // Validation checks
    if (data.moisture < 0 || data.moisture > 100.0f || 
        data.ph < 0 || data.ph > 14.0f || 
        data.soilTemp < -40 || data.soilTemp > 80.0f ||
        data.nitrogen < 0 || data.phosphorus < 0 || data.potassium < 0 ||
        data.nitrogen > 1999 || data.phosphorus > 1999 || data.potassium > 1999) {
        data.status = "OUT_OF_RANGE";
        return false;
    }
    
    if (debugModbus) {
        Serial.println("[MODBUS] CRC OK");
        Serial.print("[SENSOR] Moisture: "); Serial.print(data.moisture); Serial.println(" %");
        Serial.print("[SENSOR] Soil Temp: "); Serial.print(data.soilTemp); Serial.println(" C");
        Serial.print("[SENSOR] pH: "); Serial.println(data.ph);
        Serial.print("[SENSOR] N: "); Serial.print(data.nitrogen); Serial.print(" mg/kg  ");
        Serial.print("P: "); Serial.print(data.phosphorus); Serial.print(" mg/kg  ");
        Serial.print("K: "); Serial.print(data.potassium); Serial.println(" mg/kg");
    }
    
    data.valid = true;
    data.timestamp = millis();
    data.status = "VALID";
    return true;
}
