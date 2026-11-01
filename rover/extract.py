import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- OVERVIEW GRIDS ---")
m = re.search(r'<div class="grid-4".*?SOIL MOISTURE.*?SOIL PH.*?(<div class="grid-.*?>)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
else:
    print("Not found")

print("\n--- SENSORS CLIMATE ---")
m = re.search(r'ATMOSPHERIC CLIMATE.*?Atmospheric Pressure.*?</div>\s*</div>\s*</div>', text, re.DOTALL)
if m:
    print(m.group(0))
else:
    print("Not found")
