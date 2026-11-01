import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CROP_REQUIREMENTS
old_crop_req = '''const CROP_REQUIREMENTS = {
  "Wheat": { minMoisture: 40, maxMoisture: 80, minN: 40, minP: 20, minK: 40, icon: '🌾' },
  "Corn/Maize": { minMoisture: 50, maxMoisture: 90, minN: 50, minP: 30, minK: 50, icon: '🌽' },
  "Tomato": { minMoisture: 60, maxMoisture: 90, minN: 60, minP: 40, minK: 60, icon: '🍅' },
  "Rice": { minMoisture: 80, maxMoisture: 100, minN: 30, minP: 20, minK: 30, icon: '🌾' },
  "Potato": { minMoisture: 50, maxMoisture: 80, minN: 50, minP: 40, minK: 80, icon: '🥔' },
  "Onion": { minMoisture: 40, maxMoisture: 70, minN: 40, minP: 30, minK: 40, icon: '🧅' },
  "Cabbage": { minMoisture: 60, maxMoisture: 90, minN: 60, minP: 30, minK: 50, icon: '🥬' },
  "Sugarcane": { minMoisture: 70, maxMoisture: 100, minN: 60, minP: 40, minK: 80, icon: '🌿' },
  "Tea/Coffee": { minMoisture: 60, maxMoisture: 90, minN: 50, minP: 20, minK: 40, icon: '🍃' },
  "Legumes": { minMoisture: 40, maxMoisture: 70, minN: 10, minP: 30, minK: 40, icon: '🫛' },
  "Sunflower": { minMoisture: 30, maxMoisture: 60, minN: 40, minP: 20, minK: 40, icon: '🌻' },
  "Broccoli": { minMoisture: 60, maxMoisture: 90, minN: 60, minP: 30, minK: 50, icon: '🥦' },
  "Sorghum": { minMoisture: 20, maxMoisture: 60, minN: 30, minP: 15, minK: 30, icon: '🌾' },
  "Groundnut": { minMoisture: 30, maxMoisture: 60, minN: 20, minP: 20, minK: 30, icon: '🥜' },
  "Millet": { minMoisture: 20, maxMoisture: 50, minN: 20, minP: 15, minK: 20, icon: '🌱' },
  "Garlic": { minMoisture: 30, maxMoisture: 60, minN: 40, minP: 30, minK: 40, icon: '🧄' },
  "Cactus Fruit": { minMoisture: 5, maxMoisture: 30, minN: 10, minP: 10, minK: 20, icon: '🌵' },
  "Barley": { minMoisture: 20, maxMoisture: 60, minN: 30, minP: 20, minK: 30, icon: '🌾' },
  "Aloe Vera": { minMoisture: 5, maxMoisture: 40, minN: 10, minP: 10, minK: 20, icon: '🌿' }
};'''

new_crop_req = '''const CROP_REQUIREMENTS = {
  "Wheat": { minMoisture: 40, maxMoisture: 80, minTemp: 10, maxTemp: 25, minPh: 6.0, maxPh: 7.0, minN: 40, minP: 20, minK: 40, icon: '🌾' },
  "Corn/Maize": { minMoisture: 50, maxMoisture: 90, minTemp: 18, maxTemp: 32, minPh: 5.8, maxPh: 7.0, minN: 50, minP: 30, minK: 50, icon: '🌽' },
  "Tomato": { minMoisture: 60, maxMoisture: 90, minTemp: 18, maxTemp: 30, minPh: 6.0, maxPh: 6.8, minN: 60, minP: 40, minK: 60, icon: '🍅' },
  "Rice": { minMoisture: 80, maxMoisture: 100, minTemp: 20, maxTemp: 35, minPh: 5.0, maxPh: 6.5, minN: 30, minP: 20, minK: 30, icon: '🌾' },
  "Potato": { minMoisture: 50, maxMoisture: 80, minTemp: 15, maxTemp: 25, minPh: 5.0, maxPh: 6.5, minN: 50, minP: 40, minK: 80, icon: '🥔' },
  "Onion": { minMoisture: 40, maxMoisture: 70, minTemp: 13, maxTemp: 28, minPh: 6.0, maxPh: 7.0, minN: 40, minP: 30, minK: 40, icon: '🧅' },
  "Cabbage": { minMoisture: 60, maxMoisture: 90, minTemp: 15, maxTemp: 25, minPh: 6.0, maxPh: 6.8, minN: 60, minP: 30, minK: 50, icon: '🥬' },
  "Sugarcane": { minMoisture: 70, maxMoisture: 100, minTemp: 22, maxTemp: 35, minPh: 6.0, maxPh: 7.5, minN: 60, minP: 40, minK: 80, icon: '🌿' },
  "Tea/Coffee": { minMoisture: 60, maxMoisture: 90, minTemp: 18, maxTemp: 28, minPh: 4.5, maxPh: 5.5, minN: 50, minP: 20, minK: 40, icon: '🍃' },
  "Legumes": { minMoisture: 40, maxMoisture: 70, minTemp: 20, maxTemp: 30, minPh: 6.0, maxPh: 7.5, minN: 10, minP: 30, minK: 40, icon: '🫛' },
  "Sunflower": { minMoisture: 30, maxMoisture: 60, minTemp: 20, maxTemp: 35, minPh: 6.0, maxPh: 7.5, minN: 40, minP: 20, minK: 40, icon: '🌻' },
  "Broccoli": { minMoisture: 60, maxMoisture: 90, minTemp: 15, maxTemp: 25, minPh: 6.0, maxPh: 6.8, minN: 60, minP: 30, minK: 50, icon: '🥦' },
  "Sorghum": { minMoisture: 20, maxMoisture: 60, minTemp: 25, maxTemp: 35, minPh: 5.5, maxPh: 8.5, minN: 30, minP: 15, minK: 30, icon: '🌾' },
  "Groundnut": { minMoisture: 30, maxMoisture: 60, minTemp: 25, maxTemp: 30, minPh: 5.5, maxPh: 7.0, minN: 20, minP: 20, minK: 30, icon: '🥜' },
  "Millet": { minMoisture: 20, maxMoisture: 50, minTemp: 25, maxTemp: 35, minPh: 5.5, maxPh: 7.5, minN: 20, minP: 15, minK: 20, icon: '🌱' },
  "Garlic": { minMoisture: 30, maxMoisture: 60, minTemp: 12, maxTemp: 25, minPh: 6.0, maxPh: 7.0, minN: 40, minP: 30, minK: 40, icon: '🧄' },
  "Cactus Fruit": { minMoisture: 5, maxMoisture: 30, minTemp: 18, maxTemp: 40, minPh: 6.0, maxPh: 8.0, minN: 10, minP: 10, minK: 20, icon: '🌵' },
  "Barley": { minMoisture: 20, maxMoisture: 60, minTemp: 12, maxTemp: 25, minPh: 6.0, maxPh: 8.0, minN: 30, minP: 20, minK: 30, icon: '🌾' },
  "Aloe Vera": { minMoisture: 5, maxMoisture: 40, minTemp: 20, maxTemp: 40, minPh: 7.0, maxPh: 8.5, minN: 10, minP: 10, minK: 20, icon: '🌿' }
};'''
text = text.replace(old_crop_req, new_crop_req)

# 2. Update getCropRecommendations signature and logic
old_get_crop = '''function getCropRecommendations(moisture, n, p, k) {
  if (moisture < 10) {
    return [{ icon:'❌', name:'No crops', note:'Irrigate before planting' }];
  }
  
  let suitable = [];
  for (let cropName in CROP_REQUIREMENTS) {
    const req = CROP_REQUIREMENTS[cropName];
    if (moisture >= req.minMoisture && moisture <= req.maxMoisture) {'''

new_get_crop = '''function getCropRecommendations(moisture, temp, ph, n, p, k) {
  if (moisture < 10) {
    return [{ icon:'❌', name:'No crops', note:'Irrigate before planting' }];
  }
  
  let suitable = [];
  for (let cropName in CROP_REQUIREMENTS) {
    const req = CROP_REQUIREMENTS[cropName];
    // Check all survival factors: Moisture, Temperature, and pH
    if (moisture >= req.minMoisture && moisture <= req.maxMoisture &&
        temp >= req.minTemp && temp <= req.maxTemp &&
        ph >= req.minPh && ph <= req.maxPh) {'''
text = text.replace(old_get_crop, new_get_crop)

# 3. Update calls to getCropRecommendations
text = text.replace('const crops = getCropRecommendations(avgSoilPct, avgN, avgP, avgK);',
                    'const crops = getCropRecommendations(avgSoilPct, avgTemp, avgPh, avgN, avgP, avgK);')
text = text.replace('const crops = getCropRecommendations(soilPct, avgN, avgP, avgK);',
                    'const crops = getCropRecommendations(soilPct, temp, avgPh, avgN, avgP, avgK);')


# 4. Update analyzeSelectedCrop to include temp and pH calculation and checks
old_analyze = '''  // Calculate averages
  let sumMoisture=0, sumN=0, sumP=0, sumK=0;
  lastSamples.forEach(s => {
    sumMoisture += s.moisture;
    sumN += s.n; sumP += s.p; sumK += s.k;
  });
  const count = lastSamples.length;
  const avgMoisture = sumMoisture / count;
  const avgSoilPct  = Math.round(Math.max(0, Math.min(100, avgMoisture))); // SN-3002 already sends percentage
  const avgN = sumN/count, avgP = sumP/count, avgK = sumK/count;

  const req = CROP_REQUIREMENTS[cropName];
  let survive = true;
  let reasons = [];
  let amendments = [];

  // Moisture check
  if (avgSoilPct < req.minMoisture) {
    survive = false;
    reasons.push(`Soil moisture is deficient (${avgSoilPct}%). ${cropName} requires at least ${req.minMoisture}%.`);
    amendments.push(`💧 <strong>Irrigation Scheduling:</strong> Irrigate to raise soil moisture by ~${req.minMoisture - avgSoilPct}%.`);
  } else if (avgSoilPct > req.maxMoisture) {
    survive = false;
    reasons.push(`Soil moisture is excessive (${avgSoilPct}%). Max recommended is ${req.maxMoisture}%.`);
    amendments.push(`☀️ <strong>Drainage Management:</strong> Enhance sub-surface aeration and drainage to avoid root rot.`);
  } else {
    reasons.push(`Moisture content is optimal (${avgSoilPct}%).`);
  }'''

new_analyze = '''  // Calculate averages
  let sumMoisture=0, sumTemp=0, sumPh=0, sumN=0, sumP=0, sumK=0;
  lastSamples.forEach(s => {
    sumMoisture += s.moisture;
    sumTemp += s.temp;
    sumPh += s.ph;
    sumN += s.n; sumP += s.p; sumK += s.k;
  });
  const count = lastSamples.length;
  const avgMoisture = sumMoisture / count;
  const avgSoilPct  = Math.round(Math.max(0, Math.min(100, avgMoisture)));
  const avgTemp = sumTemp/count;
  const avgPh = sumPh/count;
  const avgN = sumN/count, avgP = sumP/count, avgK = sumK/count;

  const req = CROP_REQUIREMENTS[cropName];
  let survive = true;
  let reasons = [];
  let amendments = [];

  // Moisture check
  if (avgSoilPct < req.minMoisture) {
    survive = false;
    reasons.push(`Soil moisture is deficient (${avgSoilPct}%). ${cropName} requires at least ${req.minMoisture}%.`);
    amendments.push(`💧 <strong>Irrigation:</strong> Irrigate to raise soil moisture.`);
  } else if (avgSoilPct > req.maxMoisture) {
    survive = false;
    reasons.push(`Soil moisture is excessive (${avgSoilPct}%). Max recommended is ${req.maxMoisture}%.`);
    amendments.push(`☀️ <strong>Drainage:</strong> Enhance sub-surface aeration and drainage.`);
  } else {
    reasons.push(`Moisture content is optimal (${avgSoilPct}%).`);
  }
  
  // Temp check
  if (avgTemp < req.minTemp) {
    survive = false;
    reasons.push(`Temperature is too cold (${avgTemp.toFixed(1)}°C). ${cropName} needs at least ${req.minTemp}°C.`);
  } else if (avgTemp > req.maxTemp) {
    survive = false;
    reasons.push(`Temperature is too hot (${avgTemp.toFixed(1)}°C). ${cropName} requires under ${req.maxTemp}°C.`);
  } else {
    reasons.push(`Temperature is ideal (${avgTemp.toFixed(1)}°C).`);
  }

  // pH check
  if (avgPh < req.minPh) {
    survive = false;
    reasons.push(`Soil is too acidic (pH ${avgPh.toFixed(1)}). ${cropName} needs min pH ${req.minPh}.`);
    amendments.push(`🧪 <strong>pH Correction:</strong> Add lime to raise pH.`);
  } else if (avgPh > req.maxPh) {
    survive = false;
    reasons.push(`Soil is too alkaline (pH ${avgPh.toFixed(1)}). ${cropName} needs max pH ${req.maxPh}.`);
    amendments.push(`🧪 <strong>pH Correction:</strong> Add sulfur/gypsum to lower pH.`);
  } else {
    reasons.push(`Soil pH is ideal (${avgPh.toFixed(1)}).`);
  }'''
text = text.replace(old_analyze, new_analyze)

# 5. Fix updateResultsTab where avgTemp and avgPh might not be defined
old_res_tab = '''  const avgMoisture = sumMoisture / count;
  const avgSoilPct  = Math.round(Math.max(0, Math.min(100, avgMoisture))); // SN-3002 already sends percentage
  const avgN = sumN/count, avgP = sumP/count, avgK = sumK/count;

  document.getElementById('resSoilPct').textContent = avgSoilPct + '%';'''

new_res_tab = '''  const avgMoisture = sumMoisture / count;
  const avgSoilPct  = Math.round(Math.max(0, Math.min(100, avgMoisture))); // SN-3002 already sends percentage
  let sumTemp=0, sumPh=0;
  samples.forEach(s => { sumTemp+=s.temp; sumPh+=s.ph; });
  const avgTemp = sumTemp/count;
  const avgPh = sumPh/count;
  const avgN = sumN/count, avgP = sumP/count, avgK = sumK/count;

  document.getElementById('resSoilPct').textContent = avgSoilPct + '%';'''
text = text.replace(old_res_tab, new_res_tab)

# 6. Finally, update Agro-Bot specific crop logic to check Temp and pH
old_agrobot_spec = '''      if (soilPct < req.minMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ko kam se kam ${req.minMoisture}% moisture chahiye, aur abhi sirf ${soilPct}% hai.` : `Because ${askedSpecificCrop} needs at least ${req.minMoisture}% moisture, but current is ${soilPct}%.`);
      } else if (soilPct > req.maxMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ke liye zyada se zyada ${req.maxMoisture}% moisture chahiye, aur abhi excessive ${soilPct}% hai.` : `Because maximum recommended for ${askedSpecificCrop} is ${req.maxMoisture}%, but current is excessive at ${soilPct}%.`);
      } else {
        reason = (hi ? `Moisture level (${soilPct}%) bilkul perfect hai.` : `Moisture level (${soilPct}%) is perfect.`);
      }'''

new_agrobot_spec = '''      if (soilPct < req.minMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ko kam se kam ${req.minMoisture}% moisture chahiye, aur abhi ${soilPct}% hai.` : `Because ${askedSpecificCrop} needs at least ${req.minMoisture}% moisture, but current is ${soilPct}%.`);
      } else if (soilPct > req.maxMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ke liye max ${req.maxMoisture}% moisture chahiye, aur abhi excessive ${soilPct}% hai.` : `Because maximum recommended for ${askedSpecificCrop} is ${req.maxMoisture}%, but current is excessive at ${soilPct}%.`);
      } else if (temp < req.minTemp || temp > req.maxTemp) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ko ${req.minTemp} se ${req.maxTemp} degree temperature chahiye, par abhi ${temp.toFixed(1)} degree hai.` : `Because ${askedSpecificCrop} needs ${req.minTemp}-${req.maxTemp}°C, but current is ${temp.toFixed(1)}°C.`);
      } else if (avgPh < req.minPh || avgPh > req.maxPh) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ko ${req.minPh} se ${req.maxPh} pH chahiye, par mitti ka pH ${avgPh.toFixed(1)} hai.` : `Because ${askedSpecificCrop} needs pH ${req.minPh}-${req.maxPh}, but soil pH is ${avgPh.toFixed(1)}.`);
      } else {
        reason = (hi ? `Moisture (${soilPct}%), temperature aur pH bilkul perfect hain.` : `Moisture (${soilPct}%), temperature, and pH are perfect.`);
      }'''
text = text.replace(old_agrobot_spec, new_agrobot_spec)

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied for multi-sensor crop checking!")
