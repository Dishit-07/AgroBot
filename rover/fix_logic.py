import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/app_new/app_new.ino', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Change handleAutoStart to start by moving forward instead of probing immediately
old_start = """void handleAutoStart() {
  if (server.hasArg("length") && server.hasArg("width")) {
    gridRows = server.arg("length").toInt();
    gridCols = server.arg("width").toInt();
    sampleCount = 0; curRow = 0; curCol = 0; serpentineFwd = true;
    autoState = AUTO_STOP_SAMPLE;
    autoTimer = millis();
  }
  sendCORS(200, "text/plain", "OK");
}"""

new_start = """void handleAutoStart() {
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
}"""

text = text.replace(old_start, new_start)

# 2. Increase SERVO_STEP_MS back to a safe value to prevent brownouts
text = text.replace('#define SERVO_STEP_MS    8', '#define SERVO_STEP_MS    15')

with open('app/app_new/app_new.ino', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated logic')
