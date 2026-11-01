import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
# Check for app.ino in parent directories or backup
target_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'app backup', 'app.ino'))
if not os.path.exists(target_path):
    target_path = os.path.abspath(os.path.join(current_dir, '..', 'app.ino'))

if os.path.exists(target_path):
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pin replacements
    content = re.sub(r'#define DHTPIN\s+4', '#define DHTPIN 27', content)
    content = re.sub(r'#define GPS_RX\s+16', '#define GPS_RX 23', content)
    content = re.sub(r'#define GPS_TX\s+17', '#define GPS_TX 5', content)
    content = re.sub(r'#define SOIL_PIN\s+35\s*//[^\n]*\n', '', content)

    # Add RS485 pins
    rs485_pins = '''#define RS485_RX 16
#define RS485_TX 17
#define RS485_EN 4
'''
    content = re.sub(r'(#define GPS_TX\s+5\n)', r'\1' + rs485_pins, content)

    # Add headers
    content = re.sub(r'#include <Wire\.h>', '#include <Wire.h>\n#include "SoilSensor.h"', content)

    # Add globals
    globals_add = '''
SoilData currentSoilData;
bool debugModbus = true;
HardwareSerial RS485Serial(2);
const char *apSSID = "AGRO-BOT";
const char *apPASS = "agro12345";
'''
    content = re.sub(r'HardwareSerial gpsSerial\(2\);', 'HardwareSerial gpsSerial(1);\n' + globals_add, content)

    # Remove old WiFi vars
    content = re.sub(r'const char \*wifiSSID = "ROVER";\nconst char \*wifiPASS = "123456789";', '', content)
    content = re.sub(r'// WiFi reconnect watchdog\nunsigned long lastWifiCheckMs = 0;\nbool wifiWasConnected = false;\n', '', content)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

