import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '// ============================================================\n// ASK AGRO-BOT'
start = text.find(start_marker)
if start == -1:
    start_marker = '// ============================================================\r\n// ASK AGRO-BOT'
    start = text.find(start_marker)

end = text.find('</script>', start)

new_js = r"""// ============================================================
// ASK AGRO-BOT — VOICE ASSISTANT (v3 — Smart Analytics & Native Scripts)
// ============================================================

let recognition = null;
let isListening = false;
let voicesLoaded = false;

// ---- Keyword matching engine ----
function has(q, keywords) {
  for (let kw of keywords) {
    if (q.indexOf(kw) !== -1) return true;
  }
  return false;
}

function getAgrobotAnswer(question) {
  const d = lastData || {};
  const q = question.toLowerCase().trim();
  const samples = lastSamples || [];
  const lang = document.getElementById('voiceLang').value;
  const hi = lang.startsWith('hi') || lang.startsWith('pa') || lang.startsWith('mr') || lang.startsWith('bn') || lang.startsWith('gu') || lang.startsWith('ta') || lang.startsWith('te') || lang.startsWith('kn');

  // 1. Calculate Averages from Field Survey (if available)
  let avgMoisture = d.soilMoisture || 0;
  let avgPh = d.ph || 0;
  let avgN = d.nitrogen || 0;
  let avgP = d.phosphorus || 0;
  let avgK = d.potassium || 0;
  let isSurveyData = false;

  if (samples.length > 0) {
    let sumM=0, sumPh=0, sumN=0, sumP=0, sumK=0;
    samples.forEach(s => { sumM+=s.moisture; sumPh+=s.ph; sumN+=s.n; sumP+=s.p; sumK+=s.k; });
    avgMoisture = sumM / samples.length;
    avgPh = sumPh / samples.length;
    avgN = sumN / samples.length;
    avgP = sumP / samples.length;
    avgK = sumK / samples.length;
    isSurveyData = true;
  }

  const temp = d.temp || 0;
  const hum  = d.hum  || 0;
  const press = d.press || 0;
  const gas  = d.gas || 0;
  const day  = d.day;
  const aqiPct = Math.round((gas/4095)*100);
  
  const prefixHi = isSurveyData ? "Field survey analysis ke anusaar, " : "Live sensor ke anusaar, ";
  const prefixEn = isSurveyData ? "Based on the field survey, " : "Based on the live sensor, ";

  // ---- MOISTURE ----
  if (has(q, ['moisture','nami','neemi','geela','sukha','dry','wet','mitti','soil moisture',
              'paani mitti','kitna geela','kitni nami','moisture level','nam','nemee','moist',
              'water level','soil water','pani','jal', 'नमी', 'गीला', 'सूखा', 'मिट्टी', 'पानी'])) {
    if (hi) return prefixHi + 'moisture level ' + avgMoisture.toFixed(1) + '% hai. ' + (avgMoisture>=60?'Mitti kaafi geeli hai, paani dene ki zarurat nahi.':avgMoisture>=30?'Moisture theek hai, lekin dhyaan rakhein.':'Moisture kam hai, irrigation ki zarurat hai!');
    return prefixEn + 'soil moisture is ' + avgMoisture.toFixed(1) + '%. ' + (avgMoisture>=60?'Soil is well-watered, no irrigation needed.':avgMoisture>=30?'Moisture is moderate.':'Moisture is low, irrigation recommended!');
  }

  // ---- IRRIGATION ----
  if (has(q, ['irrigat','sinchai','paani','water','seench','pani de','pani do',
              'watering','sprinkler','pump','daalna','dena chahiye','paani dena',
              'should i water','pani daal','pani lagao','seenchai','sinchaayi',
              'सिंचाई', 'पानी', 'सींच', 'इरिगेशन', 'दूं'])) {
    if (avgMoisture >= 60) {
      return hi ? prefixHi + 'abhi irrigation ki zarurat nahi hai. Moisture ' + avgMoisture.toFixed(1) + '% hai, kaafi accha hai!'
                : prefixEn + 'no irrigation needed right now. Moisture is ' + avgMoisture.toFixed(1) + '%, sufficient!';
    } else if (avgMoisture >= 30) {
      return hi ? prefixHi + 'moisture ' + avgMoisture.toFixed(1) + '% hai. Halka paani de sakte hain agar agle 2 din barish ka anumaan nahi hai.'
                : prefixEn + 'moisture is ' + avgMoisture.toFixed(1) + '%. Light irrigation suggested if no rain is expected in 2 days.';
    } else {
      return hi ? prefixHi + 'haan! Turant irrigation karein! Mitti ka moisture sirf ' + avgMoisture.toFixed(1) + '% hai, bahut kam hai!'
                : prefixEn + 'yes! Irrigate immediately! Soil moisture is only ' + avgMoisture.toFixed(1) + '%, critically low!';
    }
  }

  // ---- pH ----
  if (has(q, ['ph','amla','kshaar','acidic','alkaline','tezaab','khaar',
              'ph level','ph kitna','ph kya','soil ph','ph value','acidity',
              'ph reading','ph sensor','aml','kshar', 'पीएच', 'अम्ल', 'क्षार'])) {
    let phStatus = avgPh < 5.5 ? (hi?'Mitti acidic hai':'Soil is acidic') : avgPh > 7.5 ? (hi?'Mitti alkaline hai':'Soil is alkaline') : (hi?'pH bilkul sahi range mein hai':'pH is in the ideal range');
    if (hi) return prefixHi + 'mitti ka pH level ' + avgPh.toFixed(1) + ' hai. ' + phStatus + '. ' + (avgPh<5.5?'Lime yaani chuna milayein pH badhane ke liye.':avgPh>7.5?'Gypsum ya sulphur milayein pH kam karne ke liye.':'Koi correction ki zarurat nahi!');
    return prefixEn + 'soil pH is ' + avgPh.toFixed(1) + '. ' + phStatus + '. ' + (avgPh<5.5?'Add lime to raise pH.':avgPh>7.5?'Add gypsum or sulphur to lower pH.':'No correction needed!');
  }

  // ---- NPK / NUTRIENTS / FERTILIZER ----
  if (has(q, ['npk','nitrogen','phospho','potass','khad','urea','nutrient','tatva',
              'dap','fertiliz','compost','n p k','naitrojan','fosfor',
              'potaash','khad ki','khad daal','fertiliser','manure', 
              'खाद', 'यूरिया', 'नाइट्रोजन', 'फास्फोरस', 'पोटेशियम', 'तत्व', 'उर्वरक'])) {
    if (hi) return prefixHi + 'NPK analysis: Nitrogen (N) ' + avgN.toFixed(0) + ' mg/kg ' + (avgN>300?'(Zyada)':'(Theek)') + ', Phosphorus (P) ' + avgP.toFixed(0) + ' mg/kg ' + (avgP>300?'(Zyada)':'(Theek)') + ', Potassium (K) ' + avgK.toFixed(0) + ' mg/kg ' + (avgK>300?'(Zyada)':'(Theek)') + '. ' + (avgN>300||avgP>300||avgK>300?'Kuch nutrients zyada hain, khad kam karein.':'Sab nutrients balance mein hain!');
    return prefixEn + 'NPK analysis: Nitrogen (N) ' + avgN.toFixed(0) + ' mg/kg ' + (avgN>300?'(Excess)':'(OK)') + ', Phosphorus (P) ' + avgP.toFixed(0) + ' mg/kg ' + (avgP>300?'(Excess)':'(OK)') + ', Potassium (K) ' + avgK.toFixed(0) + ' mg/kg ' + (avgK>300?'(Excess)':'(OK)') + '. ' + (avgN>300||avgP>300||avgK>300?'Some nutrients are in excess, reduce fertilizer.':'All nutrients are balanced!');
  }

  // ---- TEMPERATURE / HUMIDITY ----
  if (has(q, ['temp','tapman','garmi','sardi','thanda','humidity','ardrata',
              'temperature','taapman','thand','garam','kitni garmi','kitni thand',
              'degree','celsius','humid','nemee','hum ','current temp',
              'weather temp','aaj kitna','kitna tap', 'तापमान', 'गर्मी', 'सर्दी', 'ठंड', 'आर्द्रता'])) {
    if (hi) return 'Abhi aasa paas ka temperature ' + temp.toFixed(1) + ' degree Celsius hai aur humidity ' + hum.toFixed(1) + '% hai. ' + (temp>40?'Bahut garmi hai, faslon ko pani dein!':temp<10?'Thand hai, frost se faslon ko bachayein.':'Mausam kaafi accha hai faslon ke liye.');
    return 'Current ambient temperature is ' + temp.toFixed(1) + ' degrees Celsius, humidity is ' + hum.toFixed(1) + '%. ' + (temp>40?'Very hot, water your crops!':temp<10?'Cold, protect crops from frost.':'Weather is good for crops.');
  }

  // ---- WEATHER ----
  if (has(q, ['mausam','weather','barish','rain','dhoop','cloud','badal',
              'toofan','storm','forecast','prediction','kaisa mausam',
              'kaisa rahega','hawa','wind','baarish','varsha','megh', 'मौसम', 'बारिश', 'वर्षा', 'धूप', 'बादल'])) {
    const weather = d.weather || 'Unknown';
    if (hi) return 'Abhi temperature ' + temp.toFixed(1) + ' degree hai aur humidity ' + hum.toFixed(1) + '% hai. ' + (day?'Din ka waqt hai.':'Raat hai.') + ' Anumaan: ' + weather + '. ' + (hum>80?'Barish ka anumaan hai, irrigation roko!':'Barish ka anumaan nahi.');
    return 'Temperature: ' + temp.toFixed(1) + ' C, Humidity: ' + hum.toFixed(1) + '%. ' + (day?'Daytime.':'Nighttime.') + ' Prediction: ' + weather + '. ' + (hum>80?'Rain likely, hold off irrigation!':'No rain expected.');
  }

  // ---- AIR QUALITY ----
  if (has(q, ['air','hawa','aqi','pradushan','pollution','gas','quality of air',
              'air quality','vayu','vaayu','pradooshan','smell','badboo',
              'gand','dhuaan','smoke','carbon', 'हवा', 'प्रदूषण', 'वायु', 'गैस'])) {
    if (hi) return 'Hawa ki quality (AQI) ' + aqiPct + '% kharab hai. ' + (aqiPct<=25?'Hawa bilkul saaf hai!':aqiPct<=50?'Hawa theek hai, moderate level.':'Hawa ki quality kharab hai, dhyaan rakhein!');
    return 'Air quality (AQI) metric is ' + aqiPct + '%. ' + (aqiPct<=25?'Air quality is clean!':aqiPct<=50?'Air quality is moderate.':'Air quality is poor, take precautions!');
  }

  // ---- BIGGEST PROBLEM ----
  if (has(q, ['problem','samasya','dikkat','issue','kharab','flag','trouble',
              'sabse badi','sabse bada','biggest','main issue','kya galat',
              'kya problem','koi dikkat','koi problem','kuch gadbad',
              'attention','warning','alert','khatra','danger','risk', 'समस्या', 'दिक्कत', 'खराब', 'खतरा', 'गड़बड़'])) {
    let problems = [];
    if (avgMoisture < 30) problems.push(hi ? 'Moisture bahut kam hai (' + avgMoisture.toFixed(1) + '%), turant paani dein' : 'Moisture critically low (' + avgMoisture.toFixed(1) + '%), irrigate now');
    if (avgPh < 5.5) problems.push(hi ? 'pH acidic hai (' + avgPh.toFixed(1) + '), chuna milayein' : 'pH is acidic (' + avgPh.toFixed(1) + '), add lime');
    if (avgPh > 7.5) problems.push(hi ? 'pH alkaline hai (' + avgPh.toFixed(1) + '), gypsum milayein' : 'pH is alkaline (' + avgPh.toFixed(1) + '), add gypsum');
    if (avgN > 300) problems.push(hi ? 'Nitrogen zyada hai (' + avgN.toFixed(0) + ' mg/kg), urea kam karein' : 'Excess Nitrogen (' + avgN.toFixed(0) + ' mg/kg), reduce urea');
    if (avgP > 300) problems.push(hi ? 'Phosphorus zyada hai (' + avgP.toFixed(0) + ' mg/kg)' : 'Excess Phosphorus (' + avgP.toFixed(0) + ' mg/kg)');
    if (avgK > 300) problems.push(hi ? 'Potassium zyada hai (' + avgK.toFixed(0) + ' mg/kg)' : 'Excess Potassium (' + avgK.toFixed(0) + ' mg/kg)');
    if (temp > 40) problems.push(hi ? 'Temperature bahut zyada hai (' + temp.toFixed(1) + ' degree)' : 'Ambient temperature too high (' + temp.toFixed(1) + ' C)');
    if (aqiPct > 50) problems.push(hi ? 'Hawa ki quality kharab hai (' + aqiPct + '%)' : 'Poor air quality (' + aqiPct + '%)');

    if (problems.length === 0) {
      return hi ? 'Field data ke anusaar abhi koi badi problem nahi dikhti! Sab theek hai.' : 'Based on field data, no major problems detected right now! Everything looks good.';
    }
    return (hi ? 'Field data ke anusaar yeh problems detect hui hain: ' : 'Based on field data, these problems were detected: ') + problems.join('. ');
  }

  // ---- CROP SUGGESTION ----
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
  }

  // ---- SURVEY / RESULTS ----
  if (has(q, ['survey','result','mapping','sample','record','data','report',
              'collect','kitne sample','kitna data','field result',
              'jaanch','janch','parchi','report dikhao','natija', 'सर्वे', 'नतीजा', 'रिपोर्ट'])) {
    if (samples.length === 0) {
      return hi ? 'Abhi tak koi field survey nahi hua. Pehle Auto Mapping tab se survey chalayein.' : 'No field survey data yet. Please run a survey from the Auto Mapping tab.';
    }
    if (hi) return 'Total ' + samples.length + ' samples liye gaye hain. Average moisture ' + avgMoisture.toFixed(1) + '% hai. Field Results tab mein detail dekhein!';
    return samples.length + ' samples collected. Average moisture is ' + avgMoisture.toFixed(1) + '%. See detailed analysis in the Field Results tab!';
  }

  // ---- HELLO / GREETING ----
  if (has(q, ['hello','namaste','hi ','hey','namaskar','kaise ho','how are',
              'good morning','good evening','suprabhat','shubh','pranam',
              'sat sri akal','vanakkam','namaskara', 'नमस्ते', 'नमस्कार', 'प्रणाम'])) {
    if (hi) return 'Namaste! Main Agro-Bot hoon. Aapki field ke baare mein kuch bhi poochiye, jaise irrigation, fasal, mausam, ya nutrients. Main aapke data ka analysis karke bataunga!';
    return 'Hello! I am Agro-Bot. Ask me anything about your field like irrigation, crops, weather, or nutrients. I will analyze your data and answer!';
  }

  // ---- DEFAULT ----
  if (hi) return 'Aapki field ka data: Temperature ' + temp.toFixed(1) + ' degree, Moisture ' + avgMoisture.toFixed(1) + '%, pH ' + avgPh.toFixed(1) + '. Aap pooch sakte hain: Kya mujhe irrigation karni chahiye? ya Kaun si fasal lagaye?';
  return 'Your field data: Temp ' + temp.toFixed(1) + ' C, Moisture ' + avgMoisture.toFixed(1) + '%, pH ' + avgPh.toFixed(1) + '. You can ask: Should I irrigate? or What crops should I plant?';
}

function addChatBubble(text, who) {
  const area = document.getElementById('chatArea');
  const div = document.createElement('div');
  div.className = 'chat-bubble ' + who;
  const nameLabel = who === 'user' ? 'You' : 'Agro-Bot';
  div.innerHTML = '<div class="chat-name">' + nameLabel + '</div><div class="chat-text">' + text.replace(/\n/g,'<br>') + '</div>';
  area.appendChild(div);
  area.scrollTop = area.scrollHeight;
}

function processQuestion(question) {
  addChatBubble(question, 'user');
  const answer = getAgrobotAnswer(question);
  setTimeout(function() {
    addChatBubble(answer, 'bot');
    speakAnswer(answer);
  }, 300);
}

function speakAnswer(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  let clean = text.replace(/<[^>]*>/g, '');
  clean = clean.replace(/[\u{1F300}-\u{1FAD6}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}\u{1F900}-\u{1F9FF}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]/gu, '');
  clean = clean.trim();
  if (!clean) return;
  
  const lang = document.getElementById('voiceLang').value;
  const sentences = clean.split(/[.!?]+/).filter(function(s) { return s.trim().length > 0; });
  
  let delay = 0;
  sentences.forEach(function(sentence, idx) {
    setTimeout(function() {
      const utter = new SpeechSynthesisUtterance(sentence.trim());
      utter.lang = lang;
      utter.rate = 0.95; 
      utter.pitch = 1.0;
      
      const voices = window.speechSynthesis.getVoices();
      if (voices.length > 0) {
        // Prefer Google native voices for higher quality
        let match = voices.find(function(v) { return v.lang === lang && v.name.includes('Google'); });
        if (!match) match = voices.find(function(v) { return v.lang.startsWith(lang.split('-')[0]) && v.name.includes('Google'); });
        if (!match) match = voices.find(function(v) { return v.lang === lang; });
        if (match) utter.voice = match;
      }
      
      window.speechSynthesis.speak(utter);
    }, delay);
    delay += 200; // Increase stagger to prevent speech overlap bugs
  });
}

function toggleVoice() {
  if (isListening) {
    stopListening();
    return;
  }
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    addChatBubble('Voice recognition is not supported in this browser. Please use Google Chrome, or type your question.', 'bot');
    return;
  }
  startListening();
}

function startListening() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = document.getElementById('voiceLang').value;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.continuous = false;

  recognition.onstart = function() {
    isListening = true;
    document.getElementById('micBtn').classList.add('listening');
    document.getElementById('micBtn').innerHTML = '&#9209;';
    document.getElementById('micStatus').textContent = 'Listening... Speak now';
    document.getElementById('waveWrap').style.display = 'flex';
  };

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    processQuestion(transcript);
  };

  recognition.onerror = function(event) {
    stopListening();
    if (event.error === 'no-speech') {
      // Don't clutter chat with errors
    }
  };

  recognition.onend = function() {
    stopListening();
  };

  recognition.start();
}

function stopListening() {
  isListening = false;
  if (recognition) { try { recognition.stop(); } catch(e){} }
  document.getElementById('micBtn').classList.remove('listening');
  document.getElementById('micBtn').innerHTML = '&#127908;';
  document.getElementById('micStatus').textContent = 'Tap to speak';
  document.getElementById('waveWrap').style.display = 'none';
}

function sendTextQuestion() {
  const inp = document.getElementById('textInput');
  const q = inp.value.trim();
  if (!q) return;
  inp.value = '';
  processQuestion(q);
}

function askQuick(question) {
  processQuestion(question);
}

function clearChat() {
  const area = document.getElementById('chatArea');
  area.innerHTML = '<div class="chat-bubble bot"><div class="chat-name">Agro-Bot</div><div class="chat-text">Chat clear ho gaya. Naya sawaal poochiye!</div></div>';
}

if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() { voicesLoaded = true; window.speechSynthesis.getVoices(); };
  setTimeout(function() { window.speechSynthesis.getVoices(); }, 500);
}
"""

text = text[:start] + new_js + text[end:]

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied successfully.")
