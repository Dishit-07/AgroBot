import re

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Sensor Connection Status
content = content.replace(
    '<div class="conn-status" id="connStatus">\n          <div class="conn-dot"></div>\n          <span id="connText">CONNECTING</span>\n        </div>',
    '<div class="conn-status" id="connStatus">\n          <div class="conn-dot"></div>\n          <span id="connText">CONNECTING</span>\n        </div>\n        <div class="conn-status offline" id="sensorStatusBadge" style="margin-left: 10px; background:#f1f5f9; border-color:#cbd5e1; color:#475569;">\n          <span id="sensorStatusText" style="font-weight: 800; font-size: 0.75rem;">SN-3002: WAIT</span>\n        </div>'
)

# Update NPK text on Overview
content = content.replace('NPK Live Estimation', 'SN-3002 NPK Reading')
content = content.replace('Sensor fusion model (moisture + temp + gas)', 'Direct RS485 Data Link')

# Update Soil Moisture Gauge raw text
content = content.replace('Raw: <span id="ovSoilRaw\">--</span> / 4095', 'SN-3002 Active Probe')
content = content.replace('Soil Raw: <span id="sSoilRaw\">--</span>', 'Probe Active')

# Update Air Quality to pH on Overview
content = content.replace('💨 Air Quality (MQ135)', '⚗️ Soil pH')
content = content.replace('id="ovGasArc"', 'id="ovPhArc"')
content = content.replace('id="ovGasPct"', 'id="ovPhPct"')
content = content.replace('id="ovGasStatus"', 'id="ovPhStatus"')
content = content.replace('Raw: <span id="ovGasRaw">--</span> / 4095', 'SN-3002 RS485')

# Update Page 2 (Sensors)
# Soil Moisture and Gas (now pH)
content = content.replace('id="sGasArc"', 'id="sPhArc"')
content = content.replace('id="sGasPct"', 'id="sPhPct"')
content = content.replace('id="sGasStatus"', 'id="sPhStatus"')
content = content.replace('AQI Raw: <span id="sGasRaw">--</span>', 'pH Sensor Active')

# Update NPK area on Page 2
content = content.replace('Soil Nutrient Matrix (NPK + Density)', 'Soil Nutrient Matrix (SN-3002 Direct)')

density_html = '''<div style="background:var(--bg-card-subtle);padding:14px;border-radius:var(--radius-md);border:1px solid var(--border-card);">
                <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;font-weight:800;margin-bottom:6px;">Soil Density</div>
                <div style="font-family:var(--font-mono);font-size:1.35rem;font-weight:800;color:var(--text-main);"><span id="sDensity">--</span> <span style="font-size:0.72rem;color:var(--text-muted);">ADC/10</span></div>
              </div>'''
content = content.replace(density_html, '')
content = content.replace('<div class="grid-4" style="gap:14px;margin-top:10px;">', '<div class="grid-3" style="gap:14px;margin-top:10px;">')

# Table Headers
content = content.replace('<th>Moist</th><th>T°C</th><th>Hum%</th>', '<th>Moist%</th><th>Soil T°C</th><th>pH</th><th>Air Hum%</th>')
content = content.replace('<th>Moisture</th><th>Temp(°C)</th><th>Hum(%)</th>', '<th>Moist(%)</th><th>Soil T(°C)</th><th>pH</th><th>Air Hum(%)</th>')

# Default IP
content = content.replace("let ESP_IP  = localStorage.getItem('esp_ip') || '';", "let ESP_IP  = localStorage.getItem('esp_ip') || '192.168.4.1';")

# JS Polling logic updates
# Replace soilPct and gasPct logic with real values
poll_js_old = '''// Soil %
      const soilPct = Math.round(Math.max(0, Math.min(100, (d.soil/4095)*100)));
      const gasPct  = Math.round(Math.max(0, Math.min(100, (d.gas/4095)*100)));'''
poll_js_new = '''const soilPct = Math.round(d.soilMoisture || 0);
      const phVal = d.ph || 0;
      
      // Update sensor status badge
      const sb = document.getElementById('sensorStatusBadge');
      const st = document.getElementById('sensorStatusText');
      if (d.sensorStatus === 'VALID') {
          sb.style.background = '#dcfce7'; sb.style.borderColor = '#86efac'; sb.style.color = '#15803d';
          st.textContent = 'SN-3002: VALID ✓';
      } else {
          sb.style.background = '#fee2e2'; sb.style.borderColor = '#fca5a5'; sb.style.color = '#b91c1c';
          st.textContent = 'SN-3002: ' + (d.sensorStatus || 'ERR');
      }
'''
content = content.replace(poll_js_old, poll_js_new)

# Update gas gauge call to ph gauge call
content = content.replace("updateGauge('ovGasArc','ovGasPct','ovGasStatus', gasPct, 'gas');", "updateGauge('ovPhArc','ovPhPct','ovPhStatus', phVal, 'ph');")
content = content.replace("updateGauge('sGasArc','sGasPct','sGasStatus', gasPct, 'gas');", "updateGauge('sPhArc','sPhPct','sPhStatus', phVal, 'ph');")

content = content.replace("document.getElementById('ovGasRaw').textContent  = d.gas;", "")
content = content.replace("document.getElementById('sGasRaw').textContent  = d.gas;", "")

content = content.replace("if(d.density!==undefined) document.getElementById('sDensity').textContent = d.density.toFixed(1);", "")

# Sample Table rows
content = content.replace("<td>${s.temp.toFixed(1)}</td><td>${s.hum.toFixed(1)}</td>", "<td>${s.temp.toFixed(1)}</td><td>${s.ph.toFixed(1)}</td><td>${s.hum.toFixed(1)}</td>")

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(content)
