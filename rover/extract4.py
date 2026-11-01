import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'(\.grid-\d+\s*{[^}]*})', text, re.DOTALL)
if m:
    print(m.group(1))

# Find the pH gauge
m2 = re.search(r'(<div class="metric-card accent-.*?Soil pH.*?</svg>\s*</div>\s*</div>)', text, re.DOTALL | re.IGNORECASE)
if m2:
    print(m2.group(1))

