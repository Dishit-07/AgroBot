/**
 * AGRO-BOT MASTER TEST SUITE (Phase 8 Verification)
 * Runs end-to-end agronomic, algorithmic, and boundary test scenarios.
 */

const {
  AgroDecisionEngine,
  UP_CROP_DATABASE,
  UP_AGRO_ZONES,
  computeFieldStats,
  classifyParamStatus
} = require('./dashboard/decision_engine.js');

let passCount = 0;
let failCount = 0;

function assert(condition, testName, details) {
  if (condition) {
    console.log(`✅ PASS: ${testName}`);
    passCount++;
  } else {
    console.error(`❌ FAIL: ${testName} - Details:`, details);
    failCount++;
  }
}

console.log("============================================================");
console.log("AGRO-BOT MASTER DECISION INTELLIGENCE TEST SUITE (PHASE 8)");
console.log("============================================================\n");

// ----------------------------------------------------------------------------
// TEST 1: Optimal Wheat Conditions (Rabi Season, Kanpur Nagar)
// ----------------------------------------------------------------------------
console.log("--- Test Group 1: Optimal Rabi Conditions (Wheat) ---");
const eng1 = new AgroDecisionEngine();
eng1.setContext("Kanpur Nagar", "RABI", "Alluvial Loam", "Tube well");
eng1.ingestSamples([
  { row: 0, col: 0, moisture: 48, ph: 6.8, n: 120, p: 45, k: 80, temp: 21.0, lat: 26.45, lng: 80.33 },
  { row: 0, col: 1, moisture: 50, ph: 6.7, n: 130, p: 50, k: 85, temp: 20.8, lat: 26.45, lng: 80.33 },
  { row: 1, col: 0, moisture: 46, ph: 6.9, n: 115, p: 42, k: 75, temp: 21.2, lat: 26.45, lng: 80.33 }
]);

const disc1 = eng1.runCropDiscovery();
const topCrop1 = disc1.rankedCrops[0];
assert(topCrop1.cropId === 'wheat', "Wheat ranks #1 under optimal Rabi conditions", topCrop1);
assert(topCrop1.suitabilityScore >= 90, "Wheat receives high score (>=90)", topCrop1.suitabilityScore);
assert(topCrop1.suitabilityTag === 'HIGHLY_SUITABLE', "Wheat tagged HIGHLY_SUITABLE", topCrop1.suitabilityTag);

const gap1 = eng1.runTargetCropAnalysis('wheat');
assert(gap1.readinessStatus === 'READY', "Target crop readiness is READY", gap1.readinessStatus);
assert(gap1.preSowingActions.length === 0, "No pre-sowing chemical amendments needed", gap1.preSowingActions);

const irri1 = eng1.runIrrigationAssessment('wheat');
assert(irri1.urgency === 'SUFFICIENT_NO_IRRIGATION', "Irrigation correctly identifies sufficient moisture", irri1.urgency);

// ----------------------------------------------------------------------------
// TEST 2: Acidic & Drought-Stressed Soil (pH 5.2, Moisture 18%)
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 2: Acidic & Drought Stress (pH 5.2, M 18%) ---");
const eng2 = new AgroDecisionEngine();
eng2.setContext("Mirzapur", "RABI", "Red Sandy", "Rain-fed");
eng2.ingestSamples([
  { row: 0, col: 0, moisture: 18, ph: 5.2, n: 30, p: 15, k: 25, temp: 23.0, lat: 25.13, lng: 82.56 },
  { row: 0, col: 1, moisture: 19, ph: 5.3, n: 35, p: 18, k: 30, temp: 22.8, lat: 25.13, lng: 82.56 }
]);

const disc2 = eng2.runCropDiscovery();
const wheatIn2 = disc2.rankedCrops.find(c => c.cropId === 'wheat');
assert(wheatIn2.suitabilityScore < 50, "Wheat heavily penalized under severe acidity/drought", wheatIn2.suitabilityScore);
assert(wheatIn2.limitingFactors.some(l => l.severity === 'CRITICAL'), "Critical limiting factors flagged for Wheat", wheatIn2.limitingFactors);

const gap2 = eng2.runTargetCropAnalysis('wheat');
assert(gap2.readinessStatus === 'ATTENTION_MANDATORY', "Gap analysis status is ATTENTION_MANDATORY", gap2.readinessStatus);
assert(gap2.preSowingActions.some(a => a.titleEn.includes('Lime')), "Mandatory Lime application prescribed", gap2.preSowingActions);
assert(gap2.preSowingActions.some(a => a.titleEn.includes('Palewa')), "Mandatory Palewa irrigation prescribed", gap2.preSowingActions);

const voiceWheat2 = eng2.getAgrobotAnswer("क्या मैं गेहूँ लगा सकता हूँ?", "hi-IN");
assert(voiceWheat2.includes("जोखिम") || voiceWheat2.includes("अम्लीय"), "Agro-Bot voice bot warns against planting wheat in acidic soil", voiceWheat2);

// ----------------------------------------------------------------------------
// TEST 3: Alkaline / Sodic Soil (pH 8.6 in Central UP)
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 3: Alkaline / Sodic Soil (pH 8.6, Central UP) ---");
const eng3 = new AgroDecisionEngine();
eng3.setContext("Unnao", "RABI", "Sodic / Alkaline", "Canal");
eng3.ingestSamples([
  { row: 0, col: 0, moisture: 52, ph: 8.6, n: 60, p: 25, k: 50, temp: 20.0, lat: 26.54, lng: 80.49 }
]);

const gap3 = eng3.runTargetCropAnalysis('wheat');
assert(gap3.preSowingActions.some(a => a.titleEn.includes('Gypsum')), "Gypsum application prescribed for alkaline sodic soil", gap3.preSowingActions);
assert(gap3.mandatoryLabTests.some(t => t.includes('Sodium Percentage')), "ESP laboratory testing mandated", gap3.mandatoryLabTests);

// ----------------------------------------------------------------------------
// TEST 4: Saturated / Waterlogged Soil (Moisture 92%)
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 4: Waterlogged Soil (Moisture 92%) ---");
const eng4 = new AgroDecisionEngine();
eng4.setContext("Gorakhpur", "KHARIF", "Clay Loam", "Tube well");
eng4.ingestSamples([
  { row: 0, col: 0, moisture: 92, ph: 6.8, n: 80, p: 40, k: 60, temp: 28.0, lat: 26.76, lng: 83.37 }
]);

const disc4 = eng4.runCropDiscovery();
const rice4 = disc4.rankedCrops.find(c => c.cropId === 'rice');
const chickpea4 = disc4.rankedCrops.find(c => c.cropId === 'chickpea');
assert(rice4.isFeasible === true && rice4.suitabilityScore >= 80, "Rice is suitable under high water availability", rice4);
assert(chickpea4.isFeasible === false || chickpea4.suitabilityScore < 40, "Chickpea is rejected under saturated soil", chickpea4);

const irri4Rice = eng4.runIrrigationAssessment('rice');
assert(irri4Rice.urgency === 'SUFFICIENT_NO_IRRIGATION', "Rice irrigation acknowledges 92% moisture as sufficient for paddy", irri4Rice.urgency);

const irri4Chickpea = eng4.runIrrigationAssessment('chickpea');
assert(irri4Chickpea.urgency === 'EXCESS_DRAINAGE_REQUIRED', "Chickpea irrigation correctly flags 92% moisture as EXCESS_DRAINAGE_REQUIRED", irri4Chickpea.urgency);


// ----------------------------------------------------------------------------
// TEST 5: Zero Data / Uninserted Probe Boundary Handling
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 5: Zero Data Boundary Safety ---");
const eng5 = new AgroDecisionEngine();
eng5.ingestLiveData({}); // zero readings
eng5.ingestSamples([]);   // empty samples

const disc5 = eng5.runCropDiscovery();
assert(Array.isArray(disc5.rankedCrops) && disc5.rankedCrops.length > 0, "Crop discovery handles zero data gracefully without crashing", disc5.rankedCrops.length);
assert(disc5.rankedCrops[0].confidence.includes("MODERATE") || disc5.rankedCrops[0].confidence.includes("SINGLE"), "Confidence reduced when no survey data present", disc5.rankedCrops[0].confidence);

const irri5 = eng5.runIrrigationAssessment();
assert(irri5.urgency === 'DATA_INSUFFICIENT', "Irrigation intelligence reports DATA_INSUFFICIENT on 0 moisture", irri5.urgency);

// ----------------------------------------------------------------------------
// TEST 6: Season Mismatch Gate
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 6: Season Mismatch Gate ---");
const eng6 = new AgroDecisionEngine();
eng6.setContext("Kanpur Nagar", "RABI", "Alluvial Loam", "Tube well");
eng6.ingestSamples([
  { row: 0, col: 0, moisture: 80, ph: 6.5, n: 80, p: 40, k: 50, temp: 20.0, lat: 26.45, lng: 80.33 }
]);

const disc6 = eng6.runCropDiscovery();
const rice6 = disc6.rankedCrops.find(c => c.cropId === 'rice');
assert(rice6.limitingFactors.some(l => l.param === 'Season Window'), "Rice flagged with season mismatch alert in Rabi", rice6.limitingFactors);

// ----------------------------------------------------------------------------
// TEST 7: Invalid GPS Handling
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 7: Invalid GPS Nodes ---");
const eng7 = new AgroDecisionEngine();
eng7.ingestSamples([
  { row: 0, col: 0, moisture: 45, ph: 6.5, n: 90, p: 40, k: 60, temp: 20.0, lat: 0, lng: 0, gpsValid: false },
  { row: 0, col: 1, moisture: 48, ph: 6.6, n: 95, p: 42, k: 65, temp: 20.2, lat: 0, lng: 0, gpsValid: false },
  { row: 1, col: 0, moisture: 46, ph: 6.4, n: 85, p: 38, k: 58, temp: 20.1, lat: 0, lng: 0, gpsValid: false }
]);

const zones7 = eng7.classifyZones();
assert(zones7.hasSufficientSamples === true, "Zoning functions with grid coordinates even when GPS is 0", zones7.hasSufficientSamples);
assert(zones7.nodes.every(n => n.gpsValid === false), "GPS invalidity preserved per node", zones7.nodes[0]);

// ----------------------------------------------------------------------------
// TEST 8: Field Spatial Heterogeneity Classification
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 8: Spatial Field Heterogeneity Classification ---");
const eng8 = new AgroDecisionEngine();
eng8.ingestSamples([
  { row: 0, col: 0, moisture: 22, ph: 5.4, n: 40, p: 20, k: 30, temp: 20, lat: 26.45, lng: 80.33 }, // Deficient
  { row: 0, col: 1, moisture: 50, ph: 6.8, n: 120, p: 45, k: 80, temp: 20, lat: 26.45, lng: 80.33 }, // Optimal
  { row: 1, col: 0, moisture: 82, ph: 7.2, n: 140, p: 55, k: 90, temp: 20, lat: 26.45, lng: 80.33 }  // Excess
]);

const zones8 = eng8.classifyZones();
assert(zones8.fieldVariability.isHeterogeneous === true, "High CV detected and field classified as heterogeneous", zones8.fieldVariability);
assert(zones8.nodes.some(n => n.zoneTag === 'ZONE_A_ATTENTION'), "Zone A (deficiency) node identified", zones8.nodes);
assert(zones8.nodes.some(n => n.zoneTag === 'ZONE_B_OPTIMAL'), "Zone B (optimal) node identified", zones8.nodes);
assert(zones8.nodes.some(n => n.zoneTag === 'ZONE_C_EXCESS'), "Zone C (excess) node identified", zones8.nodes);

// ----------------------------------------------------------------------------
// TEST 9: Voice Assistant Bilingual & Script Alignment
// ----------------------------------------------------------------------------
console.log("\n--- Test Group 9: Voice Assistant Multi-Script Integration ---");
const eng9 = new AgroDecisionEngine();
eng9.setContext("Kanpur Nagar", "RABI", "Alluvial Loam", "Tube well");
eng9.ingestSamples([
  { row: 0, col: 0, moisture: 24, ph: 5.5, n: 60, p: 30, k: 50, temp: 21, lat: 26.45, lng: 80.33 }
]);

const ansHindiIrri = eng9.getAgrobotAnswer("सिंचाई करनी चाहिए?", "hi-IN");
assert(ansHindiIrri.includes("तुरंत") || ansHindiIrri.includes("सिंचाई"), "Hindi irrigation query replies in native Hindi", ansHindiIrri);

const ansHindiProblem = eng9.getAgrobotAnswer("खेत में सबसे बड़ी समस्या क्या है?", "hi-IN");
assert(ansHindiProblem.includes("समस्याएं") || ansHindiProblem.includes("नमी"), "Hindi problem query flags moisture/pH", ansHindiProblem);

const ansEnIrri = eng9.getAgrobotAnswer("should i irrigate my field?", "en-IN");
assert(ansEnIrri.includes("Irrigate") || ansEnIrri.includes("Moisture"), "English query returns coherent English advice", ansEnIrri);

console.log("\n============================================================");
console.log(`TEST SUMMARY: ${passCount} PASSED, ${failCount} FAILED`);
console.log("============================================================");

if (failCount > 0) process.exit(1);
