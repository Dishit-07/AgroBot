import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update updateResultsTab to pass avgSoilPct instead of q
text = text.replace('const crops = getCropRecommendations(q, avgN, avgP, avgK);',
                    'const crops = getCropRecommendations(avgSoilPct, avgN, avgP, avgK);')

# 2. Update getAgrobotAnswer to pass soilPct instead of q2
text = text.replace('const crops = getCropRecommendations(q2, avgN, avgP, avgK);',
                    'const crops = getCropRecommendations(soilPct, avgN, avgP, avgK);')

# 3. Rewrite getCropRecommendations
old_func = '''function getCropRecommendations(quality, n, p, k) {
  const crops = {
    excellent: [
      { icon:'🌾', name:'Wheat',       note:'High yield expected' },
      { icon:'🌽', name:'Corn/Maize',  note:'Ideal conditions' },
      { icon:'🍅', name:'Tomato',      note:'Excellent growth' },
      { icon:'🥬', name:'Cabbage',     note:'High moisture OK' },
      { icon:'🌿', name:'Sugarcane',   note:'Thrives in wet soil' },
      { icon:'🍃', name:'Tea/Coffee',  note:'Loves moisture' }
    ],
    good: [
      { icon:'🌾', name:'Rice',        note:'Good water availability' },
      { icon:'🥔', name:'Potato',      note:'Solid conditions' },
      { icon:'🧅', name:'Onion',       note:'Good growth expected' },
      { icon:'🫛', name:'Legumes',     note:'Nitrogen fixing, ideal' },
      { icon:'🌻', name:'Sunflower',   note:'Well-drained good' },
      { icon:'🥦', name:'Broccoli',    note:'Moderate moisture OK' }
    ],
    moderate: [
      { icon:'🌾', name:'Sorghum',     note:'Drought-tolerant' },
      { icon:'🥜', name:'Groundnut',   note:'Adapts to conditions' },
      { icon:'🌱', name:'Millet',      note:'Low-water crop' },
      { icon:'🧄', name:'Garlic',      note:'Dry soil preferred' }
    ],
    poor: [
      { icon:'🌵', name:'Cactus Fruit',note:'Drought specialist' },
      { icon:'🌾', name:'Barley',      note:'Handles dry conditions' },
      { icon:'🌿', name:'Aloe Vera',   note:'Minimal water needed' }
    ],
    critical: [
      { icon:'❌', name:'No crops',    note:'Irrigate before planting' }
    ]
  };
  return crops[quality.cls] || crops.poor;
}'''

new_func = '''function getCropRecommendations(moisture, n, p, k) {
  if (moisture < 10) {
    return [{ icon:'❌', name:'No crops', note:'Irrigate before planting' }];
  }
  
  let suitable = [];
  for (let cropName in CROP_REQUIREMENTS) {
    const req = CROP_REQUIREMENTS[cropName];
    if (moisture >= req.minMoisture && moisture <= req.maxMoisture) {
      let score = 0;
      if (n >= req.minN) score++;
      if (p >= req.minP) score++;
      if (k >= req.minK) score++;
      
      let note = 'Suitable conditions';
      if (score === 3) note = 'Ideal NPK conditions';
      else if (score === 2) note = 'Good conditions';
      else note = 'Requires NPK amendments';
      
      suitable.push({
        icon: req.icon,
        name: cropName,
        note: note,
        score: score
      });
    }
  }
  
  if (suitable.length === 0) {
    // If no crop perfectly matches, find the closest by moisture
    let closest = null;
    let minDiff = 999;
    for (let cropName in CROP_REQUIREMENTS) {
      const req = CROP_REQUIREMENTS[cropName];
      let diff = 0;
      if (moisture < req.minMoisture) diff = req.minMoisture - moisture;
      if (moisture > req.maxMoisture) diff = moisture - req.maxMoisture;
      if (diff < minDiff) {
        minDiff = diff;
        closest = { icon: req.icon, name: cropName, note: 'Needs soil pretreatment' };
      }
    }
    if (closest) suitable.push(closest);
  } else {
    // Sort by NPK match score descending
    suitable.sort((a,b) => b.score - a.score);
  }
  
  return suitable.slice(0, 6); // Return top 6
}'''

text = text.replace(old_func, new_func)

# 4. We also need to fix the general crop suggestion in Ask Agro-Bot to catch "laga", "sakta", "sakti", etc.
old_specific = "if (askedSpecificCrop && has(q, ['kya', 'can i', 'should i', 'ugau', 'lagau', 'ugana', 'lagana', 'grow', 'plant', 'karu', 'chahiye'])) {"
new_specific = "if (askedSpecificCrop && has(q, ['kya', 'can i', 'should i', 'ugau', 'lagau', 'ugana', 'lagana', 'laga', 'sakt', 'grow', 'plant', 'karu', 'chahiye'])) {"
text = text.replace(old_specific, new_specific)

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated getCropRecommendations logic!")
