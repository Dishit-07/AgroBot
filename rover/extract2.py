import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- OVERVIEW ---")
for i, line in enumerate(lines):
    if 'AMBIENT TEMPERATURE' in line:
        print("".join(lines[i-2:i+20]))
        break

print("--- SENSORS ---")
for i, line in enumerate(lines):
    if 'ATMOSPHERIC CLIMATE' in line:
        print("".join(lines[i-2:i+20]))
        break
