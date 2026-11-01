import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update grid-4 to grid-5 in the first instance (Overview row)
# Actually, it's easier to just change the CSS to auto-fit instead of adding grid-5
# Let's do auto-fit for this specific container.
text = text.replace(
    '<div class="grid-4">',
    '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--grid-gap);">',
    1
)

# 2. Insert AQI card after pH card
ph_card_end = text.find('SN-3002 RS485</div>\n          </div>')
if ph_card_end != -1:
    insert_pos = ph_card_end + len('SN-3002 RS485</div>\n          </div>')
    aqi_card = '''
          <!-- AQI -->
          <div class="metric-card accent-purple">
            <div class="metric-header">
              <span class="metric-label">Air Quality (MQ135)</span>
              <div class="metric-icon-wrap">💨</div>
            </div>
            <div class="gauge-wrap" style="margin:auto">
              <svg class="gauge-svg" viewBox="0 0 120 120">
                <circle class="gauge-bg" cx="60" cy="60" r="45"/>
                <circle class="gauge-fill" cx="60" cy="60" r="45" id="ovAqiArc" stroke-dasharray="282.74" stroke-dashoffset="282.74"/>
              </svg>
              <div class="gauge-center">
                <div class="gauge-pct" id="ovAqiPct">--<span class="gauge-pct-sign">%</span></div>
                <div class="gauge-status" id="ovAqiStatus">--</div>
              </div>
            </div>
            <div class="fusion-note"><div class="fusion-dot"></div>AQI Estimate</div>
          </div>'''
    text = text[:insert_pos] + aqi_card + text[insert_pos:]

# 3. Add to Sensors tab
text = text.replace(
    '<div class="data-row"><span class="label">Atmospheric Pressure</span><span class="value" id="sPress">-- hPa</span></div>',
    '<div class="data-row"><span class="label">Atmospheric Pressure</span><span class="value" id="sPress">-- hPa</span></div>\n            <div class="data-row"><span class="label">Air Quality Index</span><span class="value" id="sAqi">--</span></div>'
)

# 4. JS: updateGauge support for 'gas'
text = text.replace(
    "} else if(type==='ph'){",
    "} else if(type==='gas'){  if(pct<=25){statusEl.textContent='CLEAN';statusEl.className='gauge-status good';arc.className.baseVal='gauge-fill green';} else if(pct<=50){statusEl.textContent='MODERATE';statusEl.className='gauge-status warn';arc.className.baseVal='gauge-fill amber';} else{statusEl.textContent='POOR';statusEl.className='gauge-status bad';arc.className.baseVal='gauge-fill red';} } else if(type==='ph'){"
)

# 5. JS: poll() update
text = text.replace(
    "updateGauge('ovPhArc','ovPhPct','ovPhStatus', phVal, 'ph');",
    "updateGauge('ovPhArc','ovPhPct','ovPhStatus', phVal, 'ph');\n      const aqiPct = Math.min(100, Math.round(((d.gas||0) / 4095) * 100));\n      updateGauge('ovAqiArc','ovAqiPct','ovAqiStatus', aqiPct, 'gas');"
)

text = text.replace(
    "document.getElementById('sPress').textContent = d.press.toFixed(1)+' hPa';",
    "document.getElementById('sPress').textContent = d.press.toFixed(1)+' hPa';\n      document.getElementById('sAqi').textContent = (d.gas||0) + ' (' + aqiPct + '%)';"
)

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added AQI successfully!")
