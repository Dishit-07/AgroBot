import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find and replace the entire Agro-Bot JS block
start_marker = '// ============================================================\n// ASK AGRO-BOT'
# Also try with \r\n
start = text.find(start_marker)
if start == -1:
    start_marker = '// ============================================================\r\n// ASK AGRO-BOT'
    start = text.find(start_marker)

end_marker = "// Pre-load voices"
end = text.find(end_marker, start)
if end != -1:
    # Find the end of the pre-load voices block
    end = text.find('</script>', end)

print(f"Start: {start}, End: {end}")
if start == -1 or end == -1:
    print("ERROR: Could not find JS block")
    sys.exit(1)

new_js = r"""// ============================================================
// ASK AGRO-BOT — VOICE ASSISTANT (v2 — Robust)
// ============================================================

let recognition = null;
let isListening = false;
let voicesLoaded = false;

// ---- Keyword matching engine ----
function has(q, keywords) {
  // Returns true if the question contains ANY of the keywords
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

  const temp = d.temp || 0;
  const hum  = d.hum  || 0;
  const press = d.press || 0;
  const gas  = d.gas || 0;
  const moisture = d.soilMoisture || 0;
  const ph   = d.ph || 0;
  const n    = d.nitrogen || 0;
  const p    = d.phosphorus || 0;
  const k    = d.potassium || 0;
  const day  = d.day;
  const aqiPct = Math.round((gas/4095)*100);

  // ---- MOISTURE ----
  if (has(q, ['moisture','nami','neemi','geela','sukha','dry','wet','mitti','soil moisture',
              'paani mitti','kitna geela','kitni nami','moisture level','nam','nami','nemee',
              'moist','water level','soil water','pani','jal'])) {
    if (hi) return 'Aapki mitti ka moisture level abhi ' + moisture.toFixed(1) + '% hai. ' + (moisture>=60?'Mitti kaafi geeli hai, paani dene ki zarurat nahi.':moisture>=30?'Moisture theek hai, lekin dhyaan rakhein.':'Moisture kam hai, irrigation ki zarurat hai!');
    return 'Current soil moisture is ' + moisture.toFixed(1) + '%. ' + (moisture>=60?'Soil is well-watered, no irrigation needed.':moisture>=30?'Moisture is moderate.':'Moisture is low, irrigation recommended!');
  }

  // ---- IRRIGATION ----
  if (has(q, ['irrigat','sinchai','paani','water','seench','pani de','pani do',
              'irrigation','watering','sprinkler','pump','bund','daalna','dena chahiye',
              'paani dena','paani daalna','should i water','pani daal','pani lagao',
              'seenchai','sinchaayi'])) {
    if (moisture >= 60) {
      return hi ? 'Abhi irrigation ki zarurat nahi hai. Moisture ' + moisture.toFixed(1) + '% hai, kaafi accha hai!'
                : 'No irrigation needed right now. Moisture is ' + moisture.toFixed(1) + '%, sufficient!';
    } else if (moisture >= 30) {
      return hi ? 'Moisture ' + moisture.toFixed(1) + '% hai. Halka paani de sakte hain agar agle 2 din barish ka anumaan nahi hai.'
                : 'Moisture is ' + moisture.toFixed(1) + '%. Light irrigation suggested if no rain is expected in 2 days.';
    } else {
      return hi ? 'Haan! Turant irrigation karein! Mitti ka moisture sirf ' + moisture.toFixed(1) + '% hai, bahut kam hai!'
                : 'Yes! Irrigate immediately! Soil moisture is only ' + moisture.toFixed(1) + '%, critically low!';
    }
  }

  // ---- pH ----
  if (has(q, ['ph','amla','kshaar','acidic','alkaline','tezaab','khaar',
              'ph level','ph kitna','ph kya','soil ph','ph value','acidity',
              'ph reading','ph sensor','aml','kshar'])) {
    let phStatus = ph < 5.5 ? (hi?'Mitti acidic hai':'Soil is acidic') : ph > 7.5 ? (hi?'Mitti alkaline hai':'Soil is alkaline') : (hi?'pH bilkul sahi range mein hai':'pH is in the ideal range');
    if (hi) return 'Mitti ka pH level ' + ph.toFixed(1) + ' hai. ' + phStatus + '. ' + (ph<5.5?'Lime yaani chuna milayein pH badhane ke liye.':ph>7.5?'Gypsum ya sulphur milayein pH kam karne ke liye.':'Koi correction ki zarurat nahi!');
    return 'Soil pH is ' + ph.toFixed(1) + '. ' + phStatus + '. ' + (ph<5.5?'Add lime to raise pH.':ph>7.5?'Add gypsum or sulphur to lower pH.':'No correction needed!');
  }

  // ---- NPK / NUTRIENTS / FERTILIZER ----
  if (has(q, ['npk','nitrogen','phospho','potass','khad','urea','nutrient','tatva',
              'dap','fertiliz','compost','nutrients','n p k','naitrojan','fosfor',
              'potaash','khad ki','khad daal','fertiliser','manure'])) {
    if (hi) return 'NPK Reading: Nitrogen (N) ' + n + ' mg/kg ' + (n>300?'zyada hai':'theek hai') + ', Phosphorus (P) ' + p + ' mg/kg ' + (p>300?'zyada hai':'theek hai') + ', Potassium (K) ' + k + ' mg/kg ' + (k>300?'zyada hai':'theek hai') + '. ' + (n>300||p>300||k>300?'Kuch nutrients zyada hain, khad kam karein.':'Sab nutrients balance mein hain!');
    return 'NPK Reading: Nitrogen (N) ' + n + ' mg/kg ' + (n>300?'Excess':'OK') + ', Phosphorus (P) ' + p + ' mg/kg ' + (p>300?'Excess':'OK') + ', Potassium (K) ' + k + ' mg/kg ' + (k>300?'Excess':'OK') + '. ' + (n>300||p>300||k>300?'Some nutrients are in excess, reduce fertilizer.':'All nutrients are balanced!');
  }

  // ---- TEMPERATURE / HUMIDITY ----
  if (has(q, ['temp','tapman','garmi','sardi','thanda','humidity','ardrata',
              'temperature','taapman','thand','garam','kitni garmi','kitni thand',
              'degree','celsius','humid','nemee','hum ','current temp',
              'weather temp','aaj kitna','kitna tap'])) {
    if (hi) return 'Abhi temperature ' + temp.toFixed(1) + ' degree Celsius hai aur humidity ' + hum.toFixed(1) + '% hai. Atmospheric pressure ' + press.toFixed(1) + ' hPa hai. ' + (temp>40?'Bahut garmi hai, faslon ko pani dein!':temp<10?'Thand hai, frost se faslon ko bachayein.':'Mausam kaafi accha hai faslon ke liye.');
    return 'Current temperature is ' + temp.toFixed(1) + ' degrees Celsius, humidity is ' + hum.toFixed(1) + '%, pressure is ' + press.toFixed(1) + ' hPa. ' + (temp>40?'Very hot, water your crops!':temp<10?'Cold, protect crops from frost.':'Weather is good for crops.');
  }

  // ---- WEATHER ----
  if (has(q, ['mausam','weather','barish','rain','dhoop','cloud','badal',
              'toofan','storm','forecast','prediction','kaisa mausam',
              'kaisa rahega','hawa','wind','baarish','varsha','megh'])) {
    const weather = d.weather || 'Unknown';
    if (hi) return 'Abhi temperature ' + temp.toFixed(1) + ' degree hai aur humidity ' + hum.toFixed(1) + '% hai. Pressure ' + press.toFixed(1) + ' hPa. ' + (day?'Din ka waqt hai.':'Raat hai.') + ' Weather prediction: ' + weather + '. ' + (hum>80?'Barish ka anumaan hai, irrigation roko!':'Barish ka anumaan nahi.');
    return 'Temperature: ' + temp.toFixed(1) + ' C, Humidity: ' + hum.toFixed(1) + '%, Pressure: ' + press.toFixed(1) + ' hPa. ' + (day?'Daytime.':'Nighttime.') + ' Prediction: ' + weather + '. ' + (hum>80?'Rain likely, hold off irrigation!':'No rain expected.');
  }

  // ---- AIR QUALITY ----
  if (has(q, ['air','hawa','aqi','pradushan','pollution','gas','quality of air',
              'air quality','vayu','vaayu','pradooshan','smell','badboo',
              'gand','dhuaan','smoke','carbon'])) {
    if (hi) return 'MQ135 sensor ki reading ' + gas + ' hai, yaani ' + aqiPct + '%. ' + (aqiPct<=25?'Hawa bilkul saaf hai!':aqiPct<=50?'Hawa theek hai, moderate level.':'Hawa ki quality kharab hai, dhyaan rakhein!');
    return 'MQ135 sensor reading is ' + gas + ', which is ' + aqiPct + '%. ' + (aqiPct<=25?'Air quality is clean!':aqiPct<=50?'Air quality is moderate.':'Air quality is poor, take precautions!');
  }

  // ---- BIGGEST PROBLEM ----
  if (has(q, ['problem','samasya','dikkat','issue','kharab','flag','trouble',
              'sabse badi','sabse bada','biggest','main issue','kya galat',
              'kya problem','koi dikkat','koi problem','kuch gadbad',
              'attention','warning','alert','khatra','danger','risk'])) {
    let problems = [];
    if (moisture < 30) problems.push(hi ? 'Moisture bahut kam hai (' + moisture.toFixed(1) + '%), turant paani dein' : 'Moisture critically low (' + moisture.toFixed(1) + '%), irrigate now');
    if (ph < 5.5) problems.push(hi ? 'pH acidic hai (' + ph.toFixed(1) + '), chuna milayein' : 'pH is acidic (' + ph.toFixed(1) + '), add lime');
    if (ph > 7.5) problems.push(hi ? 'pH alkaline hai (' + ph.toFixed(1) + '), gypsum milayein' : 'pH is alkaline (' + ph.toFixed(1) + '), add gypsum');
    if (n > 300) problems.push(hi ? 'Nitrogen zyada hai (' + n + ' mg/kg), urea kam karein' : 'Excess Nitrogen (' + n + ' mg/kg), reduce urea');
    if (p > 300) problems.push(hi ? 'Phosphorus zyada hai (' + p + ' mg/kg)' : 'Excess Phosphorus (' + p + ' mg/kg)');
    if (k > 300) problems.push(hi ? 'Potassium zyada hai (' + k + ' mg/kg)' : 'Excess Potassium (' + k + ' mg/kg)');
    if (temp > 40) problems.push(hi ? 'Temperature bahut zyada hai (' + temp.toFixed(1) + ' degree)' : 'Temperature too high (' + temp.toFixed(1) + ' C)');
    if (aqiPct > 50) problems.push(hi ? 'Hawa ki quality kharab hai (' + aqiPct + '%)' : 'Poor air quality (' + aqiPct + '%)');

    if (problems.length === 0) {
      return hi ? 'Aapki field mein abhi koi badi problem nahi dikhti! Sab theek hai.' : 'No major problems detected in your field right now! Everything looks good.';
    }
    return (hi ? 'Aapki field mein yeh problems detect hui hain: ' : 'The following problems were detected: ') + problems.join('. ');
  }

  // ---- CROP SUGGESTION ----
  if (has(q, ['crop','fasal','ugana','laga','boo','seed','beej','suggest',
              'kaun si','konsi','kya ugaye','kya lagaye','best crop',
              'farming','kheti','khet','ugayen','lagayen','suitable',
              'recommend','harvest','katai','sowing','buwai','ropai'])) {
    const avgSoilPct = Math.round(moisture);
    const q2 = classifyQuality(avgSoilPct);
    const crops = getCropRecommendations(q2, n, p, k);
    const names = crops.map(function(c) { return c.name; }).join(', ');
    if (hi) return 'Aapki mitti ke hisaab se, moisture ' + avgSoilPct + '% hai, quality ' + q2.label + ' hai. Yeh fasle lagayein: ' + names + '.';
    return 'Based on your soil with moisture ' + avgSoilPct + '% and quality ' + q2.label + ', recommended crops are: ' + names + '.';
  }

  // ---- SURVEY / RESULTS ----
  if (has(q, ['survey','result','mapping','sample','record','data','report',
              'collect','kitne sample','kitna data','field result',
              'jaanch','janch','parchi','report dikhao','natija'])) {
    if (samples.length === 0) {
      return hi ? 'Abhi tak koi field survey nahi hua. Auto Mapping tab se survey shuru karein!' : 'No field survey data yet. Start a survey from the Auto Mapping tab!';
    }
    let sumM=0; samples.forEach(function(s) { sumM += s.moisture; });
    const avgM = (sumM/samples.length).toFixed(1);
    if (hi) return 'Total ' + samples.length + ' samples liye gaye hain. Average moisture ' + avgM + '% hai. Field Results tab mein detail dekhein!';
    return samples.length + ' samples collected. Average moisture is ' + avgM + '%. See detailed analysis in the Field Results tab!';
  }

  // ---- DAY / NIGHT ----
  if (has(q, ['din','raat','day','night','dhoop','andhera','suraj','sun',
              'subah','shaam','dopahar','evening','morning','sunrise','sunset'])) {
    if (hi) return day ? 'Abhi din ka waqt hai, LDR sensor dhoop detect kar raha hai.' : 'Abhi raat hai, LDR sensor andhera detect kar raha hai.';
    return day ? 'It is currently daytime, LDR sensor detects sunlight.' : 'It is currently nighttime, LDR sensor detects darkness.';
  }

  // ---- SENSOR STATUS ----
  if (has(q, ['sensor','status','kaam','working','online','offline','connect',
              'chalu','band','reading','value','kya chal','sab theek',
              'health','check','diagnostic'])) {
    const sensorOk = d.sensorStatus || 'UNKNOWN';
    if (hi) return 'Sensor ka status: SN-3002 ' + sensorOk + '. Temperature ' + temp.toFixed(1) + ' degree, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + ', Air Quality ' + aqiPct + '%. ' + (sensorOk === 'VALID' ? 'Sab sensors sahi kaam kar rahe hain!' : 'SN-3002 sensor mein problem hai, check karein!');
    return 'Sensor status: SN-3002 is ' + sensorOk + '. Temp ' + temp.toFixed(1) + ' C, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + ', AQI ' + aqiPct + '%. ' + (sensorOk === 'VALID' ? 'All sensors are working!' : 'SN-3002 sensor has an issue, please check!');
  }

  // ---- HELLO / GREETING ----
  if (has(q, ['hello','namaste','hi ','hey','namaskar','kaise ho','how are',
              'good morning','good evening','suprabhat','shubh','pranam',
              'sat sri akal','vanakkam','namaskara'])) {
    if (hi) return 'Namaste! Main Agro-Bot hoon. Aapki field ke baare mein kuch bhi poochiye, jaise moisture, pH, fasal, irrigation, mausam, ya NPK. Main aapke sensors ka data dekhkar jawaab dunga!';
    return 'Hello! I am Agro-Bot. Ask me anything about your field like moisture, pH, crops, irrigation, weather, or NPK levels. I will answer using your live sensor data!';
  }

  // ---- HELP ----
  if (has(q, ['help','madad','sahayata','kya pooch','what can','kya kar',
              'kaise use','how to','guide','batao kya','options'])) {
    if (hi) return 'Aap mujhse yeh pooch sakte hain: Moisture level kya hai? Kya irrigation karni chahiye? pH kitna hai? NPK level kaisa hai? Temperature aur humidity? Air quality? Sabse badi problem? Kaun si fasal lagaye? Survey ka result? Mausam kaisa hai?';
    return 'You can ask me: What is the moisture level? Should I irrigate? What is the pH? NPK levels? Temperature and humidity? Air quality? Biggest problem? Crop suggestions? Survey results? Weather conditions?';
  }

  // ---- THANK YOU ----
  if (has(q, ['thank','shukriya','dhanyavaad','dhanyawad','thanks','bahut accha',
              'very good','nice','great','awesome','shabash'])) {
    if (hi) return 'Dhanyavaad! Agar aur koi sawaal ho toh zaroor poochiye. Main hamesha aapki madad ke liye tayyar hoon!';
    return 'You are welcome! Feel free to ask more questions anytime. I am always here to help!';
  }

  // ---- SUMMARY / OVERALL ----
  if (has(q, ['summary','sab batao','overall','poora','sabkuch','everything',
              'complete','all data','all reading','saari reading','full report'])) {
    if (hi) return 'Field ka poora status: Temperature ' + temp.toFixed(1) + ' degree, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + ', Nitrogen ' + n + ' mg/kg, Phosphorus ' + p + ' mg/kg, Potassium ' + k + ' mg/kg, Air Quality ' + aqiPct + '%, Pressure ' + press.toFixed(1) + ' hPa. ' + (day?'Din ka waqt hai.':'Raat hai.');
    return 'Full field status: Temperature ' + temp.toFixed(1) + ' C, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + ', N ' + n + ', P ' + p + ', K ' + k + ' mg/kg, AQI ' + aqiPct + '%, Pressure ' + press.toFixed(1) + ' hPa. ' + (day?'Daytime.':'Nighttime.');
  }

  // ---- DEFAULT: Give a helpful summary instead of "I don't understand" ----
  if (hi) return 'Aapki field ka status: Temperature ' + temp.toFixed(1) + ' degree, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + '. Aap mujhse moisture, pH, NPK, irrigation, fasal, mausam, air quality ke baare mein pooch sakte hain!';
  return 'Your field status: Temperature ' + temp.toFixed(1) + ' C, Humidity ' + hum.toFixed(1) + '%, Moisture ' + moisture.toFixed(1) + '%, pH ' + ph.toFixed(1) + '. You can ask about moisture, pH, NPK, irrigation, crops, weather, or air quality!';
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
  // Stop any ongoing speech
  window.speechSynthesis.cancel();
  
  // Clean text for speech: remove emoji, HTML tags, special chars
  let clean = text.replace(/<[^>]*>/g, '');
  clean = clean.replace(/[\u{1F300}-\u{1FAD6}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}\u{1F900}-\u{1F9FF}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]/gu, '');
  clean = clean.replace(/[!]{2,}/g, '!');
  clean = clean.trim();
  
  if (!clean) return;
  
  const lang = document.getElementById('voiceLang').value;
  
  // Split into sentences for more natural speech
  const sentences = clean.split(/[.!?]+/).filter(function(s) { return s.trim().length > 0; });
  
  let delay = 0;
  sentences.forEach(function(sentence, idx) {
    setTimeout(function() {
      const utter = new SpeechSynthesisUtterance(sentence.trim());
      utter.lang = lang;
      utter.rate = 0.9;
      utter.pitch = 1.0;
      utter.volume = 1.0;
      
      // Try to find a matching voice
      const voices = window.speechSynthesis.getVoices();
      if (voices.length > 0) {
        const langPrefix = lang.split('-')[0];
        let match = voices.find(function(v) { return v.lang === lang; });
        if (!match) match = voices.find(function(v) { return v.lang.startsWith(langPrefix); });
        if (match) utter.voice = match;
      }
      
      window.speechSynthesis.speak(utter);
    }, delay);
    delay += 100; // Small stagger so they queue properly
  });
}

function toggleVoice() {
  if (isListening) {
    stopListening();
    return;
  }
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    addChatBubble('Voice recognition is not supported in this browser. Please use Google Chrome, or type your question below.', 'bot');
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
      addChatBubble(document.getElementById('voiceLang').value.startsWith('hi') ? 'Koi awaaz nahi aayi. Phir se try karein!' : 'No speech detected. Please try again!', 'bot');
    } else if (event.error === 'not-allowed') {
      addChatBubble('Microphone access denied. Please allow microphone permission in browser settings.', 'bot');
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

// Pre-load voices for speech synthesis
if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() { voicesLoaded = true; window.speechSynthesis.getVoices(); };
  // Chrome workaround: voices load async
  setTimeout(function() { window.speechSynthesis.getVoices(); }, 500);
}

"""

text = text[:start] + new_js + text[end:]

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced Agro-Bot JS with v2 successfully!")
