import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# ============================================================
# 1. ADD TAB BUTTON (after Field Results tab)
# ============================================================
old_tab = """      <button class="tab" onclick="switchTab(5,this)" id="tab5">
        <span class="tab-icon">📋</span>
        <span class="tab-label-text">Field Results</span>
      </button>
    </div>"""

new_tab = """      <button class="tab" onclick="switchTab(5,this)" id="tab5">
        <span class="tab-icon">📋</span>
        <span class="tab-label-text">Field Results</span>
      </button>
      <button class="tab" onclick="switchTab(6,this)" id="tab6">
        <span class="tab-icon">🎙️</span>
        <span class="tab-label-text">Ask Agro-Bot</span>
      </button>
    </div>"""

text = text.replace(old_tab, new_tab)

# ============================================================
# 2. ADD PAGE 6 HTML (before </main>)
# ============================================================
page6_html = """
      <!-- ======== PAGE 6 — ASK AGRO-BOT (Voice Assistant) ======== -->
      <div class="page" id="page6">
        <div class="section-card" style="text-align:center;padding:32px 20px 24px;">
          <div style="font-size:2.5rem;margin-bottom:8px">🎙️</div>
          <h2 style="margin:0 0 6px;font-size:1.4rem;font-weight:700;color:var(--text-primary)">Ask Agro-Bot</h2>
          <p style="color:var(--text-muted);font-size:0.85rem;max-width:520px;margin:0 auto 18px;">
            Press the microphone and ask any question about your field — in <b>Hindi</b>, <b>English</b>, or <b>Hinglish</b>.<br>
            Agro-Bot will answer using your real-time sensor data.
          </p>

          <!-- Language selector -->
          <div style="margin-bottom:18px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <label style="color:var(--text-muted);font-size:0.82rem;align-self:center;">Language:</label>
            <select id="voiceLang" style="padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:var(--card-bg);color:var(--text-primary);font-size:0.85rem;">
              <option value="hi-IN">🇮🇳 Hindi (हिन्दी)</option>
              <option value="en-IN">🇬🇧 English (India)</option>
              <option value="en-US">🇺🇸 English (US)</option>
              <option value="pa-IN">ਪੰਜਾਬੀ Punjabi</option>
              <option value="ta-IN">தமிழ் Tamil</option>
              <option value="te-IN">తెలుగు Telugu</option>
              <option value="bn-IN">বাংলা Bengali</option>
              <option value="mr-IN">मराठी Marathi</option>
              <option value="gu-IN">ગુજરાતી Gujarati</option>
              <option value="kn-IN">ಕನ್ನಡ Kannada</option>
            </select>
          </div>

          <!-- Mic Button -->
          <button id="micBtn" onclick="toggleVoice()" style="
            width:90px;height:90px;border-radius:50%;border:none;
            background:linear-gradient(135deg,#16a34a,#15803d);
            color:#fff;font-size:2.2rem;cursor:pointer;
            box-shadow:0 4px 24px rgba(22,163,74,0.35);
            transition:all .25s ease;position:relative;
          ">🎤</button>
          <div id="micStatus" style="margin-top:12px;color:var(--text-muted);font-size:0.82rem;">Tap to speak</div>

          <!-- Waveform animation (visible when listening) -->
          <div id="waveWrap" style="display:none;margin:16px auto 0;width:200px;height:40px;display:none;justify-content:center;align-items:flex-end;gap:3px;">
            <div class="wave-bar" style="animation-delay:0.0s"></div>
            <div class="wave-bar" style="animation-delay:0.1s"></div>
            <div class="wave-bar" style="animation-delay:0.2s"></div>
            <div class="wave-bar" style="animation-delay:0.3s"></div>
            <div class="wave-bar" style="animation-delay:0.4s"></div>
            <div class="wave-bar" style="animation-delay:0.3s"></div>
            <div class="wave-bar" style="animation-delay:0.2s"></div>
            <div class="wave-bar" style="animation-delay:0.1s"></div>
          </div>
        </div>

        <!-- Chat Area -->
        <div class="section-card" style="min-height:320px;padding:20px;">
          <div class="card-header" style="margin-bottom:14px;">
            <span class="card-icon">💬</span>
            <span class="card-title">Conversation</span>
            <button onclick="clearChat()" style="margin-left:auto;background:none;border:1px solid var(--border);color:var(--text-muted);padding:4px 12px;border-radius:6px;font-size:0.75rem;cursor:pointer;">Clear</button>
          </div>
          <div id="chatArea" style="
            max-height:420px;overflow-y:auto;display:flex;flex-direction:column;gap:12px;
            padding:10px;border-radius:10px;background:var(--bg);
          ">
            <div class="chat-bubble bot">
              <div class="chat-name">🤖 Agro-Bot</div>
              <div class="chat-text">Namaste! Main Agro-Bot hoon. Apni field ke baare mein kuch bhi poochiye — mausam, mitti, fasal, paani — main aapke sensors ka data dekhkar jawaab dunga! 🌱</div>
            </div>
          </div>

          <!-- Text fallback input -->
          <div style="display:flex;gap:8px;margin-top:14px;">
            <input id="textInput" type="text" placeholder="Type your question here..." style="
              flex:1;padding:10px 14px;border-radius:10px;border:1px solid var(--border);
              background:var(--card-bg);color:var(--text-primary);font-size:0.88rem;
            " onkeydown="if(event.key==='Enter')sendTextQuestion()">
            <button onclick="sendTextQuestion()" style="
              padding:10px 18px;border-radius:10px;border:none;
              background:var(--accent);color:#fff;font-size:0.88rem;
              cursor:pointer;font-weight:600;
            ">Send</button>
          </div>
        </div>

        <!-- Quick Questions -->
        <div class="section-card" style="padding:20px;">
          <div class="card-header" style="margin-bottom:14px;">
            <span class="card-icon">⚡</span>
            <span class="card-title">Quick Questions</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;">
            <button class="quick-q" onclick="askQuick('Meri field ka moisture level kya hai?')">💧 Moisture level?</button>
            <button class="quick-q" onclick="askQuick('Kya aaj irrigation karni chahiye?')">🚿 Irrigation today?</button>
            <button class="quick-q" onclick="askQuick('Meri mitti ka pH kitna hai?')">🧪 Soil pH?</button>
            <button class="quick-q" onclick="askQuick('Sabse badi problem kya hai?')">⚠️ Biggest problem?</button>
            <button class="quick-q" onclick="askQuick('Kaun si fasal laga sakta hoon?')">🌾 Crop suggestion?</button>
            <button class="quick-q" onclick="askQuick('NPK level kaisa hai?')">🧬 NPK levels?</button>
            <button class="quick-q" onclick="askQuick('Mausam kaisa hai abhi?')">🌤️ Weather now?</button>
            <button class="quick-q" onclick="askQuick('Temperature aur humidity kya hai?')">🌡️ Temp & Humidity?</button>
            <button class="quick-q" onclick="askQuick('Air quality kaisi hai?')">💨 Air Quality?</button>
            <button class="quick-q" onclick="askQuick('Field survey ka result kya hai?')">📊 Survey results?</button>
          </div>
        </div>
      </div>

"""

text = text.replace("    </main>", page6_html + "    </main>")

# ============================================================
# 3. ADD CSS 
# ============================================================
css_block = """
/* ---- Ask Agro-Bot Page ---- */
.wave-bar {
  width:4px; border-radius:4px;
  background:var(--accent);
  animation:waveAnim 0.6s ease-in-out infinite alternate;
}
@keyframes waveAnim {
  0%   { height:6px;  opacity:0.4; }
  100% { height:32px; opacity:1;   }
}
#micBtn.listening {
  background:linear-gradient(135deg,#dc2626,#b91c1c) !important;
  box-shadow:0 0 0 8px rgba(220,38,38,0.18), 0 4px 24px rgba(220,38,38,0.35) !important;
  animation:pulse-mic 1.2s ease-in-out infinite;
}
@keyframes pulse-mic {
  0%,100% { transform:scale(1);   }
  50%     { transform:scale(1.06); }
}
.chat-bubble {
  max-width:85%;padding:12px 16px;border-radius:14px;font-size:0.88rem;line-height:1.5;
}
.chat-bubble.user {
  align-self:flex-end;background:var(--accent);color:#fff;border-bottom-right-radius:4px;
}
.chat-bubble.bot {
  align-self:flex-start;background:var(--card-bg);color:var(--text-primary);
  border:1px solid var(--border);border-bottom-left-radius:4px;
}
.chat-name {
  font-size:0.72rem;font-weight:700;margin-bottom:4px;opacity:0.7;
}
.chat-bubble.user .chat-name { text-align:right; }
.quick-q {
  padding:8px 16px;border-radius:20px;border:1px solid var(--border);
  background:var(--card-bg);color:var(--text-primary);font-size:0.8rem;
  cursor:pointer;transition:all .2s;
}
.quick-q:hover { background:var(--accent);color:#fff;border-color:var(--accent); }

"""

# Insert CSS before the closing </style>
# Find the last </style>
style_close = text.rfind('</style>')
if style_close != -1:
    text = text[:style_close] + css_block + text[style_close:]

# ============================================================
# 4. ADD JS (before the closing </script>)
# ============================================================
js_block = """

// ============================================================
// ASK AGRO-BOT — VOICE ASSISTANT
// ============================================================

let recognition = null;
let isListening = false;

function getAgrobotAnswer(question) {
  const d = lastData || {};
  const q = question.toLowerCase();
  const samples = lastSamples || [];
  const lang = document.getElementById('voiceLang').value;
  const isHindi = lang.startsWith('hi') || lang.startsWith('pa') || lang.startsWith('mr') || lang.startsWith('bn') || lang.startsWith('gu') || lang.startsWith('ta') || lang.startsWith('te') || lang.startsWith('kn');

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
  const sensorStatus = d.sensorStatus || '';
  const aqiPct = Math.round((gas/4095)*100);

  // Moisture
  if (q.match(/moisture|nami|neemi|geela|sukha|dry|wet|paani.*mitti/)) {
    if (isHindi) return `Aapki mitti ka moisture level abhi ${moisture.toFixed(1)}% hai. ${moisture>=60?'Mitti kaafi geeli hai, paani dene ki zarurat nahi.':moisture>=30?'Moisture theek hai, lekin dhyaan rakhein.':'Moisture kam hai — irrigation ki zarurat hai!'}`;
    return `Current soil moisture is ${moisture.toFixed(1)}%. ${moisture>=60?'Soil is well-watered.':moisture>=30?'Moisture is moderate.':'Moisture is low — irrigation recommended!'}`;
  }

  // Irrigation
  if (q.match(/irrigat|sinchai|paani|water.*de|seench/)) {
    if (moisture >= 60) {
      return isHindi ? `Abhi irrigation ki zarurat nahi hai. Moisture ${moisture.toFixed(1)}% hai — kaafi accha hai! 💧` 
                      : `No irrigation needed right now. Moisture is ${moisture.toFixed(1)}% — sufficient! 💧`;
    } else if (moisture >= 30) {
      return isHindi ? `Moisture ${moisture.toFixed(1)}% hai — halka paani de sakte hain agar agle 2 din barish ka anumaan nahi hai.`
                      : `Moisture is ${moisture.toFixed(1)}% — light irrigation suggested if no rain is expected in 2 days.`;
    } else {
      return isHindi ? `Haan! Turant irrigation karein! Mitti ka moisture sirf ${moisture.toFixed(1)}% hai — bahut kam hai. ⚠️`
                      : `Yes! Irrigate immediately! Soil moisture is only ${moisture.toFixed(1)}% — critically low. ⚠️`;
    }
  }

  // pH
  if (q.match(/ph|अम्ल|amla|kshaar|acidic|alkaline/)) {
    let phStatus = ph < 5.5 ? (isHindi?'Mitti acidic hai':'Soil is acidic') : ph > 7.5 ? (isHindi?'Mitti alkaline hai':'Soil is alkaline') : (isHindi?'pH bilkul sahi range mein hai':'pH is in the ideal range');
    if (isHindi) return `Mitti ka pH level ${ph.toFixed(1)} hai. ${phStatus}. ${ph<5.5?'Lime (chuna) milayein pH badhane ke liye.':ph>7.5?'Gypsum ya sulphur milayein pH kam karne ke liye.':'Koi correction ki zarurat nahi! ✅'}`;
    return `Soil pH is ${ph.toFixed(1)}. ${phStatus}. ${ph<5.5?'Add lime to raise pH.':ph>7.5?'Add gypsum or sulphur to lower pH.':'No correction needed! ✅'}`;
  }

  // NPK
  if (q.match(/npk|nitrogen|phospho|potass|khad|urea|nutrient|tatva/)) {
    if (isHindi) return `NPK Reading:\\n🟢 Nitrogen (N): ${n} mg/kg ${n>300?'— Zyada hai':'— Theek hai'}\\n🟡 Phosphorus (P): ${p} mg/kg ${p>300?'— Zyada hai':'— Theek hai'}\\n🔵 Potassium (K): ${k} mg/kg ${k>300?'— Zyada hai':'— Theek hai'}\\n\\n${n>300||p>300||k>300?'Kuch nutrients zyada hain — khad kam karein.':'Sab nutrients balance mein hain! ✅'}`;
    return `NPK Reading:\\n🟢 Nitrogen (N): ${n} mg/kg ${n>300?'— Excess':'— OK'}\\n🟡 Phosphorus (P): ${p} mg/kg ${p>300?'— Excess':'— OK'}\\n🔵 Potassium (K): ${k} mg/kg ${k>300?'— Excess':'— OK'}\\n\\n${n>300||p>300||k>300?'Some nutrients are in excess — reduce fertilizer.':'All nutrients are balanced! ✅'}`;
  }

  // Temperature / Humidity
  if (q.match(/temp|tapman|garmi|sardi|thanda|humidity|ardrata|namee|hum/)) {
    if (isHindi) return `Abhi temperature ${temp.toFixed(1)}°C hai aur humidity ${hum.toFixed(1)}% hai. Atmospheric pressure ${press.toFixed(1)} hPa hai. ${temp>40?'Bahut garmi hai — faslon ko pani dein!':temp<10?'Thand hai — frost se faslon ko bachayein.':'Mausam kaafi accha hai faslon ke liye. ☀️'}`;
    return `Current temperature is ${temp.toFixed(1)}°C, humidity is ${hum.toFixed(1)}%, pressure is ${press.toFixed(1)} hPa. ${temp>40?'Very hot — water your crops!':temp<10?'Cold — protect crops from frost.':'Weather is good for crops. ☀️'}`;
  }

  // Weather
  if (q.match(/mausam|weather|barish|rain|dhoop|cloud/)) {
    const weather = d.weather || 'Unknown';
    if (isHindi) return `Abhi temperature ${temp.toFixed(1)}°C aur humidity ${hum.toFixed(1)}% hai. Pressure ${press.toFixed(1)} hPa. ${day?'Din ka waqt hai ☀️':'Raat hai 🌙'}. Weather prediction: ${weather}. ${hum>80?'Barish ka anumaan hai — irrigation roko!':'Barish ka anumaan nahi, irrigation plan karein.'}`;
    return `Temperature: ${temp.toFixed(1)}°C, Humidity: ${hum.toFixed(1)}%, Pressure: ${press.toFixed(1)} hPa. ${day?'Daytime ☀️':'Nighttime 🌙'}. Prediction: ${weather}. ${hum>80?'Rain likely — hold off irrigation!':'No rain expected.'}`;
  }

  // Air Quality
  if (q.match(/air|hawa|aqi|quality|pradushan|pollution|gas/)) {
    if (isHindi) return `MQ135 sensor reading: ${gas} (${aqiPct}%). ${aqiPct<=25?'Hawa bilkul saaf hai! ✅':aqiPct<=50?'Hawa theek hai — moderate level.':'Hawa ki quality kharab hai — dhyaan rakhein! ⚠️'}`;
    return `MQ135 sensor reading: ${gas} (${aqiPct}%). ${aqiPct<=25?'Air quality is clean! ✅':aqiPct<=50?'Air quality is moderate.':'Air quality is poor — take precautions! ⚠️'}`;
  }

  // Biggest problem
  if (q.match(/problem|samasya|dikkat|issue|kharab|flag|samadhan|fix|trouble/)) {
    let problems = [];
    if (moisture < 30) problems.push(isHindi ? `Moisture bahut kam hai (${moisture.toFixed(1)}%) — turant paani dein` : `Moisture critically low (${moisture.toFixed(1)}%) — irrigate now`);
    if (ph < 5.5) problems.push(isHindi ? `pH acidic hai (${ph.toFixed(1)}) — chuna milayein` : `pH is acidic (${ph.toFixed(1)}) — add lime`);
    if (ph > 7.5) problems.push(isHindi ? `pH alkaline hai (${ph.toFixed(1)}) — gypsum milayein` : `pH is alkaline (${ph.toFixed(1)}) — add gypsum`);
    if (n > 300) problems.push(isHindi ? `Nitrogen zyada hai (${n} mg/kg) — urea kam karein` : `Excess Nitrogen (${n} mg/kg) — reduce urea`);
    if (p > 300) problems.push(isHindi ? `Phosphorus zyada hai (${p} mg/kg)` : `Excess Phosphorus (${p} mg/kg)`);
    if (k > 300) problems.push(isHindi ? `Potassium zyada hai (${k} mg/kg)` : `Excess Potassium (${k} mg/kg)`);
    if (temp > 40) problems.push(isHindi ? `Temperature bahut zyada hai (${temp.toFixed(1)}°C)` : `Temperature too high (${temp.toFixed(1)}°C)`);

    if (problems.length === 0) {
      return isHindi ? 'Aapki field mein abhi koi badi problem nahi dikhti! Sab theek hai. ✅🌱' : 'No major problems detected in your field right now! Everything looks good. ✅🌱';
    }
    return (isHindi ? 'Aapki field mein yeh problems detect hui hain:\\n\\n' : 'The following problems were detected:\\n\\n') + problems.map((p,i) => `${i+1}. ${p}`).join('\\n');
  }

  // Crop suggestion
  if (q.match(/crop|fasal|ugana|laga.*sakt|kya.*boo|seed|beej|suggest.*crop/)) {
    const avgSoilPct = Math.round(moisture);
    const q2 = classifyQuality(avgSoilPct);
    const crops = getCropRecommendations(q2, n, p, k);
    const names = crops.map(c => c.icon + ' ' + c.name).join(', ');
    if (isHindi) return `Aapki mitti ke hisaab se (moisture ${avgSoilPct}%, quality: ${q2.label}), yeh fasle lagayein: ${names}`;
    return `Based on your soil (moisture ${avgSoilPct}%, quality: ${q2.label}), recommended crops: ${names}`;
  }

  // Survey results
  if (q.match(/survey|result|mapping|sample|record|data.*collect/)) {
    if (samples.length === 0) {
      return isHindi ? 'Abhi tak koi field survey nahi hua. Auto Mapping tab se survey shuru karein!' : 'No field survey data yet. Start a survey from the Auto Mapping tab!';
    }
    let sumM=0; samples.forEach(s => sumM += s.moisture);
    const avgM = (sumM/samples.length).toFixed(1);
    if (isHindi) return `Total ${samples.length} samples liye gaye hain. Average moisture ${avgM}% hai. Field Results tab mein detail dekhein! 📊`;
    return `${samples.length} samples collected. Average moisture is ${avgM}%. See detailed analysis in the Field Results tab! 📊`;
  }

  // Day/Night
  if (q.match(/din|raat|day|night|dhoop|andhera|suraj|sun/)) {
    if (isHindi) return day ? 'Abhi din ka waqt hai ☀️ — LDR sensor dhoop detect kar raha hai.' : 'Abhi raat hai 🌙 — LDR sensor andhera detect kar raha hai.';
    return day ? 'It is currently daytime ☀️ — LDR sensor detects sunlight.' : 'It is currently nighttime 🌙 — LDR sensor detects darkness.';
  }

  // Default / catch-all
  if (isHindi) return `Main samajh nahi paya. Aap moisture, pH, NPK, temperature, irrigation, ya fasal ke baare mein pooch sakte hain. Abhi ke sensor values: Temp ${temp.toFixed(1)}°C, Humidity ${hum.toFixed(1)}%, Moisture ${moisture.toFixed(1)}%, pH ${ph.toFixed(1)}.`;
  return `I didn't understand that. You can ask about moisture, pH, NPK, temperature, irrigation, or crops. Current readings: Temp ${temp.toFixed(1)}°C, Humidity ${hum.toFixed(1)}%, Moisture ${moisture.toFixed(1)}%, pH ${ph.toFixed(1)}.`;
}

function addChatBubble(text, who) {
  const area = document.getElementById('chatArea');
  const div = document.createElement('div');
  div.className = 'chat-bubble ' + who;
  const nameLabel = who === 'user' ? '👨‍🌾 You' : '🤖 Agro-Bot';
  div.innerHTML = '<div class="chat-name">' + nameLabel + '</div><div class="chat-text">' + text.replace(/\\n/g,'<br>') + '</div>';
  area.appendChild(div);
  area.scrollTop = area.scrollHeight;
}

function processQuestion(question) {
  addChatBubble(question, 'user');
  const answer = getAgrobotAnswer(question);
  setTimeout(() => {
    addChatBubble(answer, 'bot');
    speakAnswer(answer);
  }, 400);
}

function speakAnswer(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text.replace(/<[^>]*>/g,'').replace(/\\n/g,' '));
  const lang = document.getElementById('voiceLang').value;
  utter.lang = lang;
  utter.rate = 0.95;
  utter.pitch = 1.0;
  // Try to find a matching voice
  const voices = window.speechSynthesis.getVoices();
  const match = voices.find(v => v.lang.startsWith(lang.split('-')[0]));
  if (match) utter.voice = match;
  window.speechSynthesis.speak(utter);
}

function toggleVoice() {
  if (isListening) {
    stopListening();
    return;
  }
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    addChatBubble('Voice recognition is not supported in your browser. Use Chrome for best results, or type your question below.', 'bot');
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

  recognition.onstart = () => {
    isListening = true;
    document.getElementById('micBtn').classList.add('listening');
    document.getElementById('micBtn').textContent = '⏹';
    document.getElementById('micStatus').textContent = 'Listening... Speak now';
    document.getElementById('waveWrap').style.display = 'flex';
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    processQuestion(transcript);
  };

  recognition.onerror = (event) => {
    stopListening();
    if (event.error === 'no-speech') {
      addChatBubble('Koi awaaz nahi aayi. Phir se try karein! 🎤', 'bot');
    } else if (event.error === 'not-allowed') {
      addChatBubble('Microphone access denied. Please allow microphone permission in your browser settings.', 'bot');
    }
  };

  recognition.onend = () => {
    stopListening();
  };

  recognition.start();
}

function stopListening() {
  isListening = false;
  if (recognition) { try { recognition.stop(); } catch(e){} }
  document.getElementById('micBtn').classList.remove('listening');
  document.getElementById('micBtn').textContent = '🎤';
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
  area.innerHTML = '<div class="chat-bubble bot"><div class="chat-name">🤖 Agro-Bot</div><div class="chat-text">Chat clear ho gaya. Naya sawaal poochiye! 🌱</div></div>';
}

// Pre-load voices
if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = () => { window.speechSynthesis.getVoices(); };
}

"""

# Find the closing </script> and insert before it
script_close = text.rfind('</script>')
if script_close != -1:
    text = text[:script_close] + js_block + text[script_close:]

with open('dashboard/v1.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added Ask Agro-Bot tab successfully!")
