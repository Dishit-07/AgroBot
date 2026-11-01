import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find overview section to see the structure of the cards
ov_start = text.find('Ambient Temperature')
print(text[ov_start-200:ov_start+500])

# Find Atmospheric Climate in Sensors
sns_start = text.find('Atmospheric Climate')
print(text[sns_start-50:sns_start+400])
