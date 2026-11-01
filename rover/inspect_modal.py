# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('D:/Graphic hackathon/rover/dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="settingsModal"')
print(text[idx-50:idx+800])
