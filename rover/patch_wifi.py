import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/app_new/app_new.ino', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
start = -1
end = -1
for i, line in enumerate(lines):
    if 'WiFi.softAP' in line:
        start = i - 1
    if 'WiFi.softAPIP' in line:
        end = i + 1

if start != -1 and end != -1:
    old_code = '\n'.join(lines[start:end])
    new_code = '''  // Initialize WiFi STA (Connect to Hotspot)
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
    Serial.println("*** ENTER THIS IP IN THE DASHBOARD SETTINGS ***");
  } else {
    Serial.println("\\nWiFi Failed to connect. Check SSID/Password!");
  }'''
    
    text = text.replace(old_code, new_code)
    text = text.replace('const char *apSSID = "AGRO-BOT";', 'const char *staSSID = "YOUR_HOTSPOT_NAME"; // <--- CHANGE THIS')
    text = text.replace('const char *apPASS = "agro12345";', 'const char *staPASS = "YOUR_HOTSPOT_PASSWORD"; // <--- CHANGE THIS')
    
    with open('app/app_new/app_new.ino', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated successfully to STA mode')
else:
    print('Could not find WiFi AP code')
