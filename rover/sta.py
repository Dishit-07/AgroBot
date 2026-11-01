import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/app_new/app_new.ino', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update global variables
text = text.replace('const char *apSSID = "AGRO-BOT";', 'const char *staSSID = "YOUR_HOTSPOT_NAME"; // <--- CHANGE THIS')
text = text.replace('const char *apPASS = "agro12345";', 'const char *staPASS = "YOUR_HOTSPOT_PASSWORD"; // <--- CHANGE THIS')

# 2. Update setup() WiFi connection
old_wifi = """  // Initialize WiFi AP
  WiFi.softAP(apSSID, apPASS);
  Serial.print("AP SSID: "); Serial.println(apSSID);
  Serial.print("AP IP address: "); Serial.println(WiFi.softAPIP());"""

new_wifi = """  // Initialize WiFi STA (Connect to Hotspot)
  WiFi.mode(WIFI_STA);
  WiFi.begin(staSSID, staPASS);
  Serial.print("Connecting to Hotspot: "); Serial.print(staSSID);
  
  // Wait for connection
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\\nConnected!");
    Serial.print("ESP32 IP address: "); Serial.println(WiFi.localIP());
    Serial.println(">>> ENTER THIS IP IN THE DASHBOARD SETTINGS <<<");
  } else {
    Serial.println("\\nWiFi Failed to connect. Check SSID/Password!");
  }"""

if old_wifi in text:
    text = text.replace(old_wifi, new_wifi)
    with open('app/app_new/app_new.ino', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated successfully to STA mode")
else:
    print("Could not find the old WiFi code to replace")
