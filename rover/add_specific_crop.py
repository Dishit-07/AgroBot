import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_crop_block = """  // ---- CROP SUGGESTION ----
  if (has(q, ['crop','fasal','ugana','laga','boo','seed','beej','suggest',
              'kaun si','konsi','kya ugaye','kya lagaye','best crop',
              'farming','kheti','khet','ugayen','lagayen','suitable',
              'recommend','harvest','katai','sowing','buwai','ropai', 'फसल', 'उगाना', 'बीज', 'खेती', 'लगाएं'])) {
    const soilPct = Math.round(avgMoisture);
    const q2 = classifyQuality(soilPct);
    const crops = getCropRecommendations(q2, avgN, avgP, avgK);
    const names = crops.map(function(c) { return c.name; }).join(', ');
    if (hi) return prefixHi + 'moisture ' + soilPct + '% hai. Yeh fasle lagayein: ' + names + '.';
    return prefixEn + 'moisture is ' + soilPct + '%. Recommended crops are: ' + names + '.';
  }"""

new_crop_block = """  // ---- CROP SUGGESTION (General & Specific) ----
  // First, check if they asked about a SPECIFIC crop
  const specificCrops = {
    'wheat': 'Wheat', 'gehun': 'Wheat', 'gehu': 'Wheat', 'गेहूँ': 'Wheat',
    'corn': 'Corn/Maize', 'maize': 'Corn/Maize', 'makka': 'Corn/Maize', 'bhutta': 'Corn/Maize', 'मक्का': 'Corn/Maize',
    'tomato': 'Tomato', 'tamatar': 'Tomato', 'टमाटर': 'Tomato',
    'rice': 'Rice', 'chawal': 'Rice', 'dhan': 'Rice', 'चावल': 'Rice', 'धान': 'Rice',
    'potato': 'Potato', 'aloo': 'Potato', 'alu': 'Potato', 'आलू': 'Potato',
    'onion': 'Onion', 'pyaz': 'Onion', 'pyaaz': 'Onion', 'प्याज': 'Onion',
    'cabbage': 'Cabbage', 'patta gobhi': 'Cabbage', 'gobhi': 'Cabbage', 'गोभी': 'Cabbage',
    'sugarcane': 'Sugarcane', 'ganna': 'Sugarcane', 'गन्ना': 'Sugarcane',
    'tea': 'Tea/Coffee', 'coffee': 'Tea/Coffee', 'chai': 'Tea/Coffee', 'चाय': 'Tea/Coffee', 'कॉफी': 'Tea/Coffee',
    'legume': 'Legumes', 'dal': 'Legumes', 'daal': 'Legumes', 'peas': 'Legumes', 'दाल': 'Legumes',
    'sunflower': 'Sunflower', 'surajmukhi': 'Sunflower', 'सूरजमुखी': 'Sunflower', 'सनफ्लावर': 'Sunflower',
    'broccoli': 'Broccoli', 'ब्रोकोली': 'Broccoli',
    'sorghum': 'Sorghum', 'jowar': 'Sorghum', 'ज्वार': 'Sorghum',
    'groundnut': 'Groundnut', 'moongfali': 'Groundnut', 'मूंगफली': 'Groundnut',
    'millet': 'Millet', 'bajra': 'Millet', 'बाजरा': 'Millet',
    'garlic': 'Garlic', 'lahsun': 'Garlic', 'लहसुन': 'Garlic',
    'cactus': 'Cactus Fruit', 'dragon fruit': 'Cactus Fruit', 'कैक्टस': 'Cactus Fruit',
    'barley': 'Barley', 'jau': 'Barley', 'जौ': 'Barley',
    'aloe vera': 'Aloe Vera', 'aloe': 'Aloe Vera', 'एलोवेरा': 'Aloe Vera'
  };

  let askedSpecificCrop = null;
  for (let kw in specificCrops) {
    if (q.indexOf(kw) !== -1) {
      askedSpecificCrop = specificCrops[kw];
      break;
    }
  }

  if (askedSpecificCrop && has(q, ['kya', 'can i', 'should i', 'ugau', 'lagau', 'ugana', 'lagana', 'grow', 'plant', 'karu', 'chahiye'])) {
    const soilPct = Math.round(avgMoisture);
    const req = typeof CROP_REQUIREMENTS !== 'undefined' ? CROP_REQUIREMENTS[askedSpecificCrop] : null;
    if (req) {
      let isFeasible = true;
      let reason = '';
      if (soilPct < req.minMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ko kam se kam ${req.minMoisture}% moisture chahiye, aur abhi sirf ${soilPct}% hai.` : `Because ${askedSpecificCrop} needs at least ${req.minMoisture}% moisture, but current is ${soilPct}%.`);
      } else if (soilPct > req.maxMoisture) {
        isFeasible = false;
        reason = (hi ? `Kyunki ${askedSpecificCrop} ke liye zyada se zyada ${req.maxMoisture}% moisture chahiye, aur abhi excessive ${soilPct}% hai.` : `Because maximum recommended for ${askedSpecificCrop} is ${req.maxMoisture}%, but current is excessive at ${soilPct}%.`);
      } else {
        reason = (hi ? `Moisture level (${soilPct}%) bilkul perfect hai.` : `Moisture level (${soilPct}%) is perfect.`);
      }

      if (isFeasible) {
        return (hi ? `Haan, bilkul! ${reason} Aap ${askedSpecificCrop} laga sakte hain.` : `Yes, absolutely! ${reason} You can plant ${askedSpecificCrop}.`);
      } else {
        return (hi ? `Nahi, abhi ${askedSpecificCrop} lagana theek nahi rahega. ${reason}` : `No, planting ${askedSpecificCrop} is not recommended right now. ${reason}`);
      }
    }
  }

  // General crop suggestion
  if (has(q, ['crop','fasal','ugana','laga','boo','seed','beej','suggest',
              'kaun si','konsi','kya ugaye','kya lagaye','best crop',
              'farming','kheti','khet','ugayen','lagayen','suitable',
              'recommend','harvest','katai','sowing','buwai','ropai', 'फसल', 'उगाना', 'बीज', 'खेती', 'लगाएं'])) {
    const soilPct = Math.round(avgMoisture);
    const q2 = classifyQuality(soilPct);
    const crops = getCropRecommendations(q2, avgN, avgP, avgK);
    const names = crops.map(function(c) { return c.name; }).join(', ');
    if (hi) return prefixHi + 'moisture ' + soilPct + '% hai. Yeh fasle lagayein: ' + names + '.';
    return prefixEn + 'moisture is ' + soilPct + '%. Recommended crops are: ' + names + '.';
  }"""

if old_crop_block in text:
    text = text.replace(old_crop_block, new_crop_block)
else:
    print("Could not find the exact old crop block. Trying a regex approach.")
    import re
    # Try to find the bounds using regex
    m = re.search(r'// ---- CROP SUGGESTION ----.*?// ---- SURVEY / RESULTS ----', text, re.DOTALL)
    if m:
        text = text[:m.start()] + new_crop_block + '\n\n  // ---- SURVEY / RESULTS ----' + text[m.end()-29:]
        print("Used regex replacement.")
    else:
        print("Regex failed too.")

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added specific crop feasibility check to Agro-Bot!")
