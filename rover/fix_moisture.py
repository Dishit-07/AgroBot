import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# FIX 1: Average moisture calculation in updateResultsTab()
# The SN-3002 firmware already sends moisture as a percentage (0-100), NOT a raw ADC value (0-4095).
# So we should NOT divide by 4095.
text = text.replace(
    "const avgSoilPct  = Math.round(Math.max(0, Math.min(100, (avgMoisture/4095)*100)));",
    "const avgSoilPct  = Math.round(Math.max(0, Math.min(100, avgMoisture))); // SN-3002 already sends percentage"
)

# FIX 2: Per-sample quality calculation in the results table
text = text.replace(
    "const soilPctFn = m => Math.round(Math.max(0, Math.min(100, (m/4095)*100)));",
    "const soilPctFn = m => Math.round(Math.max(0, Math.min(100, m))); // SN-3002 already sends percentage"
)

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed moisture calculation - removed /4095 conversion (SN-3002 already sends %)")
