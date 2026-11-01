# -*- coding: utf-8 -*-
"""
Builds the comprehensive UP Agricultural Decision Engine JavaScript module
Location: D:\Graphic hackathon\rover\dashboard\decision_engine.js
"""

import os
import sys

output_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'decision_engine.js')

js_code = r'''/**
 * AGRO-BOT MASTER DECISION INTELLIGENCE ENGINE (v2.0-UP)
 * Regional Specialization: Uttar Pradesh, India
 * 
 * Sources: ICAR (IIWBR, NRRI, IISR, IIPR, CPRI, DOGR, IIVR, DRMR),
 *          State Agricultural Universities (CSAUAT Kanpur, ANDUAT Ayodhya, SVPUAT Meerut),
 *          Department of Agriculture, Government of Uttar Pradesh (Package of Practices 2024).
 * 
 * Complies with Master Specification:
 * - Unverified NPK Sensor Index safeguards
 * - Mode A: Crop Discovery (Explainable Suitability Ranking)
 * - Mode B: Target Crop Soil Gap Analysis & Readiness Plan
 * - Measurement-Based Contextual Irrigation Guidance
 * - Spatial Field Zoning & Multi-Sample Aggregation
 * - Bilingual (English & Hindi) Explainability Chains
 */

// ============================================================================
// 1. UTTAR PRADESH AGRO-CLIMATIC ZONES (9 ZONES - ICAR / PLANNING COMMISSION)
// ============================================================================

const UP_AGRO_ZONES = {
  "UP-Z1": {
    zoneId: "UP-Z1",
    zoneNameEn: "Tarai Zone",
    zoneNameHi: "तराई क्षेत्र",
    districts: ["Bahraich", "Balrampur", "Kheri", "Lakhimpur Kheri", "Pilibhit", "Rampur", "Bareilly", "Siddharthnagar"],
    predominantSoilsEn: "Tarai alluvial, deep silty loam to clay loam, rich in organic matter",
    predominantSoilsHi: "तराई जलोढ़, गहरी दोमट से मटियार दोमट, जीवांश युक्त",
    phRange: [6.2, 7.8],
    challengesEn: "High water table, seasonal waterlogging risk in Kharif, iron chlorosis in rice seedlings",
    challengesHi: "उच्च भूजल स्तर, खरीफ में जलभराव का जोखिम, लौह तत्व की कमी",
    majorCrops: ["Rice", "Sugarcane", "Wheat", "Lentil", "Mustard"]
  },
  "UP-Z2": {
    zoneId: "UP-Z2",
    zoneNameEn: "Western Plain Zone",
    zoneNameHi: "पश्चिमी मैदानी क्षेत्र",
    districts: ["Meerut", "Bulandshahr", "Muzaffarnagar", "Saharanpur", "Baghpat", "Shamli", "Ghaziabad", "Hapur", "Gautam Buddha Nagar"],
    predominantSoilsEn: "Alluvial sandy loam to loam, fertile with high cropping intensity",
    predominantSoilsHi: "जलोढ़ बलुई दोमट से दोमट, उपजाऊ एवं सघन खेती युक्त",
    phRange: [6.5, 8.0],
    challengesEn: "Groundwater depletion, multi-nutrient exhaustion (Zinc, Sulfur), intensive Sugarcane-Wheat rotation pressure",
    challengesHi: "भूजल स्तर में गिरावट, सूक्ष्म पोषक तत्वों (जिंक, सल्फर) की कमी",
    majorCrops: ["Sugarcane", "Wheat", "Mustard", "Potato", "Maize"]
  },
  "UP-Z3": {
    zoneId: "UP-Z3",
    zoneNameEn: "Mid-Western Plain Zone",
    zoneNameHi: "मध्य-पश्चिमी मैदानी क्षेत्र",
    districts: ["Badaun", "Shahjahanpur", "Moradabad", "Bijnor", "Sambhal", "Amroha"],
    predominantSoilsEn: "Alluvial sandy loam to clayey, pockets of saline/alkaline patches",
    predominantSoilsHi: "जलोढ़ बलुई दोमट, कुछ क्षेत्रों में क्षारीयता",
    phRange: [6.5, 8.2],
    challengesEn: "Subsoil plow-pan compaction, declining water tables, localized alkalinity",
    challengesHi: "भूमि की निचली सतह में कठोरता, स्थानीय क्षारीयता",
    majorCrops: ["Wheat", "Sugarcane", "Rice", "Mustard", "Mentha", "Potato"]
  },
  "UP-Z4": {
    zoneId: "UP-Z4",
    zoneNameEn: "South-Western Semi-Arid Zone",
    zoneNameHi: "दक्षिण-पश्चिमी अर्ध-शुष्क क्षेत्र",
    districts: ["Agra", "Mathura", "Aligarh", "Mainpuri", "Firozabad", "Hathras", "Etah", "Kasganj"],
    predominantSoilsEn: "Alluvial with desert influence, sandy to sandy loam, calcareous with kankar subsoil",
    predominantSoilsHi: "रेतीली से बलुई दोमट, चूना युक्त कंकड़ परत",
    phRange: [7.2, 8.8],
    challengesEn: "High soil alkalinity (pH > 8.0), brackish/saline groundwater, low moisture holding capacity",
    challengesHi: "उच्च क्षारीयता (pH > 8.0), खारा भूजल, नमी रोकने की कम क्षमता",
    majorCrops: ["Mustard", "Bajra", "Potato", "Wheat", "Barley"]
  },
  "UP-Z5": {
    zoneId: "UP-Z5",
    zoneNameEn: "Central Plain Zone",
    zoneNameHi: "मध्य मैदानी क्षेत्र",
    districts: ["Kanpur Nagar", "Kanpur Dehat", "Lucknow", "Unnao", "Fatehpur", "Rae Bareli", "Sitapur", "Hardoi", "Farrukhabad", "Kannauj", "Barabanki"],
    predominantSoilsEn: "Alluvial loam, extensive sodic/alkaline soils (Usar) with hard clay pan",
    predominantSoilsHi: "जलोढ़ दोमट, बड़े पैमाने पर ऊसर/सोडिक भूमि की उपस्थिति",
    phRange: [6.8, 8.5],
    challengesEn: "Sodic crusting, poor water infiltration, severe zinc deficiency, nitrogen volatilization",
    challengesHi: "ऊसर पपड़ी, जल रिसाव की कमी, जिंक तत्व की भारी कमी",
    majorCrops: ["Wheat", "Rice", "Potato", "Mustard", "Pigeonpea", "Gram"]
  },
  "UP-Z6": {
    zoneId: "UP-Z6",
    zoneNameEn: "Bundelkhand Zone",
    zoneNameHi: "बुंदेलखंड क्षेत्र",
    districts: ["Jhansi", "Lalitpur", "Jalaun", "Hamirpur", "Mahoba", "Banda", "Chitrakoot"],
    predominantSoilsEn: "Mixed Red & Black soils: Rakar & Tari (light red), Kabar & Mar (deep expansive black clay)",
    predominantSoilsHi: "मिश्रित लाल व काली मिट्टी: राकड़, तरी, काबर एवं मार",
    phRange: [6.0, 7.8],
    challengesEn: "Acute drought susceptibility, high soil erosion, shallow soil depth, hard cracking clay in summer",
    challengesHi: "सूखे का भारी जोखिम, मृदा क्षरण, उथली मिट्टी, गर्मियों में दरारें",
    majorCrops: ["Chickpea", "Lentil", "Sesame", "Mustard", "Wheat", "Sorghum"]
  },
  "UP-Z7": {
    zoneId: "UP-Z7",
    zoneNameEn: "North Eastern Plain Zone",
    zoneNameHi: "उत्तर-पूर्वी मैदानी क्षेत्र",
    districts: ["Gorakhpur", "Deoria", "Basti", "Siddharthnagar", "Maharajganj", "Kushinagar", "Sant Kabir Nagar", "Gonda", "Shravasti"],
    predominantSoilsEn: "Calcareous alluvial (Bhat soils with free CaCO3 > 25%), non-calcareous loam",
    predominantSoilsHi: "चूनायुक्त जलोढ़ (भाट मिट्टी), अत्यधिक कैल्शियम कार्बोनेट युक्त",
    phRange: [7.2, 8.4],
    challengesEn: "Severe phosphorus fixation due to high lime content, monsoon flood susceptibility",
    challengesHi: "चूने के कारण फास्फोरस का स्थिरीकरण (अघुलनशील होना), बाढ़ का खतरा",
    majorCrops: ["Rice", "Sugarcane", "Wheat", "Lentil", "Maize"]
  },
  "UP-Z8": {
    zoneId: "UP-Z8",
    zoneNameEn: "Eastern Plain Zone",
    zoneNameHi: "पूर्वी मैदानी क्षेत्र",
    districts: ["Varanasi", "Jaunpur", "Ghazipur", "Azamgarh", "Ballia", "Ayodhya", "Sultanpur", "Amethi", "Pratapgarh", "Mau", "Chandauli"],
    predominantSoilsEn: "Alluvial sandy loam to clay loam, pockets of sodic and saline patches",
    predominantSoilsHi: "जलोढ़ बलुई दोमट से मटियार दोमट, कुछ क्षारीय क्षेत्र",
    phRange: [6.5, 8.2],
    challengesEn: "Small fragmented land holdings, late wheat sowing after late rice harvest, boron/zinc deficiency",
    challengesHi: "छोटे खेत, धान के बाद गेहूँ की पिछेती बुवाई, बोरान व जिंक की कमी",
    majorCrops: ["Rice", "Wheat", "Pigeonpea", "Mustard", "Tomato", "Chilli"]
  },
  "UP-Z9": {
    zoneId: "UP-Z9",
    zoneNameEn: "Vindhyan Zone",
    zoneNameHi: "विंध्य क्षेत्र",
    districts: ["Mirzapur", "Sonbhadra", "Prayagraj"],
    predominantSoilsEn: "Red gravelly, sandy to clayey, lateritic derived from Vindhyan rocks, undulating terrain",
    predominantSoilsHi: "लाल कंकरीली, बलुई से मटियार, विंध्य चट्टानी मिट्टी",
    phRange: [5.8, 7.2],
    challengesEn: "Undulating rocky terrain, low organic carbon, shallow rooting depth, rain-dependent",
    challengesHi: "उबड़-खाबड़ पथरीली जमीन, जीवांश की कमी, उथली जड़ गहराई, वर्षा पर निर्भरता",
    majorCrops: ["Rice", "Wheat", "Lentil", "Chickpea", "Sesame", "Linseed"]
  }
};

// District to Zone mapping lookup
function getZoneByDistrict(districtName) {
  if (!districtName) return "UP-Z5"; // Default Central Plain
  const dClean = districtName.toLowerCase().trim();
  for (const zoneId in UP_AGRO_ZONES) {
    const zone = UP_AGRO_ZONES[zoneId];
    for (const d of zone.districts) {
      if (dClean.includes(d.toLowerCase()) || d.toLowerCase().includes(dClean)) {
        return zoneId;
      }
    }
  }
  return "UP-Z5";
}


// ============================================================================
// 2. UP CROP KNOWLEDGE BASE (20 VERIFIED PRIORITY CROPS)
// ============================================================================

const UP_CROP_DATABASE = {
  "wheat": {
    cropId: "wheat",
    cropNameEn: "Wheat",
    cropNameHi: "गेहूँ",
    icon: "🌾",
    botanicalName: "Triticum aestivum",
    season: "RABI",
    sowingWindow: {
      startMonth: 11, startDay: 5,
      endMonth: 12, endDay: 15,
      descEn: "05 Nov – 15 Dec (Timely: 15 Nov – 05 Dec; Late: up to 25 Dec)",
      descHi: "05 नवंबर – 15 दिसंबर (समय पर: 15 नव – 05 दिसं; पिछेती: 25 दिसं तक)"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z6", "UP-Z7", "UP-Z8", "UP-Z9"],
    varietiesUP: [
      { name: "HD-2967", type: "Timely Sown", days: "140-145", yieldQ: "50-55" },
      { name: "DBW-187 (Karan Vandana)", type: "High Yielding / Biofortified", days: "120-125", yieldQ: "60-65" },
      { name: "PBW-502", type: "Timely Irrigated", days: "135-140", yieldQ: "52-56" },
      { name: "WH-1105", type: "Rust Resistant", days: "135-140", yieldQ: "55-58" },
      { name: "K-307 (Shatabdi)", type: "UP Recommended", days: "130-135", yieldQ: "48-52" },
      { name: "HD-3086 (Pusa Gautami)", type: "Terminal Heat Tolerant", days: "135-140", yieldQ: "54-58" },
      { name: "WH-1124", type: "Late Sown (Dec)", days: "115-120", yieldQ: "42-45" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.5, 8.2],
      preferredTexture: ["Loam", "Clay Loam", "Sandy Loam"],
      drainageRequirement: "GOOD",
      organicCarbonTarget: "0.50% - 0.75%"
    },
    operationalThresholds: {
      moistureSowingPct: [40.0, 65.0],
      moistureGrowthPct: [45.0, 75.0],
      soilTempSowingC: [18.0, 24.0],
      soilTempGrowthC: [12.0, 28.0],
      ambientTempMaxC: 35.0
    },
    sensorIndexExpectation: {
      nIndexMin: 80,
      pIndexMin: 40,
      kIndexMin: 60,
      note: "Relative sensor index - not certified mg/kg laboratory available nutrients"
    },
    waterManagement: {
      totalWaterReqMm: [400, 500],
      irrigationCount: "4 to 6 irrigations",
      criticalStages: [
        { stageEn: "Crown Root Initiation (CRI)", stageHi: "शिखर जड़ जमाव (CRI)", das: "20-25 DAS", importance: "CRITICAL" },
        { stageEn: "Tillering Stage", stageHi: "कल्ले फूटने की अवस्था", das: "40-45 DAS", importance: "IMPORTANT" },
        { stageEn: "Jointing / Stem Extension", stageHi: "गांठ बनने की अवस्था", das: "60-65 DAS", importance: "IMPORTANT" },
        { stageEn: "Flowering / Booting", stageHi: "फूल आने की अवस्था", das: "80-85 DAS", importance: "CRITICAL" },
        { stageEn: "Milking / Grain Filling", stageHi: "दूधिया / दाना भराव अवस्था", das: "100-105 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "MEDIUM",
      waterloggingSensitivity: "HIGH"
    },
    limitingFactors: [
      {
        conditionEn: "Soil pH Below 5.8 (Acidic)",
        conditionHi: "मिट्टी का pH 5.8 से कम (अम्लीय)",
        threshold: "pH < 5.8",
        impactEn: "Aluminum toxicity, poor root elongation, phosphorus fixation",
        impactHi: "एल्युमीनियम विषाक्तता, जड़ों का कमजोर विकास, फास्फोरस का न मिल पाना",
        actionEn: "Incorporate agricultural lime or dolomite 2-3 weeks before sowing. Confirm dosage with buffer pH lab test.",
        actionHi: "बुवाई से 2-3 सप्ताह पूर्व खेत में कृषि चूना या डोलोमाइट मिलाएं। लैब से बफर जांच करवाएं।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Soil pH Above 8.2 (Alkaline / Sodic)",
        conditionHi: "मिट्टी का pH 8.2 से अधिक (क्षारीय / ऊसर)",
        threshold: "pH > 8.2",
        impactEn: "Micronutrient chlorosis (Zinc/Iron deficiency), seedling mortality, soil crusting",
        impactHi: "जिंक और आयरन की कमी से पीलापन, जमाव में कमी, ऊपरी पपड़ी बनना",
        actionEn: "Apply agricultural gypsum based on Soil Health Card gypsum requirement (GR). Ensure zinc sulfate basal dressing.",
        actionHi: "सॉइल हेल्थ कार्ड की संस्तुति अनुसार जिप्सम डालें। बुवाई में जिंक सल्फेट अवश्य दें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Low Sowing Soil Moisture",
        conditionHi: "बुवाई के समय नमी की कमी",
        threshold: "Moisture < 40%",
        impactEn: "Patchy germination, delayed seedling emergence",
        impactHi: "खराब जमाव, बीजों का न उगना",
        actionEn: "Apply pre-sowing irrigation (Palewa / Rauni) and prepare fine seedbed when moisture is in workable condition (Wapsa).",
        actionHi: "बुवाई से पहले पलेवा (रौनी) करें। ओट (वापसा) आने पर जुताई करके बुवाई करें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Late Sowing Terminal Heat Risk",
        conditionHi: "पिछेती बुवाई में पछुआ हवा व गर्मी का खतरा",
        threshold: "Sowing after 20 Dec",
        impactEn: "Yield loss of 25-35 kg/ha per day delay due to forced maturity in March",
        impactHi: "मार्च की गर्मी से दाना सिकुड़ना, प्रतिदिन 25-35 किग्रा/हेक्टेयर उत्पादन में गिरावट",
        actionEn: "Switch strictly to heat-tolerant late varieties (HD-3086, DBW-187, WH-1124) with 25% higher seed rate.",
        actionHi: "गर्मी सहनशील किस्में (HD-3086, DBW-187) चुनें और बीज दर 25% बढ़ाएं।",
        actionTiming: "AT_SOWING",
        isCritical: false
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIWBR Karnal & CSAUAT Kanpur",
      publication: "Package of Practices for Rabi Crops, Directorate of Agriculture, UP (2024)",
      verified: true
    }
  },

  "rice": {
    cropId: "rice",
    cropNameEn: "Rice / Paddy",
    cropNameHi: "धान (चावल)",
    icon: "🌾",
    botanicalName: "Oryza sativa",
    season: "KHARIF",
    sowingWindow: {
      startMonth: 6, startDay: 15,
      endMonth: 7, endDay: 25,
      descEn: "Nursery: 20 May – 20 Jun; Transplanting: 20 Jun – 25 Jul",
      descHi: "नर्सरी: 20 मई – 20 जून; रोपाई: 20 जून – 25 जुलाई"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z5", "UP-Z7", "UP-Z8", "UP-Z9"],
    varietiesUP: [
      { name: "Sarjoo-52", type: "Medium Duration / Popular Eastern UP", days: "130-135", yieldQ: "50-55" },
      { name: "Pant Dhan-12", type: "Semi-Dwarf High Yielding", days: "120-125", yieldQ: "55-60" },
      { name: "Sambha Sub-1", type: "Submergence / Flood Tolerant (14 days)", days: "140-145", yieldQ: "48-52" },
      { name: "Pusa Basmati 1509", type: "Early Basmati Export", days: "115-120", yieldQ: "45-50" },
      { name: "Pusa Basmati 1121", type: "Premium Long Grain Basmati", days: "140-145", yieldQ: "40-45" },
      { name: "Narendra-359", type: "Blast Resistant Central UP", days: "130-135", yieldQ: "50-55" }
    ],
    soilRequirements: {
      phOptimal: [5.5, 7.0],
      phTolerable: [5.0, 8.2],
      preferredTexture: ["Clay Loam", "Clay", "Silt Loam"],
      drainageRequirement: "WATERLOGGING_TOLERANT",
      organicCarbonTarget: "0.50% - 0.85%"
    },
    operationalThresholds: {
      moistureSowingPct: [70.0, 95.0],
      moistureGrowthPct: [75.0, 100.0],
      soilTempSowingC: [22.0, 32.0],
      soilTempGrowthC: [20.0, 36.0],
      ambientTempMaxC: 40.0
    },
    sensorIndexExpectation: {
      nIndexMin: 70,
      pIndexMin: 35,
      kIndexMin: 50,
      note: "Submerged soil alters redox potential; relative index baseline"
    },
    waterManagement: {
      totalWaterReqMm: [1100, 1400],
      irrigationCount: "Submerged / Alternate Wetting and Drying (AWD)",
      criticalStages: [
        { stageEn: "Seedling Establishment", stageHi: "रोपाई के बाद जड़ पकड़ना", das: "5-10 DAT", importance: "CRITICAL" },
        { stageEn: "Active Tillering", stageHi: "कल्ले निकलने की मुख्य अवस्था", das: "25-35 DAT", importance: "CRITICAL" },
        { stageEn: "Panicle Initiation", stageHi: "बाली बनने की शुरुआत", das: "50-60 DAT", importance: "CRITICAL" },
        { stageEn: "Flowering / Heading", stageHi: "फूल व बाली निकलने की अवस्था", das: "70-80 DAT", importance: "CRITICAL" },
        { stageEn: "Grain Development", stageHi: "दूधिया दाना अवस्था", das: "85-95 DAT", importance: "IMPORTANT" }
      ],
      droughtTolerance: "LOW",
      waterloggingSensitivity: "NONE (Tolerant)"
    },
    limitingFactors: [
      {
        conditionEn: "Soil Moisture Below Puddle Requirement",
        conditionHi: "रोपाई के लिए नमी व पानी की कमी",
        threshold: "Moisture < 65%",
        impactEn: "Failure of puddled transplanting; high weed infestation and percolation loss",
        impactHi: "लेह (पडलिंग) न बन पाना, खरपतवार की भारी समस्या",
        actionEn: "Ensure standing water 3-5 cm or transition to Direct Seeded Rice (DSR) with seed-drill.",
        actionHi: "खेत में 3-5 सेमी पानी रोकें या लेह न होने पर सीधी बिजाई (DSR) तकनीक अपनाएं।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Alkaline / Calcareous Soil Zinc Deficiency",
        conditionHi: "क्षारीय मिट्टी में खैरा रोग (जिंक की कमी)",
        threshold: "pH > 7.5",
        impactEn: "Khaira disease: rusty bronze spots on leaves, severe stunted growth 2-3 weeks after transplanting",
        impactHi: "खैरा रोग: पत्तियों पर कत्थई/तांबई धब्बे, पौधों का बौनापन व पीला पड़ना",
        actionEn: "Apply Zinc Sulfate (21% Zn @ 25 kg/ha or 33% Zn @ 15 kg/ha) as basal dressing. Foliar spray (0.5% ZnSO4 + 2% Urea) if symptoms appear.",
        actionHi: "रोपाई पूर्व 25 किग्रा/हेक्टेयर जिंक सल्फेट डालें। लक्षण आने पर 0.5% जिंक सल्फेट + 2% यूरिया का छिड़काव करें।",
        actionTiming: "AT_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-NRRI Cuttack & ANDUAT Ayodhya",
      publication: "Guidelines for Kharif Rice in Uttar Pradesh (2024)",
      verified: true
    }
  },

  "mustard": {
    cropId: "mustard",
    cropNameEn: "Mustard / Sarson",
    cropNameHi: "सरसों / राई",
    icon: "🌼",
    botanicalName: "Brassica juncea",
    season: "RABI",
    sowingWindow: {
      startMonth: 9, startDay: 25,
      endMonth: 10, endDay: 25,
      descEn: "25 Sep – 25 Oct (Optimum: 01 Oct – 15 Oct)",
      descHi: "25 सितंबर – 25 अक्टूबर (सर्वोत्तम: 01 अक्टूबर – 15 अक्टूबर)"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z6", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Varuna (T-59)", type: "Benchmark UP Variety", days: "125-130", yieldQ: "20-22" },
      { name: "Giriraj", type: "High Oil Content (40%)", days: "125-130", yieldQ: "24-26" },
      { name: "RH-749", type: "High Yielding North India", days: "140-145", yieldQ: "25-28" },
      { name: "Pusa Mustard 25", type: "Early Sown (Sept)", days: "105-110", yieldQ: "18-20" },
      { name: "NRC-HB 101", type: "Hybrid Recommended for UP", days: "120-125", yieldQ: "22-25" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.5, 8.2],
      preferredTexture: ["Sandy Loam", "Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.40% - 0.60%"
    },
    operationalThresholds: {
      moistureSowingPct: [30.0, 55.0],
      moistureGrowthPct: [35.0, 65.0],
      soilTempSowingC: [20.0, 26.0],
      soilTempGrowthC: [14.0, 26.0],
      ambientTempMaxC: 32.0
    },
    sensorIndexExpectation: {
      nIndexMin: 60,
      pIndexMin: 30,
      kIndexMin: 40,
      note: "Sulfur is critical for oil synthesis in Brassica"
    },
    waterManagement: {
      totalWaterReqMm: [250, 350],
      irrigationCount: "2 to 3 irrigations",
      criticalStages: [
        { stageEn: "Pre-flowering / Rosette", stageHi: "फूल आने से ठीक पहले", das: "30-35 DAS", importance: "CRITICAL" },
        { stageEn: "Siliqua / Pod Formation", stageHi: "फलियों में दाना बनते समय", das: "55-65 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "HIGH",
      waterloggingSensitivity: "EXTREME (Sensitive to standing water > 24 hours)"
    },
    limitingFactors: [
      {
        conditionEn: "Excessive Soil Moisture / Poor Drainage",
        conditionHi: "खेत में अत्यधिक नमी या पानी ठहरना",
        threshold: "Moisture > 70%",
        impactEn: "Root asphyxiation, collar rot (Sclerotinia), damping off",
        impactHi: "जड़ सड़न, तना गलन (स्क्लेरोटीनिया), पौधों का गिरना",
        actionEn: "Ensure field drainage channels. Do not sow on poorly drained clay; avoid flood irrigation.",
        actionHi: "खेत में जल निकासी सुनिश्चित करें। मटियार भारी मिट्टी में भारी पानी न दें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Delayed Sowing Aphid Vulnerability",
        conditionHi: "पिछेती बुवाई पर माहू (चेपा) कीट का प्रकोप",
        threshold: "Sowing after 30 Oct",
        impactEn: "Severe mustard aphid (Lipaphis erysimi) infestation during January flowering",
        impactHi: "जनवरी-फरवरी में माहू/चेपा कीट द्वारा रस चूसने से भारी नुकसान",
        actionEn: "Complete sowing before 20 October. If delayed, plan prophylactic neem oil or systemic spray at bud emergence.",
        actionHi: "बुवाई 20 अक्टूबर तक पूरी करें। देर होने पर नीम तेल या अनुशंसित कीटनाशक का पहले से प्रबंध रखें।",
        actionTiming: "AT_SOWING",
        isCritical: false
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-DRMR Bharatpur & SVPUAT Meerut",
      publication: "Mustard Production Technology for Indo-Gangetic Plains (2024)",
      verified: true
    }
  },

  "sugarcane": {
    cropId: "sugarcane",
    cropNameEn: "Sugarcane",
    cropNameHi: "गन्ना",
    icon: "🎋",
    botanicalName: "Saccharum officinarum",
    season: "PERENNIAL",
    sowingWindow: {
      startMonth: 10, startDay: 15,
      endMonth: 3, endDay: 30,
      descEn: "Autumn: 15 Oct – 15 Nov; Spring: 15 Feb – 31 Mar",
      descHi: "शरदकालीन: 15 अक्टूबर – 15 नवंबर; बसंतकालीन: 15 फरवरी – 31 मार्च"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Co-0238 (Karan 4)", type: "High Sugar Wonder Variety (Watch Red Rot)", days: "330-360", yieldQ: "850-950" },
      { name: "Co-0118", type: "Early Maturing / Red Rot Resistant Alternative", days: "300-330", yieldQ: "750-850" },
      { name: "Co-15023", type: "Super Early / High Sucrose Replacement", days: "270-300", yieldQ: "800-900" },
      { name: "Co-98014 (Karan 1)", type: "Mid-Late Robust Ratoon", days: "360-390", yieldQ: "750-800" },
      { name: "CoLk-94184", type: "Waterlogging Tolerant (Tarai / East UP)", days: "330-360", yieldQ: "700-750" }
    ],
    soilRequirements: {
      phOptimal: [6.5, 7.8],
      phTolerable: [5.5, 8.2],
      preferredTexture: ["Deep Loam", "Clay Loam"],
      drainageRequirement: "GOOD",
      organicCarbonTarget: "0.60% - 1.00%"
    },
    operationalThresholds: {
      moistureSowingPct: [60.0, 80.0],
      moistureGrowthPct: [65.0, 85.0],
      soilTempSowingC: [20.0, 32.0],
      soilTempGrowthC: [18.0, 38.0],
      ambientTempMaxC: 44.0
    },
    sensorIndexExpectation: {
      nIndexMin: 90,
      pIndexMin: 50,
      kIndexMin: 80,
      note: "Heavy nutrient and potassium consumer; relative index baseline"
    },
    waterManagement: {
      totalWaterReqMm: [1500, 2200],
      irrigationCount: "8 to 12 irrigations in summer",
      criticalStages: [
        { stageEn: "Germination Phase", stageHi: "जमाव अवस्था (अंकुरण)", das: "0-35 DAP", importance: "CRITICAL" },
        { stageEn: "Formative / Tillering Phase", stageHi: "बेत (कल्ले) फूटने की अवस्था", das: "60-120 DAP", importance: "CRITICAL" },
        { stageEn: "Grand Growth Phase (Summer)", stageHi: "तीव्र वानस्पतिक वृद्धि (ग्रीष्मकाल)", das: "150-240 DAP", importance: "CRITICAL" },
        { stageEn: "Ripening Phase", stageHi: "परिपक्वता व शर्करा निर्माण", das: "270-330 DAP", importance: "IMPORTANT" }
      ],
      droughtTolerance: "MEDIUM",
      waterloggingSensitivity: "MEDIUM (Tolerates temporary submersion with drainage)"
    },
    limitingFactors: [
      {
        conditionEn: "Insufficient Irrigation Water Source",
        conditionHi: "सिंचाई स्रोत (बोरवेल/नहर) की कमी",
        threshold: "Water Source = Rain-fed only",
        impactEn: "Severe yield collapse during hot dry pre-monsoon May-June months",
        impactHi: "मई-जून की तेज धूप व लू में फसल सूख जाना, भारी नुकसान",
        actionEn: "Sugarcane cannot be grown rain-fed in UP. Ensure assured tube-well/canal irrigation or adopt drip fertigation.",
        actionHi: "उत्तर प्रदेश में गन्ने की खेती बिना सुनिश्चित सिंचाई के संभव नहीं है। ड्रिप सिंचाई या पक्का बोरवेल सुनिश्चित करें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Red Rot Vulnerability on Co-0238",
        conditionHi: "Co-0238 में लाल सड़न (रेड रॉट) का भारी खतरा",
        threshold: "Variety = Co-0238 in Red-Rot endemic zones",
        impactEn: "Sudden drying of canes from top; total field loss",
        impactHi: "गन्ने का अंदर से लाल होकर सूख जाना, पूरी फसल का नष्ट होना",
        actionEn: "Do not plant Co-0238 in affected areas. Replace with certified tissue-culture seed of Co-0118, Co-15023, or CoLk-14201.",
        actionHi: "संक्रमित क्षेत्रों में Co-0238 न लगाएं। Co-0118, Co-15023 या नई रोगरोधी किस्मों का प्रमाणित बीज लें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IISR Lucknow & UP Council of Sugarcane Research Shahjahanpur",
      publication: "Sugarcane Production Manual for Uttar Pradesh (2024)",
      verified: true
    }
  },

  "potato": {
    cropId: "potato",
    cropNameEn: "Potato",
    cropNameHi: "आलू",
    icon: "🥔",
    botanicalName: "Solanum tuberosum",
    season: "RABI",
    sowingWindow: {
      startMonth: 10, startDay: 10,
      endMonth: 11, endDay: 5,
      descEn: "10 Oct – 05 Nov (Western UP Early: 25 Sep; Main: 15-25 Oct)",
      descHi: "10 अक्टूबर – 05 नवंबर (पश्चिमी उप्र अगेती: 25 सितं; मुख्य: 15-25 अक्टू)"
    },
    suitableZones: ["UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Kufri Bahar (3797)", type: "Most Popular Main Season UP", days: "100-110", yieldQ: "300-350" },
      { name: "Kufri Pukhraj", type: "Early High Bulk (75-80 days)", days: "75-90", yieldQ: "320-380" },
      { name: "Kufri Chipsona-1", type: "Processing / High Dry Matter", days: "100-110", yieldQ: "280-320" },
      { name: "Kufri Mohan", type: "Frost Tolerant High Yielder", days: "90-100", yieldQ: "350-400" },
      { name: "Kufri Khyati", type: "Early Bulking (60-70 days)", days: "70-80", yieldQ: "250-300" }
    ],
    soilRequirements: {
      phOptimal: [5.2, 6.5],
      phTolerable: [5.0, 7.5],
      preferredTexture: ["Sandy Loam", "Loose Friable Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.60% - 1.00%"
    },
    operationalThresholds: {
      moistureSowingPct: [50.0, 75.0],
      moistureGrowthPct: [60.0, 80.0],
      soilTempSowingC: [16.0, 22.0],
      soilTempGrowthC: [14.0, 24.0],
      ambientTempMaxC: 30.0
    },
    sensorIndexExpectation: {
      nIndexMin: 80,
      pIndexMin: 50,
      kIndexMin: 90,
      note: "High potassium requirement for tuber bulking and starch accumulation"
    },
    waterManagement: {
      totalWaterReqMm: [450, 550],
      irrigationCount: "5 to 7 light irrigations",
      criticalStages: [
        { stageEn: "Stolon / Tuber Initiation", stageHi: "कंद बनने की शुरुआत", das: "20-25 DAS", importance: "CRITICAL" },
        { stageEn: "Tuber Bulking Phase", stageHi: "कंदों के तेजी से फूलने की अवस्था", das: "45-65 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "LOW",
      waterloggingSensitivity: "EXTREME (Rotting occurs within 12 hours of flooding)"
    },
    limitingFactors: [
      {
        conditionEn: "High Soil Temperature at Planting",
        conditionHi: "बुवाई के समय मिट्टी का अधिक तापमान",
        threshold: "Soil Temp > 25°C",
        impactEn: "Seed piece rotting (bacterial soft rot) in soil, poor sprout emergence",
        impactHi: "जमीन में आलू के बीज का सड़ना, अंकुरण का फेल होना",
        actionEn: "Wait until night temperature drops consistently below 20-22°C before planting. Plant in ridges.",
        actionHi: "रात का तापमान 20-22°C से नीचे आने तक प्रतीक्षा करें। मेड़ों पर बुवाई करें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      },
      {
        conditionEn: "Soil pH Above 7.5 (Alkaline Scab Risk)",
        conditionHi: "मिट्टी का pH 7.5 से अधिक (आलू में चेचक/स्कैब रोग)",
        threshold: "pH > 7.5",
        impactEn: "Common scab (Streptomyces scabies) makes tubers disfigured, rough, and unmarketable",
        impactHi: "चेचक (स्कैब) रोग से आलू की त्वचा खुरदरी होना, बाजार मूल्य गिरना",
        actionEn: "Avoid recent liming. Apply sulfur or acidifying fertilizers (Ammonium Sulfate) and maintain consistent moisture during tuber initiation.",
        actionHi: "चूने का प्रयोग बिल्कुल न करें। कंद बनते समय खेत में नमी की कमी न होने दें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-CPRI Shimla & Central Potato Research Station Modipuram (Meerut)",
      publication: "Potato Production Guidelines for Plains of Uttar Pradesh (2024)",
      verified: true
    }
  },

  "chickpea": {
    cropId: "chickpea",
    cropNameEn: "Chickpea / Bengal Gram (चना)",
    cropNameHi: "चना (देसी व काबुली)",
    icon: "🫘",
    botanicalName: "Cicer arietinum",
    season: "RABI",
    sowingWindow: {
      startMonth: 10, startDay: 15,
      endMonth: 11, endDay: 15,
      descEn: "15 Oct – 15 Nov (Optimum: 20 Oct – 05 Nov)",
      descHi: "15 अक्टूबर – 15 नवंबर (सर्वोत्तम: 20 अक्टूबर – 05 नवंबर)"
    },
    suitableZones: ["UP-Z4", "UP-Z5", "UP-Z6", "UP-Z8", "UP-Z9"],
    varietiesUP: [
      { name: "Radhey (K-850)", type: "Large Seeded Bold UP Standard", days: "140-145", yieldQ: "20-25" },
      { name: "Uday (KPG-59)", type: "Wilt Resistant Desi", days: "135-140", yieldQ: "22-26" },
      { name: "Pusa 362", type: "Wide Adaptability", days: "140-145", yieldQ: "22-25" },
      { name: "JAKI-9218", type: "Bundelkhand Special Drought Hardy", days: "115-120", yieldQ: "18-22" },
      { name: "KGD-1168", type: "Kabuli Variety for UP", days: "135-140", yieldQ: "20-24" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.5, 8.2],
      preferredTexture: ["Loam", "Clay Loam (Black Kabar/Mar)", "Sandy Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.35% - 0.60%"
    },
    operationalThresholds: {
      moistureSowingPct: [30.0, 50.0],
      moistureGrowthPct: [30.0, 55.0],
      soilTempSowingC: [18.0, 25.0],
      soilTempGrowthC: [12.0, 26.0],
      ambientTempMaxC: 32.0
    },
    sensorIndexExpectation: {
      nIndexMin: 30,
      pIndexMin: 35,
      kIndexMin: 40,
      note: "Legume fixes atmospheric nitrogen via Rhizobium nodules; requires phosphorus"
    },
    waterManagement: {
      totalWaterReqMm: [250, 350],
      irrigationCount: "1 to 2 light irrigations maximum",
      criticalStages: [
        { stageEn: "Pre-flowering / Branching", stageHi: "शाखाएं निकलते समय (फूल आने से पूर्व)", das: "40-45 DAS", importance: "CRITICAL" },
        { stageEn: "Pod Development", stageHi: "घंटी (फलियों) में दाना भराव", das: "70-75 DAS", importance: "IMPORTANT" }
      ],
      droughtTolerance: "HIGH",
      waterloggingSensitivity: "EXTREME (Flower drop and wilt upon flooding)"
    },
    limitingFactors: [
      {
        conditionEn: "Irrigation at Active Flowering",
        conditionHi: "फूल खिलने के समय पानी देना (गंभीर भूल)",
        threshold: "Watering during flowering stage",
        impactEn: "Massive vegetative overgrowth, 80-90% flower drop, collar rot",
        impactHi: "पौधे का जरूरत से ज्यादा बढ़ना, फूलों का झड़ जाना, फलियां न बनना",
        actionEn: "NEVER irrigate chickpea during full flowering. Give light irrigation only at branching or after pod set.",
        actionHi: "चने में फूल आने पर कभी भी पानी न लगाएं। सिंचाई केवल फूल आने से पहले या दाना बनते समय दें।",
        actionTiming: "STANDING_CROP",
        isCritical: true
      },
      {
        conditionEn: "Fusarium Wilt (उकठा रोग) in Non-Resistant Varieties",
        conditionHi: "उकठा (विल्ट) रोग का खतरा",
        threshold: "Field history of wilt / acidic soil",
        impactEn: "Sudden drooping and drying of plants in patches from seedling to flowering",
        impactHi: "पौधों का अचानक सूख जाना, पूरे खेत में उकठा फैलना",
        actionEn: "Seed treatment with Trichoderma viride (10 g/kg) + Carboxin+Thiram. Use wilt-resistant varieties (Uday, JG-11).",
        actionHi: "ट्राइकोडर्मा (10 ग्राम/किग्रा बीज) से बीजोपचार अवश्य करें। रोगरोधी किस्में (उदय) ही बोएं।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIPR Kanpur",
      publication: "Chickpea Cultivation Guide for Central & Bundelkhand UP (2024)",
      verified: true
    }
  },

  "pigeonpea": {
    cropId: "pigeonpea",
    cropNameEn: "Pigeonpea / Arhar / Tur (अरहर)",
    cropNameHi: "अरहर (तूर)",
    icon: "🫛",
    botanicalName: "Cajanus cajan",
    season: "KHARIF",
    sowingWindow: {
      startMonth: 6, startDay: 15,
      endMonth: 7, endDay: 15,
      descEn: "15 Jun – 15 Jul (Early varieties: by 30 Jun for Wheat rotation)",
      descHi: "15 जून – 15 जुलाई (अगेती किस्में: 30 जून तक ताकि गेहूँ बो सकें)"
    },
    suitableZones: ["UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z6", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "UPAS-120", type: "Early Maturing (Vacates for Wheat)", days: "140-150", yieldQ: "18-22" },
      { name: "Malviya Vikalp (MA-13)", type: "Wilt Resistant Eastern UP", days: "240-260", yieldQ: "25-28" },
      { name: "Narendra Arhar-1", type: "High Yielding UP State Release", days: "240-250", yieldQ: "24-28" },
      { name: "Paras", type: "Early Maturing Short Duration", days: "135-140", yieldQ: "16-20" },
      { name: "Pusa-992", type: "Early Kharif Pulse", days: "140-145", yieldQ: "18-20" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.5, 8.0],
      preferredTexture: ["Deep Well-Drained Loam", "Sandy Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.40% - 0.70%"
    },
    operationalThresholds: {
      moistureSowingPct: [35.0, 60.0],
      moistureGrowthPct: [35.0, 65.0],
      soilTempSowingC: [22.0, 30.0],
      soilTempGrowthC: [18.0, 35.0],
      ambientTempMaxC: 40.0
    },
    sensorIndexExpectation: {
      nIndexMin: 30,
      pIndexMin: 35,
      kIndexMin: 40,
      note: "Deep taproot extracts subsoil nutrients; nitrogen-fixing"
    },
    waterManagement: {
      totalWaterReqMm: [500, 650],
      irrigationCount: "1 to 2 if post-monsoon dry spell occurs",
      criticalStages: [
        { stageEn: "Flower Bud Initiation", stageHi: "कलियां व फूल आने की शुरुआत", das: "Post-monsoon", importance: "CRITICAL" },
        { stageEn: "Pod Filling Stage", stageHi: "फलियों में दाना भराव", das: "Winter", importance: "IMPORTANT" }
      ],
      droughtTolerance: "HIGH",
      waterloggingSensitivity: "EXTREME (Phytophthora blight within 48 hrs waterlogging)"
    },
    limitingFactors: [
      {
        conditionEn: "Kharif Waterlogging & Phytophthora Stem Blight",
        conditionHi: "खरीफ में जलभराव व उकसा/झुलसा रोग",
        threshold: "Moisture > 75% for > 48 hours",
        impactEn: "Phytophthora stem rot kills standing plants rapidly in waterlogged patches",
        impactHi: "तने पर काले धब्बे, जलभराव से पौधों का अचानक सूखकर मरना",
        actionEn: "Always plant on raised beds / ridges with furrow drainage. Ensure drainage outlets.",
        actionHi: "अरहर की बुवाई मेड़ों (Ridge/Bed) पर करें ताकि बरसात का पानी जड़ों में न रुके।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIPR Kanpur",
      publication: "Pigeonpea Production Guide for Uttar Pradesh (2024)",
      verified: true
    }
  },

  "maize": {
    cropId: "maize",
    cropNameEn: "Maize / Corn (मक्का)",
    cropNameHi: "मक्का (मकई)",
    icon: "🌽",
    botanicalName: "Zea mays",
    season: "KHARIF",
    sowingWindow: {
      startMonth: 6, startDay: 15,
      endMonth: 7, endDay: 15,
      descEn: "Kharif: 15 Jun – 15 Jul; Zaid/Spring: 15 Feb – 15 Mar",
      descHi: "खरीफ: 15 जून – 15 जुलाई; जायद/बसंत: 15 फरवरी – 15 मार्च"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Kanchan", type: "Yellow Semi-Dent UP Standard", days: "85-90", yieldQ: "40-45" },
      { name: "HQPM-1", type: "Quality Protein Maize (High Lysine/Tryptophan)", days: "95-100", yieldQ: "50-55" },
      { name: "Ganga-11", type: "Widely Adapted Hybrid", days: "90-95", yieldQ: "45-50" },
      { name: "Bio-9681", type: "High Yielding Single Cross Hybrid", days: "95-100", yieldQ: "55-60" },
      { name: "Shaktiman-2", type: "White QPM Hybrid", days: "90-95", yieldQ: "48-52" }
    ],
    soilRequirements: {
      phOptimal: [5.8, 7.2],
      phTolerable: [5.5, 8.0],
      preferredTexture: ["Well-Drained Sandy Loam", "Silt Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.50% - 0.75%"
    },
    operationalThresholds: {
      moistureSowingPct: [45.0, 70.0],
      moistureGrowthPct: [50.0, 75.0],
      soilTempSowingC: [20.0, 30.0],
      soilTempGrowthC: [18.0, 35.0],
      ambientTempMaxC: 38.0
    },
    sensorIndexExpectation: {
      nIndexMin: 75,
      pIndexMin: 40,
      kIndexMin: 50,
      note: "High nitrogen and zinc demand"
    },
    waterManagement: {
      totalWaterReqMm: [450, 600],
      irrigationCount: "3 to 4 in Spring/Zaid; rain-fed in Kharif with drainage",
      criticalStages: [
        { stageEn: "Knee-High Stage", stageHi: "घुटने तक ऊंचाई की अवस्था", das: "30-35 DAS", importance: "IMPORTANT" },
        { stageEn: "Tasseling (Male Flower)", stageHi: "नर मंजरी (टैसल) निकलने की अवस्था", das: "45-55 DAS", importance: "CRITICAL" },
        { stageEn: "Silking (Female Cob)", stageHi: "सिल्क (बाल) निकलने व परागण", das: "55-65 DAS", importance: "CRITICAL" },
        { stageEn: "Grain Milking Stage", stageHi: "दाने में दूध पड़ने की अवस्था", das: "70-80 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "MEDIUM",
      waterloggingSensitivity: "HIGH (Cannot tolerate standing water for > 24 hrs)"
    },
    limitingFactors: [
      {
        conditionEn: "Drought at Tasseling/Silking",
        conditionHi: "मंजरी व सिल्क आने पर नमी का संकट",
        threshold: "Moisture < 35% at tasseling",
        impactEn: "Pollen desiccation, asynchronous tasseling/silking, blind cobs (no grain set)",
        impactHi: "परागकणों का सूखना, भुट्टे में दाने न पड़ना, भारी नुकसान",
        actionEn: "Ensure critical life-saving irrigation at tasseling and silking stages without delay.",
        actionHi: "मंजरी और सिल्क निकलते समय खेत में पानी की कमी न होने दें, सिंचाई तुरंत करें।",
        actionTiming: "STANDING_CROP",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIMR Ludhiana & CSAUAT Kanpur",
      publication: "Maize Production Manual for Uttar Pradesh (2024)",
      verified: true
    }
  },

  "lentil": {
    cropId: "lentil",
    cropNameEn: "Lentil / Masoor (मसूर)",
    cropNameHi: "मसूर",
    icon: "🫘",
    botanicalName: "Lens culinaris",
    season: "RABI",
    sowingWindow: {
      startMonth: 10, startDay: 20,
      endMonth: 11, endDay: 20,
      descEn: "20 Oct – 20 Nov (Utera / Relay: 10-15 Nov in standing rice)",
      descHi: "20 अक्टूबर – 20 नवंबर (उतेरा/पैरा विधि: खड़े धान में 10-15 नवंबर)"
    },
    suitableZones: ["UP-Z1", "UP-Z3", "UP-Z5", "UP-Z6", "UP-Z7", "UP-Z8", "UP-Z9"],
    varietiesUP: [
      { name: "DPL-62 (Sheri)", type: "Small Seeded UP Recommended", days: "125-130", yieldQ: "18-20" },
      { name: "IPL-81", type: "Large Seeded Bold Rust Resistant", days: "120-125", yieldQ: "16-18" },
      { name: "Narendra Masoor-1", type: "Eastern UP Adapted", days: "125-130", yieldQ: "16-19" },
      { name: "KLS-218", type: "High Yielding CSAUAT Release", days: "130-135", yieldQ: "18-22" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.5, 8.2],
      preferredTexture: ["Loam", "Clay Loam", "Alluvial Silty Loam"],
      drainageRequirement: "GOOD",
      organicCarbonTarget: "0.35% - 0.60%"
    },
    operationalThresholds: {
      moistureSowingPct: [30.0, 50.0],
      moistureGrowthPct: [35.0, 55.0],
      soilTempSowingC: [16.0, 24.0],
      soilTempGrowthC: [12.0, 24.0],
      ambientTempMaxC: 30.0
    },
    sensorIndexExpectation: {
      nIndexMin: 25,
      pIndexMin: 30,
      kIndexMin: 35,
      note: "Low nitrogen requirement; responds well to phosphorus"
    },
    waterManagement: {
      totalWaterReqMm: [200, 300],
      irrigationCount: "1 to 2 light irrigations",
      criticalStages: [
        { stageEn: "Branching / Pre-bloom", stageHi: "शाखाएं निकलने की अवस्था", das: "35-40 DAS", importance: "CRITICAL" },
        { stageEn: "Pod Formation", stageHi: "फलियों में दाना भराव", das: "65-70 DAS", importance: "IMPORTANT" }
      ],
      droughtTolerance: "HIGH",
      waterloggingSensitivity: "HIGH"
    },
    limitingFactors: [
      {
        conditionEn: "Excess Water / Poor Drainage",
        conditionHi: "अधिक नमी व खेत में पानी ठहरना",
        threshold: "Moisture > 60%",
        impactEn: "Root rot and collar rot; plant yellowing and mortality",
        impactHi: "जड़ गलन, पौधों का पीला होकर मरना",
        actionEn: "Ensure light irrigation only; avoid flooding.",
        actionHi: "हल्की सिंचाई करें, खेत में पानी बिल्कुल न ठहरने दें।",
        actionTiming: "STANDING_CROP",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIPR Kanpur",
      publication: "Lentil Cultivation in Indo-Gangetic Plains (2024)",
      verified: true
    }
  },

  "moong": {
    cropId: "moong",
    cropNameEn: "Green Gram / Moong (मूंग)",
    cropNameHi: "मूंग (ग्रीन ग्राम)",
    icon: "🫛",
    botanicalName: "Vigna radiata",
    season: "ZAID",
    sowingWindow: {
      startMonth: 3, startDay: 15,
      endMonth: 4, endDay: 15,
      descEn: "Zaid (Summer): 15 Mar – 15 Apr; Kharif: 01 Jul – 15 Jul",
      descHi: "जायद (ग्रीष्मकालीन): 15 मार्च – 15 अप्रैल; खरीफ: 01 जुलाई – 15 जुलाई"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Samrat", type: "Short Duration Summer (60 days)", days: "58-62", yieldQ: "12-15" },
      { name: "IPM-02-3", type: "YMV Resistant Summer Moong", days: "60-65", yieldQ: "14-16" },
      { name: "Meha", type: "Synchronous Pod Maturing", days: "62-65", yieldQ: "12-14" },
      { name: "Virat", type: "Super Early (52-55 days)", days: "52-56", yieldQ: "10-13" },
      { name: "HUM-16", type: "Eastern UP High Yielder", days: "60-65", yieldQ: "12-15" }
    ],
    soilRequirements: {
      phOptimal: [6.2, 7.5],
      phTolerable: [5.5, 8.0],
      preferredTexture: ["Loam", "Sandy Loam"],
      drainageRequirement: "GOOD",
      organicCarbonTarget: "0.40% - 0.65%"
    },
    operationalThresholds: {
      moistureSowingPct: [35.0, 60.0],
      moistureGrowthPct: [40.0, 65.0],
      soilTempSowingC: [22.0, 32.0],
      soilTempGrowthC: [20.0, 38.0],
      ambientTempMaxC: 42.0
    },
    sensorIndexExpectation: {
      nIndexMin: 25,
      pIndexMin: 35,
      kIndexMin: 35,
      note: "Short window summer catch crop; improves soil nitrogen"
    },
    waterManagement: {
      totalWaterReqMm: [300, 400],
      irrigationCount: "3 to 4 in summer at 10-12 day intervals",
      criticalStages: [
        { stageEn: "Flower Initiation", stageHi: "फूल आने की शुरुआत", das: "25-30 DAS", importance: "CRITICAL" },
        { stageEn: "Pod Development", stageHi: "फलियों में दाना भराव", das: "40-45 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "MEDIUM",
      waterloggingSensitivity: "HIGH"
    },
    limitingFactors: [
      {
        conditionEn: "Yellow Mosaic Virus (YMV) / Whitefly",
        conditionHi: "पीला मोज़ेक वायरस (YMV) का प्रकोप",
        threshold: "Susceptible variety + high whitefly population",
        impactEn: "Leaves turn completely yellow; no pod formation",
        impactHi: "पत्तियां पूरी पीली पड़ जाना, फलियां न बनना",
        actionEn: "Plant strictly YMV-resistant varieties (Samrat, IPM-02-3). Treat seed with Imidacloprid.",
        actionHi: "रोगरोधी किस्में (सम्राट, आईपीएम 02-3) ही बोएं। सफेद मक्खी का नियंत्रण करें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIPR Kanpur",
      publication: "Summer Moong Cultivation in Wheat-Rice System (2024)",
      verified: true
    }
  },

  "bajra": {
    cropId: "bajra",
    cropNameEn: "Pearl Millet / Bajra (बाजरा)",
    cropNameHi: "बाजरा",
    icon: "🌾",
    botanicalName: "Pennisetum glaucum",
    season: "KHARIF",
    sowingWindow: {
      startMonth: 7, startDay: 1,
      endMonth: 7, endDay: 30,
      descEn: "01 Jul – 25 Jul (With onset of monsoon showers)",
      descHi: "01 जुलाई – 25 जुलाई (मानसून की पहली बारिश के साथ)"
    },
    suitableZones: ["UP-Z4", "UP-Z5", "UP-Z6"],
    varietiesUP: [
      { name: "HHB-67 Improved", type: "Early Maturing Drought Escaping", days: "65-70", yieldQ: "25-30" },
      { name: "Proagro 9444", type: "High Yielding Hybrid", days: "80-85", yieldQ: "35-40" },
      { name: "Kaveri Super Boss", type: "Sturdy Tall Hybrid", days: "80-85", yieldQ: "32-38" },
      { name: "RHB-177", type: "South-West Semi-Arid UP", days: "75-80", yieldQ: "28-32" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 8.0],
      phTolerable: [5.5, 8.8],
      preferredTexture: ["Sandy Loam", "Loamy Sand", "Light Sandy Soils"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.25% - 0.50%"
    },
    operationalThresholds: {
      moistureSowingPct: [25.0, 50.0],
      moistureGrowthPct: [25.0, 60.0],
      soilTempSowingC: [25.0, 35.0],
      soilTempGrowthC: [20.0, 38.0],
      ambientTempMaxC: 44.0
    },
    sensorIndexExpectation: {
      nIndexMin: 40,
      pIndexMin: 20,
      kIndexMin: 30,
      note: "Low fertility demand; highly resilient C4 cereal"
    },
    waterManagement: {
      totalWaterReqMm: [250, 350],
      irrigationCount: "Mostly rain-fed; 1 life-saving if prolonged dry spell",
      criticalStages: [
        { stageEn: "Booting / Heading", stageHi: "सिट्टा (बाली) निकलने की अवस्था", das: "40-45 DAS", importance: "CRITICAL" },
        { stageEn: "Grain Filling", stageHi: "दाना भरने की अवस्था", das: "55-65 DAS", importance: "IMPORTANT" }
      ],
      droughtTolerance: "EXTREME",
      waterloggingSensitivity: "HIGH"
    },
    limitingFactors: [
      {
        conditionEn: "Waterlogging in Heavy Soils",
        conditionHi: "भारी मिट्टी में पानी भरना",
        threshold: "Moisture > 70% in clay soils",
        impactEn: "Seedling damping off; root rot",
        impactHi: "जड़ों का गलना, पौधे पीले पड़ना",
        actionEn: "Do not sow in low-lying clay depressions. Keep good drainage.",
        actionHi: "निचले जलभराव वाले खेतों में बाजरा न बोएं।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-AICRP on Pearl Millet & SVPUAT Meerut",
      publication: "Millets Production Package for Dryland UP (2024)",
      verified: true
    }
  },

  "tomato": {
    cropId: "tomato",
    cropNameEn: "Tomato (टमाटर)",
    cropNameHi: "टमाटर",
    icon: "🍅",
    botanicalName: "Solanum lycopersicum",
    season: "RABI",
    sowingWindow: {
      startMonth: 9, startDay: 15,
      endMonth: 10, endDay: 30,
      descEn: "Nursery: Sep; Transplanting: Oct – Nov; Spring: Jan – Feb",
      descHi: "नर्सरी: सितंबर; रोपाई: अक्टूबर – नवंबर; बसंत: जनवरी – फरवरी"
    },
    suitableZones: ["UP-Z1", "UP-Z2", "UP-Z3", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Kashi Amrit (DVRT-1)", type: "TLCV Tolerant IIVR Release", days: "110-120", yieldQ: "500-600" },
      { name: "Kashi Vishesh", type: "Determinate High Yielder", days: "115-120", yieldQ: "550-650" },
      { name: "Pusa Ruby", type: "Classic Early Acidic Standard", days: "100-110", yieldQ: "350-400" },
      { name: "Himsona", type: "Firm Round Hybrid (Long Transport)", days: "120-130", yieldQ: "600-750" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.0],
      phTolerable: [5.5, 7.5],
      preferredTexture: ["Well-Drained Sandy Loam", "Rich Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.60% - 1.00%"
    },
    operationalThresholds: {
      moistureSowingPct: [50.0, 75.0],
      moistureGrowthPct: [55.0, 75.0],
      soilTempSowingC: [18.0, 28.0],
      soilTempGrowthC: [15.0, 30.0],
      ambientTempMaxC: 35.0
    },
    sensorIndexExpectation: {
      nIndexMin: 70,
      pIndexMin: 45,
      kIndexMin: 80,
      note: "High calcium and potassium requirement for blossom-end rot prevention"
    },
    waterManagement: {
      totalWaterReqMm: [400, 600],
      irrigationCount: "Frequent light irrigations (drip preferred)",
      criticalStages: [
        { stageEn: "Flowering Stage", stageHi: "फूल आने की अवस्था", das: "30-40 DAT", importance: "CRITICAL" },
        { stageEn: "Fruit Setting & Expansion", stageHi: "फल बनने व आकार वृद्धि", das: "50-70 DAT", importance: "CRITICAL" }
      ],
      droughtTolerance: "LOW",
      waterloggingSensitivity: "EXTREME (Bacterial wilt occurs rapidly in waterlogged soil)"
    },
    limitingFactors: [
      {
        conditionEn: "Moisture Fluctuation & Blossom End Rot",
        conditionHi: "नमी का उतार-चढ़ाव व फलों का नीचे से काला पड़ना",
        threshold: "Moisture swings between <30% and >80%",
        impactEn: "Calcium deficiency causes blossom end rot; fruit cracking",
        impactHi: "टमाटर के फल नीचे से सड़ना (ब्लॉसम एंड रॉट), फलों का फटना",
        actionEn: "Maintain uniform soil moisture. Avoid alternate severe drying and heavy flooding. Apply calcium nitrate foliar spray.",
        actionHi: "खेत में एक समान हल्की नमी बनाए रखें। सूखा पड़ने के बाद भारी पानी न दें। कैल्शियम का छिड़काव करें।",
        actionTiming: "STANDING_CROP",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIVR Varanasi",
      publication: "Vegetable Production Guidelines for Eastern & Central UP (2024)",
      verified: true
    }
  },

  "onion": {
    cropId: "onion",
    cropNameEn: "Onion (प्याज)",
    cropNameHi: "प्याज",
    icon: "🧅",
    botanicalName: "Allium cepa",
    season: "RABI",
    sowingWindow: {
      startMonth: 11, startDay: 15,
      endMonth: 12, endDay: 30,
      descEn: "Nursery: Oct – Nov; Transplanting: Dec – Jan",
      descHi: "नर्सरी: अक्टूबर – नवंबर; रोपाई: दिसंबर – जनवरी"
    },
    suitableZones: ["UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Pusa Red", type: "Good Storing Rabi Variety", days: "125-135", yieldQ: "250-300" },
      { name: "Agrifound Light Red", type: "High Keeping Quality", days: "130-140", yieldQ: "280-320" },
      { name: "Bhima Super", type: "High Yielding Red Bulb", days: "115-120", yieldQ: "300-350" },
      { name: "Kalyanpur Red Round", type: "UP Local Adapted", days: "125-130", yieldQ: "250-280" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.2],
      phTolerable: [5.8, 7.8],
      preferredTexture: ["Friable Sandy Loam", "Rich Alluvial Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.50% - 0.80%"
    },
    operationalThresholds: {
      moistureSowingPct: [45.0, 65.0],
      moistureGrowthPct: [50.0, 70.0],
      soilTempSowingC: [14.0, 22.0],
      soilTempGrowthC: [12.0, 26.0],
      ambientTempMaxC: 32.0
    },
    sensorIndexExpectation: {
      nIndexMin: 65,
      pIndexMin: 40,
      kIndexMin: 60,
      note: "Sulfur improves pungency and storage firmness"
    },
    waterManagement: {
      totalWaterReqMm: [450, 600],
      irrigationCount: "10 to 12 light irrigations; shallow rooted crop",
      criticalStages: [
        { stageEn: "Transplant Establishment", stageHi: "रोपाई के बाद पौधे का जमना", das: "0-15 DAT", importance: "CRITICAL" },
        { stageEn: "Bulb Enlargement Stage", stageHi: "प्याज की गांठ (कंद) फूलने की अवस्था", das: "60-90 DAT", importance: "CRITICAL" }
      ],
      droughtTolerance: "LOW",
      waterloggingSensitivity: "EXTREME (Root rot and purple blotch in waterlogging)"
    },
    limitingFactors: [
      {
        conditionEn: "Irrigation Right Before Harvest",
        conditionHi: "खुदाई से ठीक पहले पानी देना",
        threshold: "Irrigation within 15 days of harvest",
        impactEn: "Neck rot and poor storage shelf life; rotting in godowns",
        impactHi: "भंडारण में प्याज का सड़ना, गर्दन मोटी होना",
        actionEn: "Stop irrigation completely 12-15 days before harvest when tops begin to fall (50% neck fall).",
        actionHi: "खुदाई से 12-15 दिन पूर्व पानी बिल्कुल बंद कर दें।",
        actionTiming: "STANDING_CROP",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-DOGR Rajgurunagar & CSAUAT Kanpur",
      publication: "Commercial Onion Production in Northern Plains (2024)",
      verified: true
    }
  },

  "garlic": {
    cropId: "garlic",
    cropNameEn: "Garlic (लहसुन)",
    cropNameHi: "लहसुन",
    icon: "🧄",
    botanicalName: "Allium sativum",
    season: "RABI",
    sowingWindow: {
      startMonth: 10, startDay: 15,
      endMonth: 11, endDay: 15,
      descEn: "15 Oct – 15 Nov (Optimal temperature for clove sprouting)",
      descHi: "15 अक्टूबर – 15 नवंबर (जमाव हेतु उपयुक्त तापमान)"
    },
    suitableZones: ["UP-Z2", "UP-Z3", "UP-Z4", "UP-Z5", "UP-Z7", "UP-Z8"],
    varietiesUP: [
      { name: "Yamuna Safed (G-1)", type: "Compact White Cloves", days: "140-150", yieldQ: "120-150" },
      { name: "G-282", type: "Bold White Cloves Export Quality", days: "130-140", yieldQ: "140-160" },
      { name: "Agrifound Parvati", type: "High Yielding Plains Adapted", days: "150-160", yieldQ: "150-180" }
    ],
    soilRequirements: {
      phOptimal: [6.0, 7.5],
      phTolerable: [5.8, 8.0],
      preferredTexture: ["Rich Sandy Loam", "Silt Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.60% - 1.00%"
    },
    operationalThresholds: {
      moistureSowingPct: [40.0, 65.0],
      moistureGrowthPct: [45.0, 65.0],
      soilTempSowingC: [15.0, 22.0],
      soilTempGrowthC: [12.0, 24.0],
      ambientTempMaxC: 30.0
    },
    sensorIndexExpectation: {
      nIndexMin: 65,
      pIndexMin: 40,
      kIndexMin: 55,
      note: "Sulfur essential for allicin formation and pungency"
    },
    waterManagement: {
      totalWaterReqMm: [400, 500],
      irrigationCount: "8 to 10 light irrigations",
      criticalStages: [
        { stageEn: "Clove Sprouting", stageHi: "कलियों का अंकुरण", das: "0-15 DAS", importance: "CRITICAL" },
        { stageEn: "Bulb Differentiation & Filling", stageHi: "गांठ व पुत्तियों का निर्माण", das: "70-90 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "LOW",
      waterloggingSensitivity: "EXTREME"
    },
    limitingFactors: [
      {
        conditionEn: "Clay Soil Compaction & Poor Drainage",
        conditionHi: "भारी मिट्टी में जमाव व गांठ का विकृत होना",
        threshold: "Heavy clay soil with drainage < 2 cm/hr",
        impactEn: "Misshapen, small discolored cloves; basal bulb rot",
        impactHi: "लहसुन की गांठ छोटी व बदरंग होना, जड़ सड़ना",
        actionEn: "Incorporate organic matter / sand to improve friability. Plant on raised beds.",
        actionHi: "खेत में गोबर की सड़ी खाद मिलाकर मिट्टी भुरभुरी बनाएं। उठी हुई क्यारियों में लगाएं।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-DOGR & NHRDF",
      publication: "Garlic Cultivation Practices for North India (2024)",
      verified: true
    }
  },

  "sesame": {
    cropId: "sesame",
    cropNameEn: "Sesame / Til (तिल)",
    cropNameHi: "तिल",
    icon: "🌱",
    botanicalName: "Sesamum indicum",
    season: "KHARIF",
    sowingWindow: {
      startMonth: 6, startDay: 25,
      endMonth: 7, endDay: 20,
      descEn: "25 Jun – 20 Jul (Bundelkhand & Vindhyan Kharif pulse-oilseed)",
      descHi: "25 जून – 20 जुलाई (बुंदेलखंड व विंध्य क्षेत्र में प्रमुख खरीफ तिलहन)"
    },
    suitableZones: ["UP-Z4", "UP-Z5", "UP-Z6", "UP-Z9"],
    varietiesUP: [
      { name: "Pragati", type: "White Seeded UP Recommended", days: "80-85", yieldQ: "6-8" },
      { name: "Shekhar", type: "High Oil Content Bundelkhand", days: "80-85", yieldQ: "7-9" },
      { name: "RT-351", type: "Drought Tolerant", days: "78-82", yieldQ: "6-8" }
    ],
    soilRequirements: {
      phOptimal: [5.5, 7.5],
      phTolerable: [5.2, 8.0],
      preferredTexture: ["Light Sandy Loam", "Well-Drained Loam"],
      drainageRequirement: "EXCELLENT",
      organicCarbonTarget: "0.25% - 0.50%"
    },
    operationalThresholds: {
      moistureSowingPct: [25.0, 45.0],
      moistureGrowthPct: [25.0, 50.0],
      soilTempSowingC: [25.0, 35.0],
      soilTempGrowthC: [22.0, 38.0],
      ambientTempMaxC: 42.0
    },
    sensorIndexExpectation: {
      nIndexMin: 30,
      pIndexMin: 20,
      kIndexMin: 25,
      note: "Low input crop; sensitive to excess moisture"
    },
    waterManagement: {
      totalWaterReqMm: [250, 350],
      irrigationCount: "Exclusively rain-fed; avoid water stagnancy",
      criticalStages: [
        { stageEn: "Flowering Phase", stageHi: "फूल आने की अवस्था", das: "30-35 DAS", importance: "CRITICAL" },
        { stageEn: "Capsule Formation", stageHi: "डोडिया (कैप्सूल) बनने की अवस्था", das: "45-55 DAS", importance: "CRITICAL" }
      ],
      droughtTolerance: "HIGH",
      waterloggingSensitivity: "EXTREME (Even 12 hours standing water causes total plant death)"
    },
    limitingFactors: [
      {
        conditionEn: "Water Stagnancy / Poor Drainage",
        conditionHi: "खेत में पानी रुकना",
        threshold: "Standing water > 12 hours",
        impactEn: "Phyllody disease and Phytophthora blight wipe out entire field",
        impactHi: "फाइलोडी रोग व जड़ सड़न, फसल पूरी नष्ट होना",
        actionEn: "Strictly avoid low-lying or poorly drained fields. Provide slope drainage.",
        actionHi: "ढलान वाले व अच्छी जल निकासी वाले खेतों में ही तिल की बुवाई करें।",
        actionTiming: "BEFORE_SOWING",
        isCritical: true
      }
    ],
    provenance: {
      sourceInstitution: "ICAR-IIOR Hyderabad & CSAUAT Kanpur",
      publication: "Sesame Production Guide for Bundelkhand (2024)",
      verified: true
    }
  }
};


// ============================================================================
// 3. STATISTICAL & AGRONOMIC HELPER FUNCTIONS
// ============================================================================

/**
 * Computes comprehensive statistical aggregations across sample nodes
 */
function computeFieldStats(samples) {
  if (!samples || samples.length === 0) {
    return null;
  }

  const valid = samples.filter(s => s && s.moisture > 0 || s.ph > 0);
  const n = valid.length > 0 ? valid.length : samples.length;
  const set = valid.length > 0 ? valid : samples;

  const extract = key => set.map(s => Number(s[key]) || 0);

  const statsFor = (arr) => {
    if (arr.length === 0) return { mean: 0, median: 0, min: 0, max: 0, stdDev: 0, cvPct: 0 };
    const sorted = [...arr].sort((a,b) => a - b);
    const sum = arr.reduce((acc, v) => acc + v, 0);
    const mean = sum / arr.length;
    const median = sorted.length % 2 === 0
      ? (sorted[sorted.length/2 - 1] + sorted[sorted.length/2]) / 2
      : sorted[Math.floor(sorted.length/2)];
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const variance = arr.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / arr.length;
    const stdDev = Math.sqrt(variance);
    const cvPct = mean > 0 ? (stdDev / mean) * 100 : 0;
    return { mean, median, min, max, stdDev, cvPct };
  };

  return {
    sampleCount: n,
    moisture: statsFor(extract('moisture')),
    temp: statsFor(extract('temp')),
    ph: statsFor(extract('ph')),
    nitrogen: statsFor(extract('n')),
    phosphorus: statsFor(extract('p')),
    potassium: statsFor(extract('k'))
  };
}

/**
 * Determines current agricultural season in Uttar Pradesh based on calendar month
 */
function getCurrentSeason() {
  const month = new Date().getMonth() + 1; // 1-12
  // Kharif: June (6) to October (10)
  // Rabi: November (11) to March (3)
  // Zaid: April (4) to May (5)
  if (month >= 6 && month <= 10) return "KHARIF";
  if (month >= 11 || month <= 3) return "RABI";
  return "ZAID";
}

/**
 * Classifies an individual parameter against verified ranges
 */
function classifyParamStatus(val, optimalRange, tolerableRange) {
  if (val === undefined || val === null || isNaN(val) || val <= 0) {
    return { status: "UNKNOWN", labelEn: "Unknown", labelHi: "अज्ञात", severity: "info" };
  }
  const [optMin, optMax] = optimalRange;
  const [tolMin, tolMax] = tolerableRange;

  if (val >= optMin && val <= optMax) {
    return { status: "OPTIMAL", labelEn: "Suitable", labelHi: "उपयुक्त", severity: "success" };
  }
  if (val >= tolMin && val <= tolMax) {
    if (val < optMin) {
      return { status: "MARGINAL_LOW", labelEn: "Marginal Low", labelHi: "हल्का कम", severity: "warning" };
    } else {
      return { status: "MARGINAL_HIGH", labelEn: "Marginal High", labelHi: "हल्का अधिक", severity: "warning" };
    }
  }
  if (val < tolMin) {
    return { status: "DEFICIENT", labelEn: "Critical Deficit", labelHi: "गंभीर कमी", severity: "danger" };
  }
  return { status: "EXCESS", labelEn: "Critical Excess", labelHi: "गंभीर अधिकता", severity: "danger" };
}


// ============================================================================
// 4. CENTRAL AGRO-DECISION ENGINE CLASS
// ============================================================================

class AgroDecisionEngine {
  constructor() {
    this.version = "2.0.0-UP";
    this.context = {
      state: "Uttar Pradesh",
      district: "Kanpur Nagar",
      zoneId: "UP-Z5",
      season: getCurrentSeason(),
      soilType: "Unknown",
      waterSource: "Tube well"
    };
    this.liveData = {};
    this.samples = [];
    this.fieldStats = null;
    this.labRecords = []; // Lab comparison soil validation records
  }

  setContext(district, season, soilType, waterSource) {
    if (district) {
      this.context.district = district;
      this.context.zoneId = getZoneByDistrict(district);
    }
    if (season) this.context.season = season;
    if (soilType) this.context.soilType = soilType;
    if (waterSource) this.context.waterSource = waterSource;
  }

  ingestLiveData(dataObj) {
    if (!dataObj) return;
    this.liveData = { ...dataObj };
  }

  ingestSamples(samplesArray) {
    if (!samplesArray || !Array.isArray(samplesArray)) return;
    this.samples = [...samplesArray];
    this.fieldStats = computeFieldStats(this.samples);
  }

  getFieldAverages() {
    if (this.fieldStats && this.fieldStats.sampleCount > 0) {
      return {
        isSurvey: true,
        sampleCount: this.fieldStats.sampleCount,
        moisture: this.fieldStats.moisture.mean,
        soilTemp: this.fieldStats.temp.mean,
        ph: this.fieldStats.ph.mean,
        nitrogen: this.fieldStats.nitrogen.mean,
        phosphorus: this.fieldStats.phosphorus.mean,
        potassium: this.fieldStats.potassium.mean,
        ambientTemp: this.liveData.temp || 24.0,
        ambientHum: this.liveData.hum || 60.0
      };
    }
    // Fallback to live telemetry
    return {
      isSurvey: false,
      sampleCount: 0,
      moisture: this.liveData.soilMoisture || 0,
      soilTemp: this.liveData.soilTemp || 0,
      ph: this.liveData.ph || 0,
      nitrogen: this.liveData.nitrogen || 0,
      phosphorus: this.liveData.phosphorus || 0,
      potassium: this.liveData.potassium || 0,
      ambientTemp: this.liveData.temp || 24.0,
      ambientHum: this.liveData.hum || 60.0
    };
  }

  // --------------------------------------------------------------------------
  // MODE A: CROP DISCOVERY ("What should I grow?")
  // --------------------------------------------------------------------------
  runCropDiscovery() {
    const avg = this.getFieldAverages();
    const results = [];

    for (const cropKey in UP_CROP_DATABASE) {
      const crop = UP_CROP_DATABASE[cropKey];
      const evaluation = this._evaluateCropSuitability(crop, avg, this.context);
      results.push(evaluation);
    }

    // Sort: Highly suitable first, then by numerical score
    results.sort((a, b) => {
      if (a.isFeasible !== b.isFeasible) return a.isFeasible ? -1 : 1;
      return b.suitabilityScore - a.suitabilityScore;
    });

    return {
      timestamp: new Date().toISOString(),
      context: { ...this.context },
      fieldSummary: avg,
      rankedCrops: results
    };
  }

  _evaluateCropSuitability(crop, fieldAvg, context) {
    const limits = [];
    let isFeasible = true;
    const m = fieldAvg.moisture;
    const ph = fieldAvg.ph;

    if (ph > 0) {
      if (ph < crop.soilRequirements.phTolerable[0]) {
        isFeasible = false;
        limits.push({
          severity: "CRITICAL",
          param: "Soil pH",
          textEn: `Severe soil acidity (pH ${ph.toFixed(1)}). Below tolerable minimum ${crop.soilRequirements.phTolerable[0]}.`,
          textHi: `अत्यधिक अम्लीय मिट्टी (pH ${ph.toFixed(1)}), जो न्यूनतम सीमा ${crop.soilRequirements.phTolerable[0]} से नीचे है।`
        });
      } else if (ph > crop.soilRequirements.phTolerable[1]) {
        isFeasible = false;
        limits.push({
          severity: "CRITICAL",
          param: "Soil pH",
          textEn: `Severe soil alkalinity (pH ${ph.toFixed(1)}). Exceeds tolerable maximum ${crop.soilRequirements.phTolerable[1]}.`,
          textHi: `अत्यधिक क्षारीय मिट्टी (pH ${ph.toFixed(1)}), जो अधिकतम सीमा ${crop.soilRequirements.phTolerable[1]} से अधिक है।`
        });
      }
    }

    // Hard Gate 2: Sowing Season alignment
    const currentSeason = context.season;
    const isSeasonMatch = (crop.season === "PERENNIAL") || (crop.season === currentSeason);
    if (!isSeasonMatch) {
      limits.push({
        severity: "ATTENTION",
        param: "Season Window",
        textEn: `Crop season is ${crop.season}, but current operating season is ${currentSeason}. Recommended during normal calendar window.`,
        textHi: `यह फसल ${crop.season} सीजन की है, जबकि अभी ${currentSeason} चल रहा है। उपयुक्त समय पर ही बोएं।`
      });
    }

    // Hard Gate 3: Water Availability alignment
    if (context.waterSource === "Rain-fed" && (crop.waterManagement.totalWaterReqMm[0] > 700 || crop.waterManagement.droughtTolerance === "LOW")) {
      isFeasible = false;
      limits.push({
        severity: "CRITICAL",
        param: "Water Source",
        textEn: `High water demand crop (${crop.waterManagement.totalWaterReqMm[0]}-${crop.waterManagement.totalWaterReqMm[1]} mm) cannot be sustained under strictly rain-fed farming.`,
        textHi: `भारी जल मांग (${crop.waterManagement.totalWaterReqMm[0]}-${crop.waterManagement.totalWaterReqMm[1]} मिमी) केवल वर्षा आधारित खेती में संभव नहीं है।`
      });
    }

    // Hard Gate 4: Extreme Soil Saturation / Waterlogging for sensitive crops
    const wlSens = crop.waterManagement.waterloggingSensitivity || "";
    if (m > 70 && (wlSens.includes("EXTREME") || (m > 80 && wlSens.includes("HIGH")))) {
      isFeasible = false;
      limits.push({
        severity: "CRITICAL",
        param: "Severe Waterlogging",
        textEn: `Extreme soil saturation (${m.toFixed(1)}%). Sowing ${crop.cropNameEn} will cause total failure due to root asphyxiation and damping off.`,
        textHi: `खेत में भारी जलभराव/नमी (${m.toFixed(1)}%)। इस स्थिति में ${crop.cropNameHi} बोने से जड़ सड़न व बीज नष्ट हो जाएगा।`
      });
    }


    // Compute Multi-Factor Weighted Score (0-100)
    let score = 0;
    const weights = { moisture: 0.30, ph: 0.25, temp: 0.20, zone: 0.15, season: 0.10 };

    // Moisture component (0-100)
    let mScore = 50;
    if (m > 0) {
      const [optMin, optMax] = crop.operationalThresholds.moistureSowingPct;
      if (m >= optMin && m <= optMax) {
        mScore = 100;
      } else if (m < optMin) {
        const deficit = optMin - m;
        mScore = Math.max(10, 100 - deficit * 3.5);
        if (deficit > 20) {
          limits.push({
            severity: "ATTENTION",
            param: "Moisture",
            textEn: `Sowing moisture low (${m.toFixed(1)}% vs target ${optMin}-${optMax}%). Pre-sowing irrigation (Palewa) required.`,
            textHi: `बुवाई की नमी कम (${m.toFixed(1)}% जबकि जरूरत ${optMin}-${optMax}%)। पलेवा की आवश्यकता है।`
          });
        }
      } else {
        const excess = m - optMax;
        mScore = Math.max(15, 100 - excess * 3.0);
        if (excess > 15 && crop.waterManagement.waterloggingSensitivity === "HIGH") {
          limits.push({
            severity: "ATTENTION",
            param: "Moisture",
            textEn: `Excess moisture (${m.toFixed(1)}%). Risk of seed damping off; wait for field workable condition.`,
            textHi: `नमी अधिक (${m.toFixed(1)}%)। बीज सड़ने का खतरा; खेत में ओट (वापसा) आने दें।`
          });
        }
      }
    }

    // pH component (0-100)
    let pScore = 50;
    if (ph > 0) {
      const [pOptMin, pOptMax] = crop.soilRequirements.phOptimal;
      const [pTolMin, pTolMax] = crop.soilRequirements.phTolerable;
      if (ph >= pOptMin && ph <= pOptMax) {
        pScore = 100;
      } else if (ph >= pTolMin && ph <= pTolMax) {
        pScore = 70;
        limits.push({
          severity: "ATTENTION",
          param: "Soil pH",
          textEn: `pH ${ph.toFixed(1)} is outside optimum (${pOptMin}-${pOptMax}) but tolerable. Yield will improve with soil amendment.`,
          textHi: `pH ${ph.toFixed(1)} उत्तम श्रेणी से बाहर है पर सहनशील है। सुधारक डालने से पैदावार बढ़ेगी।`
        });
      } else {
        pScore = 20;
      }
    }

    // Temperature component (0-100)
    let tScore = 60;
    const t = fieldAvg.soilTemp || fieldAvg.ambientTemp;
    if (t > 0) {
      const [tMin, tMax] = crop.operationalThresholds.soilTempSowingC;
      if (t >= tMin && t <= tMax) {
        tScore = 100;
      } else {
        const diff = t < tMin ? tMin - t : t - tMax;
        tScore = Math.max(20, 100 - diff * 7);
        if (diff > 5) {
          limits.push({
            severity: "ATTENTION",
            param: "Temperature",
            textEn: `Temperature (${t.toFixed(1)}°C) is sub-optimal for germination (optimum: ${tMin}-${tMax}°C).`,
            textHi: `तापमान (${t.toFixed(1)}°C) जमाव के लिए अनुकूलतम (${tMin}-${tMax}°C) से भिन्न है।`
          });
        }
      }
    }

    // Zone adaptability component
    let zScore = crop.suitableZones.includes(context.zoneId) ? 100 : 40;
    if (zScore < 100) {
      limits.push({
        severity: "INFO",
        param: "Zone Adaptability",
        textEn: `Not traditionally a primary crop for ${UP_AGRO_ZONES[context.zoneId]?.zoneNameEn || context.zoneId}, but can be cultivated with micro-climate management.`,
        textHi: `यह ${UP_AGRO_ZONES[context.zoneId]?.zoneNameHi || context.zoneId} की प्राथमिक फसल नहीं है, विशेष ध्यान से उगाई जा सकती है।`
      });
    }

    // Season alignment score
    let sScore = isSeasonMatch ? 100 : 30;

    // Aggregate score
    score = Math.round(
      mScore * weights.moisture +
      pScore * weights.ph +
      tScore * weights.temp +
      zScore * weights.zone +
      sScore * weights.season
    );

    // Classification
    let suitabilityTag = "NOT_RECOMMENDED";
    let tagEn = "Not Recommended";
    let tagHi = "संस्तुत नहीं";

    if (isFeasible) {
      if (score >= 80) {
        suitabilityTag = "HIGHLY_SUITABLE";
        tagEn = "Highly Suitable";
        tagHi = "अति उपयुक्त";
      } else if (score >= 60) {
        suitabilityTag = "POTENTIALLY_SUITABLE";
        tagEn = "Potentially Suitable with Management";
        tagHi = "सुधार के साथ उपयुक्त";
      } else {
        suitabilityTag = "NEEDS_ATTENTION";
        tagEn = "Sub-Optimal / Attention Required";
        tagHi = "विशेष ध्यान अपेक्षित";
      }
    }

    return {
      cropId: crop.cropId,
      cropNameEn: crop.cropNameEn,
      cropNameHi: crop.cropNameHi,
      icon: crop.icon,
      season: crop.season,
      isFeasible,
      suitabilityScore: isFeasible ? score : Math.min(score, 35),
      suitabilityTag,
      tagEn,
      tagHi,
      sowingWindow: crop.sowingWindow,
      recommendedVarieties: crop.varietiesUP,
      limitingFactors: limits,
      confidence: fieldAvg.isSurvey ? "HIGH_FIELD_SURVEY" : "MODERATE_SINGLE_SAMPLE",
      missingInformation: [
        "Laboratory soil buffer capacity for amendment dosage",
        "Soil texture verification (currently assumed)",
        "Organic carbon percentage (Walkley-Black lab test)"
      ],
      provenance: crop.provenance
    };
  }

  // --------------------------------------------------------------------------
  // MODE B: TARGET CROP GAP ANALYSIS ("I want to grow X. What to improve?")
  // --------------------------------------------------------------------------
  runTargetCropAnalysis(targetCropId) {
    const cropKey = targetCropId.toLowerCase().trim();
    const crop = UP_CROP_DATABASE[cropKey];

    if (!crop) {
      return {
        error: true,
        messageEn: `Crop '${targetCropId}' not found in Uttar Pradesh knowledge base.`,
        messageHi: `फसल '${targetCropId}' उप्र कृषि ज्ञानकोष में उपलब्ध नहीं है।`
      };
    }

    const avg = this.getFieldAverages();
    const gapRows = [];
    const preSowingActions = [];
    const standingCropActions = [];
    const labTestsNeeded = [];

    // 1. pH Parameter Gap
    const phVal = avg.ph;
    const [phOptMin, phOptMax] = crop.soilRequirements.phOptimal;
    const [phTolMin, phTolMax] = crop.soilRequirements.phTolerable;
    let phStatus = "SUITABLE";
    let phActionEn = "pH is in optimum range. No chemical correction needed.";
    let phActionHi = "pH उत्तम श्रेणी में है। रासायनिक सुधार की जरूरत नहीं।";
    let phCritical = false;

    if (phVal <= 0) {
      phStatus = "UNKNOWN";
      phActionEn = "Insert probe into moist soil to measure field pH.";
      phActionHi = "खेत का pH मापने के लिए सेंसर को नम मिट्टी में लगाएं।";
    } else if (phVal < phTolMin) {
      phStatus = "CRITICAL_ACIDIC";
      phCritical = true;
      phActionEn = `Soil is severely acidic (pH ${phVal.toFixed(1)}). Apply agricultural lime/dolomite. Conduct laboratory buffer pH test for exact lime requirement (LR).`;
      phActionHi = `मिट्टी अत्यधिक अम्लीय (pH ${phVal.toFixed(1)}) है। बुवाई से पूर्व कृषि चूना मिलाएं। सटीक मात्रा हेतु प्रयोगशाला में जांच कराएं।`;
      preSowingActions.push({
        titleEn: "Lime Application for Soil Acidity",
        titleHi: "अम्लीयता सुधार हेतु चूने का प्रयोग",
        descEn: "Broadcast agricultural lime 2-3 weeks before sowing and incorporate with deep ploughing.",
        descHi: "बुवाई से 2-3 सप्ताह पूर्व कृषि चूने का भुरकाव कर जुताई करें।",
        timing: "BEFORE_SOWING",
        critical: true
      });
      labTestsNeeded.push("Soil Buffer pH & Exchangeable Acidity Test");
    } else if (phVal > phTolMax) {
      phStatus = "CRITICAL_ALKALINE";
      phCritical = true;
      phActionEn = `Soil is severely alkaline/sodic (pH ${phVal.toFixed(1)}). Apply agricultural gypsum. Test Exchangeable Sodium Percentage (ESP) at nearest KVK soil lab.`;
      phActionHi = `मिट्टी अत्यधिक क्षारीय/ऊसर (pH ${phVal.toFixed(1)}) है। जिप्सम का प्रयोग करें। नजदीकी केवीके लैब से सोडियम प्रतिशत (ESP) जांच कराएं।`;
      preSowingActions.push({
        titleEn: "Gypsum Application for Sodic Soil",
        titleHi: "ऊसर सुधार हेतु जिप्सम का प्रयोग",
        descEn: "Apply agricultural gypsum based on Gypsum Requirement (GR). Irrigate and drain to leach salts.",
        descHi: "जिप्सम डालकर खेत में पानी भरकर लवणों का निक्षालन (लीचिंग) करें।",
        timing: "BEFORE_SOWING",
        critical: true
      });
      labTestsNeeded.push("Exchangeable Sodium Percentage (ESP) & Gypsum Requirement Test");
    } else if (phVal < phOptMin || phVal > phOptMax) {
      phStatus = "NEEDS_ATTENTION";
      phActionEn = `pH ${phVal.toFixed(1)} is slightly outside optimum (${phOptMin}-${phOptMax}). Add well-rotted FYM/compost (10-15 tonnes/ha) to buffer soil.`;
      phActionHi = `pH ${phVal.toFixed(1)} हल्का असंतुलित है। 10-15 टन सड़ी गोबर खाद या वर्मीकम्पोस्ट मिलाएं।`;
      preSowingActions.push({
        titleEn: "Organic Buffering with FYM",
        titleHi: "गोबर खाद द्वारा मृदा संतुलन",
        descEn: "Incorporate 10-15 tonnes/ha FYM or green manure (Dhaincha) to naturally buffer pH.",
        descHi: "10-15 टन/हेक्टेयर गोबर की खाद या ढैंचा हरी खाद मिलाकर मिट्टी सुधारें।",
        timing: "BEFORE_SOWING",
        critical: false
      });
    }

    gapRows.push({
      parameter: "Soil pH",
      parameterHi: "मृदा pH (अम्लीयता/क्षारीयता)",
      fieldValue: phVal > 0 ? phVal.toFixed(1) : "N/A",
      requirement: `${phOptMin} – ${phOptMax} (Tolerable: ${phTolMin}–${phTolMax})`,
      status: phStatus,
      critical: phCritical,
      suggestedActionEn: phActionEn,
      suggestedActionHi: phActionHi,
      timing: "BEFORE_SOWING"
    });

    // 2. Moisture Parameter Gap
    const mVal = avg.moisture;
    const [mOptMin, mOptMax] = crop.operationalThresholds.moistureSowingPct;
    let mStatus = "SUITABLE";
    let mActionEn = "Moisture is adequate for seed placement and germination.";
    let mActionHi = "बीज अंकुरण व बुवाई हेतु पर्याप्त नमी उपलब्ध है।";
    let mCritical = false;

    if (mVal <= 0) {
      mStatus = "UNKNOWN";
      mActionEn = "Soil moisture not recorded. Probe insertion required.";
      mActionHi = "नमी दर्ज नहीं हुई। सेंसर जांच अपेक्षित है।";
    } else if (mVal < mOptMin) {
      mStatus = "DEFICIENT";
      mCritical = true;
      mActionEn = `Moisture (${mVal.toFixed(1)}%) is below sowing requirement (${mOptMin}%). Pre-sowing irrigation (Palewa) is mandatory 5-7 days before tillage.`;
      mActionHi = `नमी (${mVal.toFixed(1)}%) बुवाई जरूरत (${mOptMin}%) से कम है। जुताई से 5-7 दिन पूर्व पलेवा (रौनी) करना अनिवार्य है।`;
      preSowingActions.push({
        titleEn: "Pre-Sowing Irrigation (Palewa)",
        titleHi: "बुवाई पूर्व पलेवा (रौनी) सिंचाई",
        descEn: `Apply 50-60 mm pre-sowing irrigation. Plough when soil reaches workable condition (Wapsa).`,
        descHi: `50-60 मिमी पलेवा लगाएं। खेत में ओट (वापसा) आने पर ही जुताई व बुवाई करें।`,
        timing: "BEFORE_SOWING",
        critical: true
      });
    } else if (mVal > mOptMax) {
      mStatus = "EXCESS";
      mCritical = crop.waterManagement.waterloggingSensitivity === "HIGH";
      mActionEn = `Moisture (${mVal.toFixed(1)}%) is high. Sowing now will cause seed rotting. Allow field to dry to workable condition (Wapsa).`;
      mActionHi = `नमी (${mVal.toFixed(1)}%) अधिक है। अभी बुवाई से बीज सड़ सकता है। खेत सूखने दें।`;
      preSowingActions.push({
        titleEn: "Field Aeration / Drainage",
        titleHi: "खेत को सुखाना व जल निकास",
        descEn: "Allow upper 5 cm soil crust to dry before running seed-drill.",
        descHi: "बीज ड्रिल चलाने से पहले ऊपरी 5 सेमी सतह सूखने दें।",
        timing: "BEFORE_SOWING",
        critical: mCritical
      });
    }

    gapRows.push({
      parameter: "Sowing Moisture",
      parameterHi: "बुवाई की नमी (%)",
      fieldValue: mVal > 0 ? `${mVal.toFixed(1)}%` : "N/A",
      requirement: `${mOptMin}% – ${mOptMax}%`,
      status: mStatus,
      critical: mCritical,
      suggestedActionEn: mActionEn,
      suggestedActionHi: mActionHi,
      timing: "BEFORE_SOWING"
    });

    // 3. Soil Temperature Parameter Gap
    const tVal = avg.soilTemp || avg.ambientTemp;
    const [tOptMin, tOptMax] = crop.operationalThresholds.soilTempSowingC;
    let tStatus = "SUITABLE";
    let tActionEn = "Temperature is in optimal biological range for seedling emergence.";
    let tActionHi = "अंकुरण व वृद्धि हेतु तापमान अनुकूलतम सीमा में है।";
    let tCritical = false;

    if (tVal < tOptMin) {
      tStatus = "COLD";
      tActionEn = `Soil temperature (${tVal.toFixed(1)}°C) is cold. Delayed germination likely. Consider shallow sowing depth.`;
      tActionHi = `तापमान (${tVal.toFixed(1)}°C) कम है। अंकुरण धीमा हो सकता है। बीज उथला बोएं।`;
    } else if (tVal > tOptMax) {
      tStatus = "HOT";
      tCritical = (crop.cropId === "potato" || crop.cropId === "wheat");
      tActionEn = `Temperature (${tVal.toFixed(1)}°C) is high. Risk of seed tuber rot or forced early emergence.`;
      tActionHi = `तापमान (${tVal.toFixed(1)}°C) अधिक है। बीज सड़ने या सूखने का खतरा।`;
    }

    gapRows.push({
      parameter: "Soil Temperature",
      parameterHi: "मृदा तापमान (°C)",
      fieldValue: tVal > 0 ? `${tVal.toFixed(1)}°C` : "N/A",
      requirement: `${tOptMin}°C – ${tOptMax}°C`,
      status: tStatus,
      critical: tCritical,
      suggestedActionEn: tActionEn,
      suggestedActionHi: tActionHi,
      timing: "AT_SOWING"
    });

    // 4. Nitrogen Index Gap (SN-3002 Relative Sensor)
    const nVal = avg.nitrogen;
    const nTarget = crop.sensorIndexExpectation.nIndexMin;
    let nStatus = nVal >= nTarget ? "ADEQUATE_INDEX" : "DEFICIENT_INDEX";
    gapRows.push({
      parameter: "Nitrogen Index",
      parameterHi: "नाइट्रोजन सूचकांक (सेंसर इंडेक्स)",
      fieldValue: nVal > 0 ? `${Math.round(nVal)} (Unverified Index)` : "N/A",
      requirement: `Target Baseline ≥ ${nTarget}`,
      status: nStatus,
      critical: false,
      suggestedActionEn: nVal >= nTarget
        ? "Sensor nitrogen index is adequate. Apply recommended split basal nitrogen as per regional university package of practices."
        : "Low nitrogen index indicated. Apply split nitrogen (1/3rd basal, 1/3rd at 1st irrigation, 1/3rd at tillering/flowering). Get lab available-N test.",
      suggestedActionHi: nVal >= nTarget
        ? "नाइट्रोजन सूचकांक पर्याप्त है। विश्वविद्यालय संस्तुति अनुसार संतुलित यूरिया का प्रयोग करें।"
        : "नाइट्रोजन स्तर कम प्रतीत हो रहा है। यूरिया को 3 भागों में बांटकर दें (बुवाई, पहली सिंचाई, कल्ले फूटते समय)।",
      timing: "BASAL_AND_TOPDRESSING"
    });

    // 5. Phosphorus Index Gap
    const pVal = avg.phosphorus;
    const pTarget = crop.sensorIndexExpectation.pIndexMin;
    let pStatus = pVal >= pTarget ? "ADEQUATE_INDEX" : "DEFICIENT_INDEX";
    gapRows.push({
      parameter: "Phosphorus Index",
      parameterHi: "फास्फोरस सूचकांक (सेंसर इंडेक्स)",
      fieldValue: pVal > 0 ? `${Math.round(pVal)} (Unverified Index)` : "N/A",
      requirement: `Target Baseline ≥ ${pTarget}`,
      status: pStatus,
      critical: false,
      suggestedActionEn: pVal >= pTarget
        ? "Phosphorus index appears sufficient. Apply basal phosphatic fertilizer (DAP or Single Super Phosphate - SSP supplies 11% Sulfur)."
        : "Low phosphorus index. Apply full recommended P2O5 as basal dose during final ploughing. SSP preferred for oilseeds/pulses.",
      suggestedActionHi: pVal >= pTarget
        ? "फास्फोरस सूचकांक ठीक है। बुवाई के समय बेसल डोज में डीएपी या सिंगल सुपर फास्फेट (SSP) दें।"
        : "फास्फोरस स्तर कम है। बुवाई की अंतिम जुताई में डीएपी या एसएसपी डालें। तिलहन/दलहन में एसएसपी उत्तम है क्योंकि इसमें 11% गंधक (सल्फर) भी होता है।",
      timing: "BEFORE_SOWING"
    });

    // 6. Potassium Index Gap
    const kVal = avg.potassium;
    const kTarget = crop.sensorIndexExpectation.kIndexMin;
    let kStatus = kVal >= kTarget ? "ADEQUATE_INDEX" : "DEFICIENT_INDEX";
    gapRows.push({
      parameter: "Potassium Index",
      parameterHi: "पोटेशियम सूचकांक (सेंसर इंडेक्स)",
      fieldValue: kVal > 0 ? `${Math.round(kVal)} (Unverified Index)` : "N/A",
      requirement: `Target Baseline ≥ ${kTarget}`,
      status: kStatus,
      critical: false,
      suggestedActionEn: kVal >= kTarget
        ? "Potassium index adequate. Apply Muriate of Potash (MOP) as basal application for lodging resistance and drought resilience."
        : "Marginal potassium index. In potato, sugarcane, and vegetables, potassium is critical for tuber size and disease resistance.",
      suggestedActionHi: kVal >= kTarget
        ? "पोटेशियम सूचकांक सामान्य है। बुवाई में पोटाश (MOP) का प्रयोग करें जिससे तना मजबूत रहे और फसल न गिरे।"
        : "पोटाश की मात्रा कम है। आलू, गन्ने व सब्जियों में कंद भराव व चमक हेतु पोटाश अवश्य डालें।",
      timing: "BEFORE_SOWING"
    });

    // Add Standing Crop & Irrigation Management Plans
    crop.waterManagement.criticalStages.forEach(cs => {
      standingCropActions.push({
        titleEn: `Irrigation at ${cs.stageEn} (${cs.das})`,
        titleHi: `${cs.stageHi} पर सिंचाई (${cs.das})`,
        descEn: `${cs.importance} stage for ${crop.cropNameEn}. Drought stress at this stage will cause irrevocable yield loss.`,
        descHi: `${crop.cropNameHi} के लिए यह अति संवेदनशील अवस्था है। इस समय पानी की कमी न होने दें।`,
        timing: "STANDING_CROP",
        critical: cs.importance === "CRITICAL"
      });
    });

    // Mandatory Lab Confirmations
    labTestsNeeded.push(
      "Wet-Chemistry Available Nitrogen (Subbiah & Asija Alkaline Permanganate Method)",
      "Available Phosphorus (Olsen Method for neutral/alkaline soils)",
      "Available Potassium (Ammonium Acetate Flame Photometry)",
      "Organic Carbon % (Walkley-Black Method)",
      "Micronutrients: Zinc (DTPA extractable) and Boron (Hot water soluble)"
    );

    // Compute Overall Readiness
    const criticalIssues = gapRows.filter(r => r.critical);
    let readinessScore = 100 - (criticalIssues.length * 35);
    readinessScore = Math.max(20, Math.min(100, readinessScore));
    let readinessStatus = "READY";
    let readinessLabelEn = "Field Ready for Sowing";
    let readinessLabelHi = "खेत बुवाई हेतु तैयार";

    if (criticalIssues.length > 0) {
      readinessStatus = "ATTENTION_MANDATORY";
      readinessLabelEn = `${criticalIssues.length} Critical Issue(s) Must Be Corrected Before Sowing`;
      readinessLabelHi = `बुवाई से पहले ${criticalIssues.length} मुख्य कमियों को सुधारना अनिवार्य है`;
    }

    return {
      cropId: crop.cropId,
      cropNameEn: crop.cropNameEn,
      cropNameHi: crop.cropNameHi,
      icon: crop.icon,
      season: crop.season,
      sowingWindow: crop.sowingWindow,
      readinessScore,
      readinessStatus,
      readinessLabelEn,
      readinessLabelHi,
      fieldSummary: avg,
      parameterGaps: gapRows,
      preSowingActions,
      standingCropActions,
      mandatoryLabTests: labTestsNeeded,
      recommendedVarietiesUP: crop.varietiesUP,
      limitingFactorsIdentified: crop.limitingFactors,
      scientificSafeguard: "Raw NPK sensor values are unverified relative indices (0-1999). Quantitative fertilizer prescriptions (kg/acre) require certified Soil Health Card laboratory testing."
    };
  }

  // --------------------------------------------------------------------------
  // NUTRIENT AUDIT (Independent N, P, K Analysis)
  // --------------------------------------------------------------------------
  runNutrientAudit() {
    const avg = this.getFieldAverages();
    return {
      timestamp: new Date().toISOString(),
      disclaimerEn: "SN-3002 sensor NPK values represent an unverified relative sensor index (0-1999), not certified wet-chemistry laboratory available nutrients. Do not calculate exact fertilizer kilograms without soil test card confirmation.",
      disclaimerHi: "सेंसर से प्राप्त एनपीके मान एक आपेक्षिक सूचकांक (0-1999) हैं, प्रमाणित प्रयोगशाला उपलब्ध पोषक तत्व नहीं। बिना मृदा स्वास्थ्य कार्ड जांच के रासायनिक उर्वरकों की सटीक किलोग्राम मात्रा तय न करें।",
      nitrogen: {
        rawIndex: Math.round(avg.nitrogen),
        status: avg.nitrogen > 150 ? "HIGH_INDEX" : avg.nitrogen > 60 ? "MODERATE_INDEX" : "LOW_INDEX",
        interpretationEn: avg.nitrogen > 150 ? "Relative nitrogen index is high. Avoid excess urea to prevent vegetative overgrowth and pest lodging." : "Relative nitrogen index is low/moderate. Plan split applications.",
        interpretationHi: avg.nitrogen > 150 ? "नाइट्रोजन सूचकांक उच्च है। अत्यधिक यूरिया से बचें ताकि फसल गिरे नहीं।" : "नाइट्रोजन सूचकांक सामान्य या कम है। यूरिया को किस्तों में दें।"
      },
      phosphorus: {
        rawIndex: Math.round(avg.phosphorus),
        status: avg.phosphorus > 80 ? "HIGH_INDEX" : avg.phosphorus > 35 ? "MODERATE_INDEX" : "LOW_INDEX",
        interpretationEn: "Phosphorus is critical for early root development and tillering. Apply all phosphatic fertilizer as basal dressing during sowing.",
        interpretationHi: "फास्फोरस जड़ों के विकास हेतु अति आवश्यक है। इसकी पूरी मात्रा बुवाई के समय बेसल डोज में दें।"
      },
      potassium: {
        rawIndex: Math.round(avg.potassium),
        status: avg.potassium > 120 ? "HIGH_INDEX" : avg.potassium > 50 ? "MODERATE_INDEX" : "LOW_INDEX",
        interpretationEn: "Potassium confers drought tolerance, insect-pest resistance, and stalk strength.",
        interpretationHi: "पोटाश पौधों को सूखे और रोगों से लड़ने की शक्ति देता है तथा तने को मजबूत बनाता है।"
      },
      organicRecommendations: [
        {
          nameEn: "Well-Rotted Farmyard Manure (FYM)",
          nameHi: "सड़ी गोबर की खाद",
          dose: "10 – 15 tonnes/ha",
          timingEn: "3-4 weeks prior to sowing during field preparation",
          timingHi: "बुवाई से 3-4 सप्ताह पूर्व खेत की तैयारी के समय"
        },
        {
          nameEn: "Vermicompost",
          nameHi: "केंचुआ खाद (वर्मीकम्पोस्ट)",
          dose: "2.5 – 5.0 tonnes/ha",
          timingEn: "During last ploughing or in seed furrows",
          timingHi: "अंतिम जुताई के समय या कतारों में"
        },
        {
          nameEn: "Green Manuring with Dhaincha (Sesbania)",
          nameHi: "ढैंचा हरी खाद",
          dose: "Incorporate at 45 days stage",
          timingEn: "Before Kharif sowing (adds 60-80 kg organic N/ha and lowers pH in sodic soils)",
          timingHi: "धान की रोपाई से पहले (यह 60-80 किग्रा प्राकृतिक नाइट्रोजन देता है और ऊसर सुधारता है)"
        }
      ]
    };
  }

  // --------------------------------------------------------------------------
  // IRRIGATION INTELLIGENCE (Context-Aware Guidance)
  // --------------------------------------------------------------------------
  runIrrigationAssessment(targetCropId) {
    const avg = this.getFieldAverages();
    const m = avg.moisture;
    const cropKey = targetCropId ? targetCropId.toLowerCase().trim() : null;
    const crop = cropKey ? UP_CROP_DATABASE[cropKey] : null;

    let targetMin = 40;
    let targetMax = 70;
    let cropName = "General Field";
    let criticalStages = [];

    if (crop) {
      targetMin = crop.operationalThresholds.moistureSowingPct[0];
      targetMax = crop.operationalThresholds.moistureSowingPct[1];
      cropName = crop.cropNameEn;
      criticalStages = crop.waterManagement.criticalStages;
    }

    let urgency = "NORMAL_MONITORING";
    let recommendationEn = "";
    let recommendationHi = "";

    if (m <= 0) {
      urgency = "DATA_INSUFFICIENT";
      recommendationEn = "No soil moisture reading recorded. Insert probe to evaluate irrigation need.";
      recommendationHi = "नमी का कोई डेटा उपलब्ध नहीं है। जांच हेतु सेंसर लगाएं।";
    } else if (m < targetMin - 15) {
      urgency = "HIGH_IRRIGATE_NOW";
      recommendationEn = `Moisture is critically low at ${m.toFixed(1)}% (Target for ${cropName}: ${targetMin}-${targetMax}%). Irrigate immediately to prevent moisture stress.`;
      recommendationHi = `नमी गंभीर रूप से कम (${m.toFixed(1)}%) है (${cropName} हेतु लक्ष्य: ${targetMin}-${targetMax}%)। तुरंत सिंचाई करें।`;
    } else if (m < targetMin) {
      urgency = "LIGHT_IRRIGATION_PLANNED";
      recommendationEn = `Moisture is moderately depleted (${m.toFixed(1)}%). Plan a light irrigation within 48-72 hours if no rain is expected.`;
      recommendationHi = `नमी कम हो रही है (${m.toFixed(1)}%)। अगले 48-72 घंटों में हल्की सिंचाई का प्रबंध करें।`;
    } else if (m <= targetMax) {
      urgency = "SUFFICIENT_NO_IRRIGATION";
      recommendationEn = `Soil moisture is optimal (${m.toFixed(1)}%). No irrigation needed at present. Continue routine monitoring.`;
      recommendationHi = `नमी उपयुक्त स्तर (${m.toFixed(1)}%) पर है। अभी पानी देने की आवश्यकता नहीं है।`;
    } else {
      urgency = "EXCESS_DRAINAGE_REQUIRED";
      recommendationEn = `Soil is saturated / waterlogged (${m.toFixed(1)}%). Do not irrigate. Open drainage channels if standing water persists.`;
      recommendationHi = `खेत में अत्यधिक पानी/नमी (${m.toFixed(1)}%) है। सिंचाई न करें, जल निकासी सुनिश्चित करें।`;
    }

    return {
      timestamp: new Date().toISOString(),
      currentMoisture: m,
      targetRange: [targetMin, targetMax],
      cropEvaluated: cropName,
      urgency,
      recommendationEn,
      recommendationHi,
      waterSourceConsiderationEn: `Operating with ${this.context.waterSource} in ${this.context.district}. Ensure conveyance efficiency.`,
      waterSourceConsiderationHi: `${this.context.district} में ${this.context.waterSource} द्वारा सिंचाई आधारित सलाह।`,
      criticalStages,
      systemLimitationEn: "Agro-Bot operates measurement-based soil moisture guidance. Forecast-based rain optimization is unavailable as no external weather API is connected. Barometer reflects local atmospheric trend only.",
      systemLimitationHi: "यह सलाह वास्तविक मिट्टी नमी पर आधारित है। बाहरी मौसम पूर्वानुमान API न होने के कारण आगामी वर्षा का पूर्वानुमान उपलब्ध नहीं है।"
    };
  }

  // --------------------------------------------------------------------------
  // FIELD ZONING & SPATIAL VARIABILITY
  // --------------------------------------------------------------------------
  classifyZones() {
    if (!this.samples || this.samples.length < 3) {
      return {
        hasSufficientSamples: false,
        messageEn: "At least 3 geo-tagged sampling points required for spatial zone classification.",
        messageHi: "स्थानिक जोन वर्गीकरण हेतु कम से कम 3 नमूनों की आवश्यकता है।"
      };
    }

    const mStats = this.fieldStats.moisture;
    const phStats = this.fieldStats.ph;

    // Classify each sample node into zone
    const classifiedNodes = this.samples.map((s, idx) => {
      let zoneTag = "ZONE_B_OPTIMAL";
      let zoneLabel = "Zone B: Optimal / Stable";
      let zoneLabelHi = "जोन B: सामान्य व संतुलित";
      let priority = "NORMAL";

      if (s.moisture < 30 || s.ph < 5.8) {
        zoneTag = "ZONE_A_ATTENTION";
        zoneLabel = "Zone A: High Priority Deficiency";
        zoneLabelHi = "जोन A: उच्च प्राथमिकता (नमी/pH कमी)";
        priority = "HIGH";
      } else if (s.moisture > 75 || s.ph > 8.3) {
        zoneTag = "ZONE_C_EXCESS";
        zoneLabel = "Zone C: Excess / Drainage Priority";
        zoneLabelHi = "जोन C: अत्यधिक नमी/क्षारीयता";
        priority = "MEDIUM";
      }

      return {
        sampleId: s.sampleId || `SMP-${idx+1}`,
        row: s.row,
        col: s.col,
        lat: s.lat || 0,
        lng: s.lng || 0,
        gpsValid: s.gpsValid !== undefined ? s.gpsValid : (s.lat !== 0 || s.lng !== 0),
        moisture: s.moisture,
        ph: s.ph,
        n: s.n, p: s.p, k: s.k,
        temp: s.temp,
        zoneTag,
        zoneLabel,
        zoneLabelHi,
        priority
      };
    });

    const isHighVariability = (mStats.cvPct > 20 || phStats.cvPct > 10);

    return {
      hasSufficientSamples: true,
      totalSamples: this.samples.length,
      fieldVariability: {
        moistureCV: mStats.cvPct.toFixed(1) + "%",
        phCV: phStats.cvPct.toFixed(1) + "%",
        isHeterogeneous: isHighVariability,
        assessmentEn: isHighVariability
          ? "High field heterogeneity detected across survey nodes. Variable-rate irrigation or spot soil amendment recommended."
          : "Field is relatively uniform. Uniform agronomic management can be practiced.",
        assessmentHi: isHighVariability
          ? "खेत के अलग-अलग हिस्सों में नमी व pH में बड़ा अंतर पाया गया। चिन्हित स्थानों पर अलग से ध्यान दें।"
          : "खेत अधिकांशतः एक समान है। सामान्य समान प्रबंधन किया जा सकता है।"
      },
      nodes: classifiedNodes
    };
  }

  // --------------------------------------------------------------------------
  // STANDARDIZED TRACEABLE DECISION RECORD GENERATOR
  // --------------------------------------------------------------------------
  generateDecisionRecord(mode, details) {
    const id = "DEC-" + Date.now().toString(36).toUpperCase() + "-" + Math.floor(Math.random()*1000);
    return {
      decisionId: id,
      decisionVersion: this.version,
      timestamp: new Date().toISOString(),
      evaluationMode: mode,
      geographicContext: { ...this.context },
      fieldDataSummary: this.getFieldAverages(),
      traceabilityChain: {
        detectedCondition: details.condition || "General Agronomic Survey",
        evidence: details.evidence || "Multi-sensor field survey data",
        agronomicInterpretation: details.interpretation || "Based on ICAR/UP SAU reference bounds",
        recommendedActionEn: details.actionEn || "Follow package of practices",
        recommendedActionHi: details.actionHi || "अनुशंसित सस्य क्रियाएं अपनाएं",
        confidenceRating: this.samples.length >= 5 ? "HIGH_VALIDATED" : "MODERATE_PROVISIONAL",
        missingInformation: [
          "Laboratory soil test calibration card",
          "Farmer verified subsoil texture",
          "Prior crop residue and fertilizer history"
        ]
      }
    };
  }

  // --------------------------------------------------------------------------
  // BILINGUAL FIELD DIAGNOSTIC REPORT GENERATOR
  // --------------------------------------------------------------------------
  generateReport(lang = 'en') {
    const hi = (lang === 'hi');
    const avg = this.getFieldAverages();
    const discovery = this.runCropDiscovery();
    const nutrients = this.runNutrientAudit();
    const irrigation = this.runIrrigationAssessment();
    const zoning = this.classifyZones();

    return {
      generatedAt: new Date().toLocaleString(hi ? 'hi-IN' : 'en-IN'),
      title: hi ? "एग्रो-बॉट खेत स्वास्थ्य एवं फसल निर्णय रिपोर्ट" : "Agro-Bot Field Intelligence & Crop Decision Report",
      region: `${this.context.district}, ${this.context.state} (${UP_AGRO_ZONES[this.context.zoneId]?.zoneNameEn})`,
      season: this.context.season,
      waterSource: this.context.waterSource,
      fieldSummary: avg,
      discoverySummary: discovery.rankedCrops.slice(0, 5),
      nutrientAudit: nutrients,
      irrigationAdvice: irrigation,
      zoningOverview: zoning,
      scientificSafeguards: {
        npkNotice: hi
          ? "सेंसर NPK केवल आपेक्षिक सूचकांक है। सटीक रासायनिक खाद हेतु सॉइल हेल्थ कार्ड लैब जांच अनिवार्य है।"
          : "Sensor NPK represents an unverified relative index (0-1999). Lab soil test is required for exact fertilizer dosage.",
        probeNotice: hi
          ? "सेंसर का अंदर/बाहर होना केवल सर्वो मोटर के कमांड पर आधारित है, भौतिक पुष्टि सेंसर नहीं है।"
          : "Probe position is software-commanded via servo angle, not physically confirmed by limit switches.",
        weatherNotice: hi
          ? "स्थानीय बैरोमीटर ट्रेंड मात्र है; आधिकारिक मौसम विज्ञान पूर्वानुमान नहीं।"
          : "Barometer provides local barometric pressure trend only; not synoptic meteorological rainfall forecast."
      }
    };
  }

  // --------------------------------------------------------------------------
  // UNIFIED VOICE ASSISTANT (ASK AGRO-BOT) ENGINE
  // --------------------------------------------------------------------------
  getAgrobotAnswer(question, lang = 'hi-IN') {
    const q = (question || "").toLowerCase().trim();
    const hi = lang.startsWith('hi') || lang.startsWith('pa') || lang.startsWith('mr');
    const avg = this.getFieldAverages();
    const pfxHi = avg.isSurvey ? "खेत सर्वे के अनुसार, " : "लाइव सेंसर के अनुसार, ";
    const pfxEn = avg.isSurvey ? "Based on field survey, " : "Based on live sensor, ";

    const has = (kwArr) => kwArr.some(kw => q.includes(kw));

    // 1. IRRIGATION & WATER
    if (has(['irrigat', 'sinchai', 'paani', 'water', 'seench', 'pani', 'सिंचाई', 'पानी', 'सींच', 'दूं', 'देना'])) {
      const irri = this.runIrrigationAssessment();
      return (hi ? pfxHi : pfxEn) + (hi ? irri.recommendationHi : irri.recommendationEn);
    }

    // 2. MOISTURE
    if (has(['moisture', 'nami', 'geela', 'sukha', 'dry', 'wet', 'नमी', 'गीला', 'सूखा'])) {
      const m = avg.moisture;
      if (hi) {
        return `${pfxHi}मिट्टी में नमी ${m.toFixed(1)}% है। ${m < 35 ? 'नमी काफी कम है, सिंचाई की आवश्यकता है।' : m < 65 ? 'नमी बुवाई व सामान्य बढ़वार के लिए अनुकूल है।' : 'मिट्टी में पर्याप्त नमी है, अभी पानी न दें।'}`;
      }
      return `${pfxEn}soil moisture is ${m.toFixed(1)}%. ${m < 35 ? 'Critically low, irrigation required.' : m < 65 ? 'Optimal for cultivation.' : 'Sufficient, no irrigation needed.'}`;
    }

    // 3. SOIL pH
    if (has(['ph', 'acidic', 'alkaline', 'amla', 'kshar', 'tezaab', 'पीएच', 'अम्ल', 'क्षार'])) {
      const p = avg.ph;
      if (hi) {
        return `${pfxHi}मिट्टी का pH मान ${p.toFixed(1)} है। ${p < 5.8 ? 'मिट्टी अम्लीय है, चूना (Lime) मिलाने की सलाह है।' : p > 8.0 ? 'मिट्टी क्षारीय (ऊसर) है, जिप्सम की आवश्यकता है।' : 'pH मान 6.0 से 7.5 के आदर्श दायरे में है, बहुत बढ़िया!'}`;
      }
      return `${pfxEn}soil pH is ${p.toFixed(1)}. ${p < 5.8 ? 'Soil is acidic, agricultural lime recommended.' : p > 8.0 ? 'Soil is alkaline/sodic, gypsum recommended.' : 'pH is within ideal range (6.0-7.5), excellent!'}`;
    }

    // 4. NUTRIENTS & NPK / FERTILIZER
    if (has(['npk', 'nitrogen', 'phospho', 'potass', 'khad', 'urea', 'dap', 'खाद', 'यूरिया', 'नाइट्रोजन', 'फास्फोरस', 'पोटाश'])) {
      const n = Math.round(avg.nitrogen);
      const p = Math.round(avg.phosphorus);
      const k = Math.round(avg.potassium);
      if (hi) {
        return `${pfxHi}सेंसर सूचकांक विश्लेषण: नाइट्रोजन सूचकांक ${n}, फास्फोरस ${p}, पोटेशियम ${k} दर्ज हुआ है। ध्यान रहे कि ये सेंसर इंडेक्स हैं। सटीक रासायनिक खाद के लिए सॉइल हेल्थ कार्ड लैब जांच अवश्य कराएं।`;
      }
      return `${pfxEn}nutrient sensor indices: N=${n}, P=${p}, K=${k} (Relative indices). Certified lab soil test recommended before exact fertilizer application.`;
    }

    // 5. SPECIFIC CROP FEASIBILITY QUERY (e.g. "क्या मैं गेहूँ बो सकता हूँ?")
    for (const cropKey in UP_CROP_DATABASE) {
      const crop = UP_CROP_DATABASE[cropKey];
      const matchers = [cropKey, crop.cropNameEn.toLowerCase(), crop.cropNameHi];
      if (matchers.some(m => q.includes(m.toLowerCase()))) {
        const gap = this.runTargetCropAnalysis(cropKey);
        if (gap.readinessStatus === "READY") {
          return hi
            ? `हाँ, बिल्कुल! ${crop.cropNameHi} (${crop.cropNameEn}) के लिए आपके खेत की स्थिति अनुकूल (तैयारी स्कोर: ${gap.readinessScore}/100) है। संस्तुत किस्में: ${crop.varietiesUP.map(v => v.name).slice(0,3).join(', ')}।`
            : `Yes! Conditions for ${crop.cropNameEn} are suitable (Readiness Score: ${gap.readinessScore}/100). Recommended varieties: ${crop.varietiesUP.map(v => v.name).slice(0,3).join(', ')}.`;
        } else {
          const topIssue = gap.parameterGaps.find(g => g.critical) || gap.parameterGaps[0];
          return hi
            ? `अभी ${crop.cropNameHi} लगाना जोखिम भरा हो सकता है। मुख्य कारण: ${topIssue ? (topIssue.suggestedActionHi || topIssue.parameterHi) : 'नमी या pH असंतुलन'}। बुवाई से पहले इसे सुधारें।`
            : `Planting ${crop.cropNameEn} is not recommended right now. Main issue: ${topIssue ? (topIssue.suggestedActionEn || topIssue.parameter) : 'Moisture/pH gap'}. Rectify before sowing.`;
        }
      }
    }

    // 6. GENERAL CROP RECOMMENDATION ("कौन सी फसल लगाऊं?")
    if (has(['crop', 'fasal', 'ugau', 'lagau', 'ugaye', 'suggest', 'best', 'फसल', 'उगाऊं', 'लगाएं', 'उपयुक्त'])) {
      const disc = this.runCropDiscovery();
      const topCrops = disc.rankedCrops.filter(c => c.isFeasible).slice(0, 3);
      if (topCrops.length === 0) {
        return hi
          ? `वर्तमान खेत स्थितियों में कोई भी फसल बिना मिट्टी सुधार के संस्तुत नहीं है। पहले pH और नमी को संतुलित करें।`
          : `No crops currently meet optimal criteria without soil correction. Please address pH/moisture first.`;
      }
      const namesHi = topCrops.map(c => `${c.cropNameHi} (${c.suitabilityScore}/100)`).join(', ');
      const namesEn = topCrops.map(c => `${c.cropNameEn} (${c.suitabilityScore}/100)`).join(', ');
      return hi
        ? `${pfxHi}आपके खेत और ${this.context.district} के लिए सबसे उपयुक्त फसलें हैं: ${namesHi}।`
        : `${pfxEn}top recommended crops for your field in ${this.context.district} are: ${namesEn}.`;
    }

    // 7. BIGGEST PROBLEM ("मेरी फील्ड में सबसे बड़ी समस्या क्या है?")
    if (has(['problem', 'samasya', 'dikkat', 'issue', 'kharab', 'समस्या', 'दिक्कत', 'कमी', 'खराबी'])) {
      const problems = [];
      if (avg.moisture < 35) problems.push(hi ? `नमी गंभीर रूप से कम (${avg.moisture.toFixed(1)}%) है` : `Moisture is critically low (${avg.moisture.toFixed(1)}%)`);
      if (avg.ph < 5.8) problems.push(hi ? `मिट्टी अम्लीय (pH ${avg.ph.toFixed(1)}) है` : `Soil is acidic (pH ${avg.ph.toFixed(1)})`);
      if (avg.ph > 8.0) problems.push(hi ? `मिट्टी क्षारीय (pH ${avg.ph.toFixed(1)}) है` : `Soil is alkaline (pH ${avg.ph.toFixed(1)})`);
      if (problems.length === 0) {
        return hi
          ? `${pfxHi}खेत में कोई गंभीर समस्या नहीं मिली है! सभी प्राथमिक पैरामीटर सामान्य सीमा में हैं।`
          : `${pfxEn}no major problems detected! Primary parameters are within standard operating ranges.`;
      }
      return (hi ? `${pfxHi}मुख्य समस्याएं पाई गईं: ` : `${pfxEn}primary issues detected: `) + problems.join(hi ? ' और ' : ' and ') + (hi ? '। विस्तृत जानकारी के लिए डैशबोर्ड में टारगेट क्रॉप टैब देखें।' : '. Check Target Crop tab for corrective actions.');
    }

    // 8. GREETING & FALLBACK
    if (has(['hello', 'namaste', 'hi', 'hey', 'kaise', 'नमस्ते', 'नमस्कार', 'प्रणाम'])) {
      return hi
        ? `नमस्ते! मैं एग्रो-बॉट (Agro-Bot) हूँ। आप मुझसे अपने खेत की सिंचाई, उपयुक्त फसल, खाद (NPK), या मिट्टी के pH के बारे में हिंदी या इंग्लिश में पूछ सकते हैं!`
        : `Hello! I am Agro-Bot. Ask me about crop suitability, irrigation needs, soil pH, or nutrients for your field in Uttar Pradesh!`;
    }

    // Default summary response
    return hi
      ? `खेत का वर्तमान डेटा: नमी ${avg.moisture.toFixed(1)}%, pH ${avg.ph.toFixed(1)}, तापमान ${(avg.soilTemp || avg.ambientTemp).toFixed(1)}°C। आप पूछ सकते हैं: 'आज सिंचाई करनी चाहिए?' या 'क्या गेहूँ लगा सकते हैं?'`
      : `Current field readings: Moisture ${avg.moisture.toFixed(1)}%, pH ${avg.ph.toFixed(1)}, Temp ${(avg.soilTemp || avg.ambientTemp).toFixed(1)}°C. You can ask: 'Should I irrigate today?' or 'Is wheat suitable?'`;
  }
}

// Global Export for browser dashboard and Node.js
if (typeof window !== 'undefined') {
  window.UP_AGRO_ZONES = UP_AGRO_ZONES;
  window.UP_CROP_DATABASE = UP_CROP_DATABASE;
  window.computeFieldStats = computeFieldStats;
  window.getCurrentSeason = getCurrentSeason;
  window.classifyParamStatus = classifyParamStatus;
  window.AgroDecisionEngine = AgroDecisionEngine;
}
if (typeof global !== 'undefined') {
  global.UP_AGRO_ZONES = UP_AGRO_ZONES;
  global.UP_CROP_DATABASE = UP_CROP_DATABASE;
  global.computeFieldStats = computeFieldStats;
  global.getCurrentSeason = getCurrentSeason;
  global.classifyParamStatus = classifyParamStatus;
  global.AgroDecisionEngine = AgroDecisionEngine;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { UP_AGRO_ZONES, UP_CROP_DATABASE, computeFieldStats, getCurrentSeason, classifyParamStatus, AgroDecisionEngine };
}

'''

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(js_code)

print("decision_engine.js generated successfully! Size:", os.path.getsize(output_path), "bytes")
