# -*- coding: utf-8 -*-
with open('D:/Graphic hackathon/rover/dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

ids = [
    'ovTemp', 'ovTempBar', 'ovHum', 'ovHumBar', 'ovSoilArc', 'ovSoilPct', 'ovSoilStatus', 
    'ovPhArc', 'ovPhPct', 'ovPhStatus', 'ovAqiArc', 'ovAqiPct', 'ovAqiStatus', 
    'ovPress', 'ovDay', 'ovSat', 'ovPos', 'ovTilt', 'ovYaw', 'ovN', 'ovP', 'ovK', 
    'ovQualityBadge', 'ovQualityScore', 'alertBanner', 'alertText', 'ovIrrBadge', 
    'ovIrrDesc', 'ovHealthArc', 'ovHealthPct', 'ovHealthStatus', 'ovWeatherText', 
    'ovWeatherIcon', 'ovCropName', 'ovCropIcon', 'ovCropReason', 'ovTerrainBadge', 
    'ovPriorityBadge', 'vSat', 'vLat', 'vLng', 'vAlt', 'vTime', 'vPitch', 'vRoll', 
    'vYaw', 'sTemp', 'sHum', 'sPress', 'sAqi', 'sSoilArc', 'sSoilPct', 'sSoilStatus', 
    'sPhArc', 'sPhPct', 'sPhStatus', 'sDay', 'sN', 'sNBar', 'sP', 'sPBar', 'sK', 
    'sKBar', 'rSolar', 'rvSolar', 'solarModeBtn', 'rvLdrL', 'rvLdrR', 'rArm', 'rvArm', 
    'buzBtn', 'progBar', 'progPct', 'progTxt', 'sensorStatusBadge', 'sensorStatusText',
    'sampleTbody', 'connStatus', 'connText'
]

missing = []
for el_id in ids:
    if f'id="{el_id}"' not in text:
        missing.append(el_id)

print("Missing elements:", missing)
