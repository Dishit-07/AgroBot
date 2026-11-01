# -*- coding: utf-8 -*-
"""
Assembles the complete 12 pages and JavaScript integration in D:\Graphic hackathon\rover\dashboard\v1.html
"""

import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

target_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'v1.html')

with open(target_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Let's extract page0, page1, page2, page3, page4, page5, page6
p0_start = html.find('<div class="page active" id="page0">')
p1_start = html.find('<div class="page" id="page1">')
p2_start = html.find('<div class="page" id="page2">')
p3_start = html.find('<div class="page" id="page3">')
p4_start = html.find('<div class="page" id="page4">')
p5_start = html.find('<div class="page" id="page5">')
p6_start = html.find('<div class="page" id="page6">')
main_end = html.find('</main>')

page0_html = html[p0_start:p1_start]
page1_html = html[p1_start:p2_start]
page2_html = html[p2_start:p3_start]
page3_old_html = html[p3_start:p4_start] # Rover Control
page4_old_html = html[p4_start:p5_start] # Auto Mapping
page5_old_html = html[p5_start:p6_start] # Field Results
page6_old_html = html[p6_start:main_end]  # Ask Agro-Bot

print("Extracted existing page blocks cleanly.")

# Page 1 Enhancement: Add Spatial Field Zoning card inside Page 1
page1_enhanced = page1_html.replace(
    '<!-- Live Trail & Heading Map -->',
    '''<!-- Spatial Field Zoning Overlay Card -->
            <div class="card span-full">
              <div class="card-title"><span class="icon">🗺️</span>Spatial Field Zoning &amp; Heterogeneity</div>
              <p style="color:var(--text-secondary);font-size:0.84rem;margin:0 0 14px;">
                Identifies field variation across GPS-tagged sample nodes. Classifies field into management zones based on Moisture and pH Coefficient of Variation (CV).
              </p>
              <div id="fieldZoningOverview">
                <div style="color:var(--text-muted);font-size:0.85rem;padding:12px;background:rgba(0,0,0,0.02);border-radius:8px;">
                  Run an autonomous mapping survey to generate spatial zone classification and soil variability analysis.
                </div>
              </div>
            </div>

            <!-- Live Trail & Heading Map -->'''
)

# Page 2 Enhancement: Add Unverified NPK Sensor Notice in Page 2
page2_enhanced = page2_html.replace(
    '<div class="card span-full">',
    '''<div class="card span-full">
              <div class="safeguard-banner">
                <b>⚠️ Scientific Safeguard Notice — Soil NPK Sensor Units:</b><br>
                Raw Nitrogen, Phosphorus, and Potassium readings from the SN-3002 sensor represent an <b>Unverified Sensor Index (0–1999)</b>, not certified wet-chemistry laboratory available nutrients (Alkaline Permanganate N, Olsen P, or Ammonium Acetate K). Do not calculate exact chemical fertilizer dosages from raw sensor values without laboratory validation.
              </div>'''
)

# New Page 3: Crop Discovery (Mode A - "What should I grow?")
page3_new_html = """
        <!-- ============================================================
             PAGE 3: CROP DISCOVERY (MODE A)
             ============================================================ -->
        <div class="page" id="page3">
          <!-- Regional Context Bar -->
          <div class="context-bar">
            <div class="context-item">
              <label for="districtSelect">UP District / Zone</label>
              <select id="districtSelect" class="context-select" onchange="updateContext()">
                <optgroup label="UP-Z1: Tarai Zone">
                  <option value="Lakhimpur Kheri">Lakhimpur Kheri</option>
                  <option value="Bahraich">Bahraich</option>
                  <option value="Balrampur">Balrampur</option>
                  <option value="Pilibhit">Pilibhit</option>
                  <option value="Rampur">Rampur</option>
                  <option value="Bareilly">Bareilly</option>
                  <option value="Siddharthnagar">Siddharthnagar</option>
                </optgroup>
                <optgroup label="UP-Z2: Western Plain">
                  <option value="Meerut">Meerut</option>
                  <option value="Bulandshahr">Bulandshahr</option>
                  <option value="Muzaffarnagar">Muzaffarnagar</option>
                  <option value="Saharanpur">Saharanpur</option>
                  <option value="Baghpat">Baghpat</option>
                  <option value="Ghaziabad">Ghaziabad</option>
                </optgroup>
                <optgroup label="UP-Z3: Mid-Western Plain">
                  <option value="Badaun">Badaun</option>
                  <option value="Shahjahanpur">Shahjahanpur</option>
                  <option value="Moradabad">Moradabad</option>
                  <option value="Bijnor">Bijnor</option>
                  <option value="Sambhal">Sambhal</option>
                </optgroup>
                <optgroup label="UP-Z4: South-Western Semi-Arid">
                  <option value="Agra">Agra</option>
                  <option value="Mathura">Mathura</option>
                  <option value="Aligarh">Aligarh</option>
                  <option value="Mainpuri">Mainpuri</option>
                  <option value="Firozabad">Firozabad</option>
                  <option value="Hathras">Hathras</option>
                </optgroup>
                <optgroup label="UP-Z5: Central Plain" selected>
                  <option value="Kanpur Nagar" selected>Kanpur Nagar</option>
                  <option value="Kanpur Dehat">Kanpur Dehat</option>
                  <option value="Lucknow">Lucknow</option>
                  <option value="Unnao">Unnao</option>
                  <option value="Fatehpur">Fatehpur</option>
                  <option value="Rae Bareli">Rae Bareli</option>
                  <option value="Sitapur">Sitapur</option>
                  <option value="Hardoi">Hardoi</option>
                  <option value="Barabanki">Barabanki</option>
                </optgroup>
                <optgroup label="UP-Z6: Bundelkhand Zone">
                  <option value="Jhansi">Jhansi</option>
                  <option value="Lalitpur">Lalitpur</option>
                  <option value="Jalaun">Jalaun</option>
                  <option value="Hamirpur">Hamirpur</option>
                  <option value="Mahoba">Mahoba</option>
                  <option value="Banda">Banda</option>
                  <option value="Chitrakoot">Chitrakoot</option>
                </optgroup>
                <optgroup label="UP-Z7: North Eastern Plain">
                  <option value="Gorakhpur">Gorakhpur</option>
                  <option value="Deoria">Deoria</option>
                  <option value="Basti">Basti</option>
                  <option value="Kushinagar">Kushinagar</option>
                  <option value="Maharajganj">Maharajganj</option>
                </optgroup>
                <optgroup label="UP-Z8: Eastern Plain">
                  <option value="Varanasi">Varanasi</option>
                  <option value="Jaunpur">Jaunpur</option>
                  <option value="Ghazipur">Ghazipur</option>
                  <option value="Azamgarh">Azamgarh</option>
                  <option value="Ballia">Ballia</option>
                  <option value="Ayodhya">Ayodhya</option>
                  <option value="Sultanpur">Sultanpur</option>
                  <option value="Pratapgarh">Pratapgarh</option>
                </optgroup>
                <optgroup label="UP-Z9: Vindhyan Zone">
                  <option value="Mirzapur">Mirzapur</option>
                  <option value="Sonbhadra">Sonbhadra</option>
                  <option value="Prayagraj">Prayagraj</option>
                </optgroup>
              </select>
            </div>

            <div class="context-item">
              <label for="seasonSelect">Current Sowing Season</label>
              <select id="seasonSelect" class="context-select" onchange="updateContext()">
                <option value="RABI" selected>Rabi (Winter: Oct - Mar)</option>
                <option value="KHARIF">Kharif (Monsoon: Jun - Oct)</option>
                <option value="ZAID">Zaid (Summer: Mar - Jun)</option>
              </select>
            </div>

            <div class="context-item">
              <label for="waterSelect">Available Irrigation Source</label>
              <select id="waterSelect" class="context-select" onchange="updateContext()">
                <option value="Tube well" selected>Tube well / Borewell (Assured)</option>
                <option value="Canal">Canal Irrigation (Seasonal)</option>
                <option value="Rain-fed">Rain-fed / Dryland (No Tubewell)</option>
                <option value="Multiple sources">Multiple (Tubewell + Canal)</option>
              </select>
            </div>

            <div class="context-item">
              <label for="soilTypeSelect">Field Soil Type (Optional)</label>
              <select id="soilTypeSelect" class="context-select" onchange="updateContext()">
                <option value="Unknown" selected>Unknown (Auto-Inferred)</option>
                <option value="Alluvial Loam">Alluvial Loam (दोमट)</option>
                <option value="Sandy Loam">Sandy Loam (बलुई दोमट)</option>
                <option value="Clay Loam">Clay Loam (मटियार दोमट)</option>
                <option value="Sodic / Alkaline">Sodic / Usar (ऊसर/क्षारीय)</option>
                <option value="Black Clay (Kabar/Mar)">Black Clay / Karail (काबर/मार)</option>
                <option value="Red Gravelly (Rakar)">Red Sandy / Rakar (राकड़)</option>
              </select>
            </div>

            <div style="display:flex;align-items:flex-end;">
              <button class="btn btn-primary" onclick="renderCropDiscovery()" style="padding:9px 18px;font-size:0.85rem;">
                🔄 Run Crop Discovery
              </button>
            </div>
          </div>

          <!-- Mode A Header -->
          <div class="section-card" style="margin-bottom:18px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
              <div>
                <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
                  🌾 Mode A: Crop Discovery ("What should I grow?")
                </h2>
                <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
                  Ranked suitability of Uttar Pradesh crops evaluated against field measured moisture, pH, temperature, seasonal window, and regional agro-climatic adaptability.
                </p>
              </div>
              <div id="discoveryFieldSummaryBadge" style="font-size:0.82rem;font-weight:700;padding:6px 12px;background:rgba(34,197,94,0.1);color:#16a34a;border-radius:8px;">
                Field Data Synced
              </div>
            </div>
          </div>

          <!-- Crop Discovery Cards Container -->
          <div class="crop-discovery-grid" id="cropDiscoveryGrid">
            <!-- Dynamically populated by renderCropDiscovery() -->
          </div>
        </div>
"""

# New Page 4: Target Crop Analysis (Mode B - "I want to grow X. What to improve?")
page4_new_html = """
        <!-- ============================================================
             PAGE 4: TARGET CROP GAP ANALYSIS (MODE B)
             ============================================================ -->
        <div class="page" id="page4">
          <!-- Crop Selector Header Card -->
          <div class="section-card" style="margin-bottom:18px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;">
              <div>
                <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
                  🎯 Mode B: Target Crop Soil Gap Analysis &amp; Action Plan
                </h2>
                <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
                  Select a specific crop to generate a parameter-by-parameter readiness gap analysis and step-by-step pre-sowing improvement plan.
                </p>
              </div>

              <div style="display:flex;align-items:center;gap:10px;">
                <label style="font-size:0.85rem;font-weight:700;color:var(--text-primary);">Target Crop:</label>
                <select id="targetCropDropdown" class="context-select" onchange="renderTargetCropAnalysis()" style="font-size:0.95rem;padding:8px 16px;">
                  <option value="wheat" selected>🌾 Wheat (गेहूँ)</option>
                  <option value="rice">🌾 Rice / Paddy (धान)</option>
                  <option value="sugarcane">🎋 Sugarcane (गन्ना)</option>
                  <option value="mustard">🌼 Mustard / Sarson (सरसों)</option>
                  <option value="potato">🥔 Potato (आलू)</option>
                  <option value="chickpea">🫘 Chickpea / Chana (चना)</option>
                  <option value="pigeonpea">🫛 Pigeonpea / Arhar (अरहर)</option>
                  <option value="maize">🌽 Maize / Corn (मक्का)</option>
                  <option value="lentil">🫘 Lentil / Masoor (मसूर)</option>
                  <option value="moong">🫛 Green Gram / Moong (मूंग)</option>
                  <option value="bajra">🌾 Pearl Millet / Bajra (बाजरा)</option>
                  <option value="tomato">🍅 Tomato (टमाटर)</option>
                  <option value="onion">🧅 Onion (प्याज)</option>
                  <option value="garlic">🧄 Garlic (लहसुन)</option>
                  <option value="sesame">🌱 Sesame / Til (तिल)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Dynamic Target Crop Results Container -->
          <div id="targetCropAnalysisContainer">
            <!-- Dynamically populated by renderTargetCropAnalysis() -->
          </div>
        </div>
"""

# New Page 5: Nutrient Management
page5_new_html = """
        <!-- ============================================================
             PAGE 5: NUTRIENT MANAGEMENT
             ============================================================ -->
        <div class="page" id="page5">
          <div class="safeguard-banner">
            <b>⚠️ Scientific Safeguard Notice — Soil NPK Sensor Units:</b><br>
            Raw Nitrogen, Phosphorus, and Potassium readings from the SN-3002 sensor represent an <b>Unverified Sensor Index (0–1999)</b>, not certified wet-chemistry laboratory available nutrients (Alkaline Permanganate N, Olsen P, or Ammonium Acetate K). Do not calculate exact chemical fertilizer dosages from raw sensor values without laboratory validation.
          </div>

          <div class="section-card" style="margin-bottom:18px;">
            <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
              🌿 Independent Nitrogen, Phosphorus &amp; Potassium Intelligence
            </h2>
            <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
              Independent multi-parameter nutrient condition monitoring with organic buffering recommendations.
            </p>
          </div>

          <div class="nutrient-grid" id="nutrientPanelsGrid">
            <!-- Dynamically populated by renderNutrientManagement() -->
          </div>

          <!-- Organic Amendment Card -->
          <div class="card span-full" style="margin-top:20px;">
            <div class="card-title"><span class="icon">🌱</span>Recommended Organic Soil Amendment Guidelines (UP Package of Practices)</div>
            <div class="grid-3" style="margin-top:12px;">
              <div class="action-card good">
                <div class="action-card-title">Well-Rotted Farmyard Manure (FYM)</div>
                <div class="action-card-desc">
                  <b>Dose:</b> 10 – 15 tonnes/ha<br>
                  <b>Timing:</b> 3-4 weeks before sowing during primary tillage.<br>
                  <b>Impact:</b> Improves organic carbon, water retention, and microbial buffering against extreme pH.
                </div>
              </div>

              <div class="action-card good">
                <div class="action-card-title">Vermicompost (केंचुआ खाद)</div>
                <div class="action-card-desc">
                  <b>Dose:</b> 2.5 – 5.0 tonnes/ha<br>
                  <b>Timing:</b> Basal application during final seedbed preparation.<br>
                  <b>Impact:</b> Supplies readily available macro &amp; micro nutrients with humic substances.
                </div>
              </div>

              <div class="action-card good">
                <div class="action-card-title">Green Manuring (Dhaincha / ढैंचा)</div>
                <div class="action-card-desc">
                  <b>Dose:</b> Incorporate 45-day standing crop.<br>
                  <b>Timing:</b> Prior to Kharif rice transplanting.<br>
                  <b>Impact:</b> Adds 60-80 kg N/ha, lowers pH in sodic Usar soils, and improves soil structure.
                </div>
              </div>
            </div>
          </div>
        </div>
"""

# New Page 6: Irrigation Intelligence
page6_new_html = """
        <!-- ============================================================
             PAGE 6: IRRIGATION INTELLIGENCE
             ============================================================ -->
        <div class="page" id="page6">
          <div class="section-card" style="margin-bottom:18px;">
            <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
              💧 Measurement-Based Irrigation Intelligence
            </h2>
            <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
              Context-aware irrigation recommendations based on measured soil moisture, target crop water demands, growth stages, and water source conveyance.
            </p>
          </div>

          <div class="grid-2">
            <!-- Live Moisture & Urgency Card -->
            <div class="card" id="irrigationUrgencyCard">
              <!-- Dynamically populated by renderIrrigationIntelligence() -->
            </div>

            <!-- Critical Irrigation Stages Timeline Card -->
            <div class="card" id="irrigationStagesCard">
              <!-- Dynamically populated by renderIrrigationIntelligence() -->
            </div>
          </div>

          <div class="card span-full" style="margin-top:18px;">
            <div class="card-title"><span class="icon">ℹ️</span>System Meteorological Limitations &amp; Irrigation Safeguards</div>
            <p style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;margin:0;">
              <b>No External Weather Forecast API:</b> Agro-Bot currently operates without external satellite or synoptic weather API feeds. The onboard BMP180 barometric sensor provides localized pressure trends only and cannot substitute for verified meteorological rainfall forecasts.<br>
              <b>Measurement-Driven:</b> Irrigation advice reflects physically measured volumetric soil moisture (%) at probe insertion depth. Adjust irrigation timing if seasonal rainfall is visibly imminent.
            </p>
          </div>
        </div>
"""

# Page 7: Rover Control (replaces old page3)
page7_html = page3_old_html.replace('id="page3"', 'id="page7"')

# Page 8: Auto Mapping (replaces old page4)
page8_html = page4_old_html.replace('id="page4"', 'id="page8"')

# Page 9: Sampling History (was part of page5)
page9_html = """
        <!-- ============================================================
             PAGE 9: SAMPLING HISTORY
             ============================================================ -->
        <div class="page" id="page9">
          <div class="section-card" style="margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
                📋 Field Sampling History &amp; Spatial Logs
              </h2>
              <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
                Historical record of all geo-tagged soil sample points captured during autonomous mapping surveys.
              </p>
            </div>
            <div style="display:flex;gap:10px;">
              <button class="btn btn-primary" onclick="exportSamplesCSV()" style="padding:8px 16px;font-size:0.85rem;">
                📥 Export CSV
              </button>
            </div>
          </div>

          <div class="card span-full">
            <div class="table-wrap">
              <table class="data-table" id="samplingHistoryTable">
                <thead>
                  <tr>
                    <th>Sample ID</th>
                    <th>Grid Node</th>
                    <th>GPS Coordinates</th>
                    <th>Moisture (%)</th>
                    <th>Soil Temp (°C)</th>
                    <th>Soil pH</th>
                    <th>N Index</th>
                    <th>P Index</th>
                    <th>K Index</th>
                    <th>Quality</th>
                  </tr>
                </thead>
                <tbody id="samplingHistoryTableBody">
                  <tr><td colspan="10" style="text-align:center;color:var(--text-muted);padding:24px;">No samples recorded yet. Run an Auto Mapping mission to collect field survey points.</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
"""

# Page 10: Ask Agro-Bot (was page6)
page10_html = page6_old_html.replace('id="page6"', 'id="page10"')

# Page 11: Reports & Laboratory Comparison
page11_html = """
        <!-- ============================================================
             PAGE 11: FIELD REPORTS & LAB VALIDATION
             ============================================================ -->
        <div class="page" id="page11">
          <div class="section-card" style="margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <h2 style="margin:0 0 4px;font-size:1.3rem;font-weight:700;color:var(--text-primary);">
                📑 Field Diagnostic Report &amp; Soil Lab Validation
              </h2>
              <p style="margin:0;color:var(--text-secondary);font-size:0.85rem;">
                Generate comprehensive bilingual diagnostic field reports and record laboratory comparison validation data.
              </p>
            </div>
            <div style="display:flex;gap:10px;">
              <button class="btn btn-secondary" onclick="window.print()" style="padding:8px 16px;font-size:0.85rem;">
                🖨️ Print Report
              </button>
              <button class="btn btn-primary" onclick="downloadReportHTML()" style="padding:8px 16px;font-size:0.85rem;">
                💾 Download HTML Report
              </button>
            </div>
          </div>

          <!-- Report Preview Box -->
          <div class="card span-full" id="reportPreviewCard" style="background:#fff;color:#1e293b;padding:28px;box-shadow:var(--shadow-md);">
            <!-- Dynamically populated by renderFieldReport() -->
          </div>

          <!-- Laboratory Soil Test Card Validation Interface -->
          <div class="card span-full" style="margin-top:20px;">
            <div class="card-title"><span class="icon">🔬</span>Laboratory Soil Health Card Comparison &amp; Sensor Calibration Log</div>
            <p style="font-size:0.84rem;color:var(--text-secondary);margin:0 0 14px;">
              Record certified wet-chemistry soil test results from Krishi Vigyan Kendra (KVK) or government soil testing laboratories to validate on-board rover sensor calibration.
            </p>
            <div class="grid-3">
              <div class="context-item">
                <label>Testing Laboratory Name</label>
                <input type="text" id="labNameInput" class="context-select" placeholder="e.g. KVK Kanpur Soil Lab">
              </div>
              <div class="context-item">
                <label>Soil Test Report / Sample ID</label>
                <input type="text" id="labReportIdInput" class="context-select" placeholder="e.g. SHC-2026-9081">
              </div>
              <div class="context-item">
                <label>Lab Organic Carbon (%)</label>
                <input type="number" step="0.01" id="labOcInput" class="context-select" placeholder="e.g. 0.55%">
              </div>
              <div class="context-item">
                <label>Lab Measured pH</label>
                <input type="number" step="0.1" id="labPhInput" class="context-select" placeholder="e.g. 7.2">
              </div>
              <div class="context-item">
                <label>Lab Available Nitrogen (kg/ha)</label>
                <input type="number" id="labNInput" class="context-select" placeholder="e.g. 210 kg/ha">
              </div>
              <div class="context-item">
                <label>Lab Available P (kg/ha)</label>
                <input type="number" id="labPInput" class="context-select" placeholder="e.g. 18 kg/ha">
              </div>
              <div class="context-item">
                <label>Lab Available K (kg/ha)</label>
                <input type="number" id="labKInput" class="context-select" placeholder="e.g. 240 kg/ha">
              </div>
              <div class="context-item" style="display:flex;align-items:flex-end;">
                <button class="btn btn-primary" onclick="saveLabComparison()" style="width:100%;padding:10px;">
                  💾 Save Lab Comparison Record
                </button>
              </div>
            </div>
            <div id="labComparisonLog" style="margin-top:14px;font-size:0.85rem;"></div>
          </div>
        </div>
"""

# Assemble all 12 pages in main
new_main_content = (
    page0_html +
    page1_enhanced +
    page2_enhanced +
    page3_new_html +
    page4_new_html +
    page5_new_html +
    page6_new_html +
    page7_html +
    page8_html +
    page9_html +
    page10_html +
    page11_html
)

# Replace the main content in html
main_start = html.find('<div class="page active" id="page0">')
html = html[:main_start] + new_main_content + html[main_end:]
print("All 12 pages assembled in HTML!")

# Write updated HTML
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Part 2 completed! File size:", os.path.getsize(target_path))
