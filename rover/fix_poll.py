import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix d.soil references (old raw ADC field no longer in JSON)
# These lines crash the poll() because d.soil is undefined
text = text.replace(
    "document.getElementById('ovSoilRaw').textContent = d.soil;",
    "// ovSoilRaw: SN-3002 replaces raw ADC"
)
text = text.replace(
    "document.getElementById('sSoilRaw').textContent = d.soil;",
    "// sSoilRaw: SN-3002 replaces raw ADC"
)

# 2. Fix chart history push - d.soil no longer exists, use d.soilMoisture
text = text.replace(
    "histData.soil.push(d.soil);",
    "histData.soil.push(d.soilMoisture||0);"
)

# 3. Fix chart Y-axis scale - was 0-4095 (raw ADC), now 0-100 (%)
text = text.replace(
    "drawLine(histData.soil,'#16a34a',0,4095);",
    "drawLine(histData.soil,'#16a34a',0,100);"
)

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Dashboard fixed successfully')
