import re

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update updateGauge function
old_fn = '''  if(type==='soil'){
    if(pct>=60){statusEl.textContent='WET';statusEl.className='gauge-status good';arc.className.baseVal='gauge-fill green';}
    else if(pct>=30){statusEl.textContent='MODERATE';statusEl.className='gauge-status warn';arc.className.baseVal='gauge-fill purple';}
    else{statusEl.textContent='DRY';statusEl.className='gauge-status bad';arc.className.baseVal='gauge-fill red';}
  } else if(type==='gas'){
    if(pct<=25){statusEl.textContent='CLEAN';statusEl.className='gauge-status good';arc.className.baseVal='gauge-fill green';}
    else if(pct<=50){statusEl.textContent='MODERATE';statusEl.className='gauge-status warn';arc.className.baseVal='gauge-fill amber';}
    else{statusEl.textContent='POOR';statusEl.className='gauge-status bad';arc.className.baseVal='gauge-fill red';}
  }'''

new_fn = '''  if(type==='soil'){
    if(pct>=60){statusEl.textContent='WET';statusEl.className='gauge-status good';arc.className.baseVal='gauge-fill green';}
    else if(pct>=30){statusEl.textContent='MODERATE';statusEl.className='gauge-status warn';arc.className.baseVal='gauge-fill purple';}
    else{statusEl.textContent='DRY';statusEl.className='gauge-status bad';arc.className.baseVal='gauge-fill red';}
  } else if(type==='ph'){
    pctEl.innerHTML = pct.toFixed(1); // pH does not have %
    arc.style.strokeDashoffset = GAUGE_CIRC - (pct/14.0)*GAUGE_CIRC;
    if(pct<5.5){statusEl.textContent='ACIDIC';statusEl.className='gauge-status bad';arc.className.baseVal='gauge-fill red';}
    else if(pct<=7.5){statusEl.textContent='NEUTRAL';statusEl.className='gauge-status good';arc.className.baseVal='gauge-fill green';}
    else{statusEl.textContent='ALKALINE';statusEl.className='gauge-status warn';arc.className.baseVal='gauge-fill purple';}
  }'''

content = content.replace(old_fn, new_fn)

# Also fix the NPK json parsing in poll()
content = content.replace("document.getElementById('ovN').textContent       = d.n.toFixed(1)+' mg/kg';", "document.getElementById('ovN').textContent       = (d.nitrogen||0)+' mg/kg';")
content = content.replace("document.getElementById('ovP').textContent       = d.p.toFixed(1)+' mg/kg';", "document.getElementById('ovP').textContent       = (d.phosphorus||0)+' mg/kg';")
content = content.replace("document.getElementById('ovK').textContent       = d.k.toFixed(1)+' mg/kg';", "document.getElementById('ovK').textContent       = (d.potassium||0)+' mg/kg';")

content = content.replace("if(d.n!==undefined) {", "if(d.nitrogen!==undefined) {")
content = content.replace("document.getElementById('sN').textContent = d.n.toFixed(1);", "document.getElementById('sN').textContent = d.nitrogen;")
content = content.replace("document.getElementById('sNBar').textContent = npkLevel(d.n,20,120);", "document.getElementById('sNBar').textContent = npkLevel(d.nitrogen,20,120);")

content = content.replace("if(d.p!==undefined) {", "if(d.phosphorus!==undefined) {")
content = content.replace("document.getElementById('sP').textContent = d.p.toFixed(1);", "document.getElementById('sP').textContent = d.phosphorus;")
content = content.replace("document.getElementById('sPBar').textContent = npkLevel(d.p,15,80);", "document.getElementById('sPBar').textContent = npkLevel(d.phosphorus,15,80);")

content = content.replace("if(d.k!==undefined) {", "if(d.potassium!==undefined) {")
content = content.replace("document.getElementById('sK').textContent = d.k.toFixed(1);", "document.getElementById('sK').textContent = d.potassium;")
content = content.replace("document.getElementById('sKBar').textContent = npkLevel(d.k,30,150);", "document.getElementById('sKBar').textContent = npkLevel(d.potassium,30,150);")

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(content)
