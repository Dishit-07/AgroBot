# -*- coding: utf-8 -*-
"""
Wires decision_engine.js and the UI rendering functions into D:\Graphic hackathon\rover\dashboard\v1.html
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

target_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'v1.html')

with open(target_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add <script src="decision_engine.js"></script> right before <script>
if '<script src="decision_engine.js"></script>' not in html:
    html = html.replace('<script>', '<script src="decision_engine.js"></script>\n<script>', 1)
    print("Added <script src=\"decision_engine.js\"></script>")

# 2. Add decisionEngine initialization right after `let lastSamples = [];`
engine_init_code = """
let decisionEngine = (typeof AgroDecisionEngine !== 'undefined') ? new AgroDecisionEngine() : null;
window.decisionEngine = decisionEngine;

function updateContext() {
  if (!decisionEngine) return;
  const dist = document.getElementById('districtSelect') ? document.getElementById('districtSelect').value : 'Kanpur Nagar';
  const seas = document.getElementById('seasonSelect') ? document.getElementById('seasonSelect').value : 'RABI';
  const wat = document.getElementById('waterSelect') ? document.getElementById('waterSelect').value : 'Tube well';
  const soil = document.getElementById('soilTypeSelect') ? document.getElementById('soilTypeSelect').value : 'Unknown';
  decisionEngine.setContext(dist, seas, soil, wat);
  renderCropDiscovery();
  renderTargetCropAnalysis();
  renderIrrigationIntelligence();
}
"""

if 'window.decisionEngine = decisionEngine;' not in html:
    html = html.replace('let lastSamples = []; // cache', 'let lastSamples = []; // cache\n' + engine_init_code, 1)
    print("Added decisionEngine initialization and updateContext.")

# 3. Update switchTab function to trigger page-specific renderers
switch_tab_orig = """function switchTab(idx, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page' + idx).classList.add('active');
  el.classList.add('active');
  closeMobileNav();
  requestAnimationFrame(() => {
    drawChart('overviewChart');
    drawChart('sensorChart');
    drawMap(lastData || {});
    if (idx === 5) updateResultsTab();
  });
}"""

switch_tab_new = """function switchTab(idx, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  const targetPage = document.getElementById('page' + idx);
  if (targetPage) targetPage.classList.add('active');
  if (el) el.classList.add('active');
  closeMobileNav();
  requestAnimationFrame(() => {
    drawChart('overviewChart');
    drawChart('sensorChart');
    if (lastData) drawMap(lastData);
    if (idx === 1) renderFieldMapZoning();
    if (idx === 3) renderCropDiscovery();
    if (idx === 4) renderTargetCropAnalysis();
    if (idx === 5) renderNutrientManagement();
    if (idx === 6) renderIrrigationIntelligence();
    if (idx === 9) renderSamplingHistory();
    if (idx === 11) renderFieldReport();
  });
}"""

if switch_tab_orig in html:
    html = html.replace(switch_tab_orig, switch_tab_new, 1)
    print("Updated switchTab to handle all 12 page renderers.")

# 4. In poll(): Ingest live telemetry into decisionEngine
poll_ingest_target = "lastData = d;"
poll_ingest_replacement = """lastData = d;
      if (window.decisionEngine) {
        decisionEngine.ingestLiveData(d);
      }"""
html = html.replace(poll_ingest_target, poll_ingest_replacement, 1)

# 5. In /samples fetch handler: Ingest samples into decisionEngine & render history
samples_ingest_target = "lastSamples = samples;"
samples_ingest_replacement = """lastSamples = samples;
        if (window.decisionEngine) {
          decisionEngine.ingestSamples(samples);
        }
        renderSamplingHistory();
        renderFieldMapZoning();"""
html = html.replace(samples_ingest_target, samples_ingest_replacement, 1)

# 6. Replace getAgrobotAnswer function to use decisionEngine
bot_fn_search = "function getAgrobotAnswer(question) {"
bot_fn_idx = html.find(bot_fn_search)
if bot_fn_idx != -1:
    # Find the matching closing bracket or start of addChatBubble
    add_bubble_idx = html.find("function addChatBubble(", bot_fn_idx)
    new_bot_fn = """function getAgrobotAnswer(question) {
  const lang = document.getElementById('voiceLang') ? document.getElementById('voiceLang').value : 'hi-IN';
  if (window.decisionEngine) {
    return decisionEngine.getAgrobotAnswer(question, lang);
  }
  return "Agro-Bot Decision Engine is initializing. Please wait...";
}

"""
    html = html[:bot_fn_idx] + new_bot_fn + html[add_bubble_idx:]
    print("Replaced getAgrobotAnswer with centralized decisionEngine call.")

# 7. Add complete rendering implementations for all pages
rendering_functions = """
// ============================================================================
// DECISION INTELLIGENCE DASHBOARD RENDERERS (PAGES 1, 3, 4, 5, 6, 9, 11)
// ============================================================================

// ---- Page 1: Field Map Spatial Zoning ----
function renderFieldMapZoning() {
  const container = document.getElementById('fieldZoningOverview');
  if (!container || !window.decisionEngine) return;
  const zoning = decisionEngine.classifyZones();
  
  if (!zoning.hasSufficientSamples) {
    container.innerHTML = `
      <div style="color:var(--text-muted);font-size:0.85rem;padding:12px;background:rgba(0,0,0,0.02);border-radius:8px;">
        ℹ️ ${zoning.messageEn}
      </div>`;
    return;
  }

  const v = zoning.fieldVariability;
  let html = `
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;">
      <div style="flex:1;min-width:180px;background:var(--card-bg);border:1px solid var(--border);border-radius:8px;padding:12px;">
        <div style="font-size:0.75rem;color:var(--text-muted);font-weight:700;">MOISTURE VARIABILITY (CV)</div>
        <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);margin-top:4px;">${v.moistureCV}</div>
      </div>
      <div style="flex:1;min-width:180px;background:var(--card-bg);border:1px solid var(--border);border-radius:8px;padding:12px;">
        <div style="font-size:0.75rem;color:var(--text-muted);font-weight:700;">pH VARIABILITY (CV)</div>
        <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);margin-top:4px;">${v.phCV}</div>
      </div>
      <div style="flex:2;min-width:240px;background:var(--card-bg);border:1px solid var(--border);border-radius:8px;padding:12px;">
        <div style="font-size:0.75rem;color:var(--text-muted);font-weight:700;">FIELD SPATIAL EVALUATION</div>
        <div style="font-size:0.85rem;color:var(--text-secondary);margin-top:4px;line-height:1.4;">${v.assessmentEn}</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
  `;

  zoning.nodes.forEach(n => {
    const isA = n.zoneTag === 'ZONE_A_ATTENTION';
    const isC = n.zoneTag === 'ZONE_C_EXCESS';
    const bg = isA ? 'rgba(239,68,68,0.1)' : isC ? 'rgba(59,130,246,0.1)' : 'rgba(34,197,94,0.1)';
    const color = isA ? '#dc2626' : isC ? '#2563eb' : '#16a34a';
    html += `
      <div style="padding:6px 12px;border-radius:6px;background:${bg};color:${color};font-size:0.75rem;font-weight:700;border:1px solid ${color}30;">
        Node [${n.row},${n.col}]: ${n.zoneLabel.split(':')[0]} (M:${n.moisture.toFixed(0)}%, pH:${n.ph.toFixed(1)})
      </div>`;
  });
  html += `</div>`;
  container.innerHTML = html;
}

// ---- Page 3: Mode A Crop Discovery ----
function renderCropDiscovery() {
  const grid = document.getElementById('cropDiscoveryGrid');
  if (!grid || !window.decisionEngine) return;
  const result = decisionEngine.runCropDiscovery();
  const crops = result.rankedCrops;

  let html = '';
  crops.forEach(c => {
    let badgeClass = 'badge-highly-suitable';
    if (c.suitabilityTag === 'POTENTIALLY_SUITABLE') badgeClass = 'badge-potentially-suitable';
    if (c.suitabilityTag === 'NEEDS_ATTENTION') badgeClass = 'badge-needs-attention';
    if (c.suitabilityTag === 'NOT_RECOMMENDED') badgeClass = 'badge-not-recommended';

    let limitsHtml = '';
    if (c.limitingFactors && c.limitingFactors.length > 0) {
      limitsHtml = '<div class="limiting-factor-list">';
      c.limitingFactors.forEach(l => {
        const cls = l.severity === 'CRITICAL' ? 'limit-critical' : 'limit-attention';
        limitsHtml += `<div class="limiting-factor-item ${cls}">
          <span>${l.severity === 'CRITICAL' ? '⚠️' : 'ℹ️'}</span>
          <div><b>${l.param}:</b> ${l.textEn}</div>
        </div>`;
      });
      limitsHtml += '</div>';
    } else {
      limitsHtml = '<div style="font-size:0.78rem;color:#16a34a;margin-top:4px;">✅ All field measurements align with optimal agronomic requirements.</div>';
    }

    const varieties = c.recommendedVarieties.map(v => v.name).slice(0, 3).join(', ');

    html += `
      <div class="crop-card">
        <div class="crop-card-header">
          <div class="crop-icon-name">
            <span class="crop-card-icon">${c.icon}</span>
            <div>
              <div class="crop-card-title">${c.cropNameEn} <span style="font-size:0.9rem;font-weight:500;color:var(--text-secondary);">(${c.cropNameHi})</span></div>
              <div class="crop-card-sub">${c.sowingWindow.descEn}</div>
            </div>
          </div>
          <span class="crop-suitability-badge ${badgeClass}">${c.tagEn}</span>
        </div>

        <div class="crop-score-bar-wrap">
          <div class="crop-score-bar-bg">
            <div class="crop-score-bar-fill" style="width:${c.suitabilityScore}%;"></div>
          </div>
          <span class="crop-score-num">${c.suitabilityScore}/100</span>
        </div>

        <div>
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">
            Agronomic Limiting Factors &amp; Alerts:
          </div>
          ${limitsHtml}
        </div>

        <div style="margin-top:auto;padding-top:10px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
          <div style="font-size:0.75rem;color:var(--text-secondary);">
            <b>Recommended UP Varieties:</b> ${varieties}
          </div>
          <button class="btn btn-secondary" style="padding:4px 10px;font-size:0.75rem;" onclick="selectTargetCrop('${c.cropId}')">
            Analyze Gap →
          </button>
        </div>
      </div>
    `;
  });

  grid.innerHTML = html;
}

function selectTargetCrop(cropId) {
  const sel = document.getElementById('targetCropDropdown');
  if (sel) sel.value = cropId;
  const tab4Btn = document.getElementById('tab4');
  switchTab(4, tab4Btn);
  renderTargetCropAnalysis();
}

// ---- Page 4: Mode B Target Crop Readiness & Gap Analysis ----
function renderTargetCropAnalysis() {
  const container = document.getElementById('targetCropAnalysisContainer');
  if (!container || !window.decisionEngine) return;
  const sel = document.getElementById('targetCropDropdown');
  const cropId = sel ? sel.value : 'wheat';
  const gap = decisionEngine.runTargetCropAnalysis(cropId);

  if (gap.error) {
    container.innerHTML = `<div style="color:#dc2626;padding:20px;">${gap.messageEn}</div>`;
    return;
  }

  // Parameter Gap Rows
  let tableRows = '';
  gap.parameterGaps.forEach(r => {
    let pillClass = 'pill-optimal';
    if (r.status.includes('DEFICIENT') || r.status.includes('ACIDIC') || r.status.includes('ALKALINE') || r.status.includes('HOT')) {
      pillClass = r.critical ? 'pill-danger' : 'pill-warning';
    } else if (r.status.includes('MARGINAL') || r.status.includes('EXCESS') || r.status.includes('COLD')) {
      pillClass = 'pill-warning';
    } else if (r.status === 'UNKNOWN') {
      pillClass = 'pill-info';
    }

    tableRows += `
      <tr>
        <td style="font-weight:700;">${r.parameter}<br><span style="font-size:0.75rem;color:var(--text-muted);font-weight:normal;">${r.parameterHi}</span></td>
        <td style="font-family:var(--font-mono);font-weight:700;">${r.fieldValue}</td>
        <td style="color:var(--text-secondary);font-size:0.8rem;">${r.requirement}</td>
        <td><span class="status-pill ${pillClass}">${r.status}</span></td>
        <td style="font-size:0.82rem;line-height:1.4;">${r.suggestedActionEn}</td>
        <td style="font-size:0.78rem;font-weight:700;color:var(--text-muted);">${r.timing}</td>
      </tr>
    `;
  });

  // Pre-sowing actions
  let preActionsHtml = '';
  if (gap.preSowingActions.length > 0) {
    gap.preSowingActions.forEach(a => {
      preActionsHtml += `
        <div class="action-card ${a.critical ? 'critical' : 'important'}">
          <div class="action-card-title">
            <span>${a.critical ? '🔴 ' : '🟠 '}${a.titleEn}</span>
            <span style="font-size:0.72rem;font-weight:800;color:${a.critical ? '#dc2626':'#f59e0b'};text-transform:uppercase;">${a.critical ? 'Mandatory Prior to Sowing' : 'Recommended'}</span>
          </div>
          <div class="action-card-desc">${a.descEn}<br><i>${a.descHi}</i></div>
        </div>
      `;
    });
  } else {
    preActionsHtml = '<div style="color:#16a34a;font-size:0.85rem;padding:12px;background:rgba(34,197,94,0.08);border-radius:8px;">✅ No critical pre-sowing chemical or soil amendments required. Standard seedbed preparation can proceed.</div>';
  }

  // Standing crop actions
  let standingActionsHtml = '';
  gap.standingCropActions.forEach(a => {
    standingActionsHtml += `
      <div class="action-card good">
        <div class="action-card-title">
          <span>💧 ${a.titleEn}</span>
          <span style="font-size:0.72rem;font-weight:700;color:#16a34a;">TIMED STAGE</span>
        </div>
        <div class="action-card-desc">${a.descEn}<br><i>${a.descHi}</i></div>
      </div>
    `;
  });

  // Mandatory Lab Tests
  let labTestsHtml = '<ul style="margin:6px 0 0;padding-left:20px;font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">';
  gap.mandatoryLabTests.forEach(t => {
    labTestsHtml += `<li><b>${t}</b></li>`;
  });
  labTestsHtml += '</ul>';

  const readinessColor = gap.readinessScore >= 80 ? '#16a34a' : gap.readinessScore >= 50 ? '#f59e0b' : '#dc2626';

  let html = `
    <!-- Readiness Banner -->
    <div class="card span-full" style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin-bottom:20px;">
      <div style="width:90px;height:90px;border-radius:50%;border:6px solid ${readinessColor};display:flex;align-items:center;justify-content:center;flex-direction:column;flex-shrink:0;">
        <span style="font-size:1.6rem;font-weight:800;font-family:var(--font-mono);color:${readinessColor};line-height:1;">${gap.readinessScore}</span>
        <span style="font-size:0.65rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">/ 100</span>
      </div>
      <div style="flex:1;min-width:260px;">
        <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;color:var(--text-muted);letter-spacing:0.5px;">Crop Readiness &amp; Soil Gap Assessment</div>
        <div style="font-size:1.3rem;font-weight:800;color:${readinessColor};margin:4px 0;">${gap.readinessLabelEn}</div>
        <div style="font-size:0.85rem;color:var(--text-secondary);">${gap.readinessLabelHi}</div>
      </div>
    </div>

    <!-- Parameter Gap Table Card -->
    <div class="card span-full" style="margin-bottom:20px;">
      <div class="card-title"><span class="icon">📊</span>Parameter-by-Parameter Readiness Gap Table</div>
      <div class="table-wrap">
        <table class="gap-table">
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Field Measurement</th>
              <th>Verified Requirement</th>
              <th>Status</th>
              <th>Suggested Agronomic Action</th>
              <th>Timing</th>
            </tr>
          </thead>
          <tbody>
            ${tableRows}
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid-2">
      <!-- Pre-Sowing Action Plan -->
      <div class="card">
        <div class="card-title"><span class="icon">🛠️</span>Pre-Sowing Soil Correction Plan (Mandatory Before Tillage)</div>
        <div style="margin-top:12px;">${preActionsHtml}</div>
      </div>

      <!-- Standing Crop Management -->
      <div class="card">
        <div class="card-title"><span class="icon">🌱</span>Standing Crop &amp; Growth Stage Management</div>
        <div style="margin-top:12px;">${standingActionsHtml}</div>
      </div>
    </div>

    <!-- Lab Testing & Traceability Card -->
    <div class="card span-full" style="margin-top:20px;">
      <div class="card-title"><span class="icon">🔬</span>Required Laboratory Soil Health Card Confirmations</div>
      <p style="font-size:0.84rem;color:var(--text-secondary);margin:0 0 10px;">
        The rover's on-board sensor provides initial field diagnostics. To avoid chemical toxicity or economic waste, the following parameters require certified wet-chemistry laboratory soil testing before bulk fertilizer prescription:
      </p>
      ${labTestsHtml}
      <div class="safeguard-banner" style="margin-top:14px;margin-bottom:0;">
        <b>Scientific Safeguard:</b> ${gap.scientificSafeguard}
      </div>
    </div>
  `;

  container.innerHTML = html;
}

// ---- Page 5: Nutrient Management ----
function renderNutrientManagement() {
  const grid = document.getElementById('nutrientPanelsGrid');
  if (!grid || !window.decisionEngine) return;
  const audit = decisionEngine.runNutrientAudit();

  grid.innerHTML = `
    <!-- Nitrogen Panel -->
    <div class="nutrient-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.85rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Nitrogen (N)</span>
        <span class="status-pill pill-info">${audit.nitrogen.status}</span>
      </div>
      <div class="nutrient-val-badge">${audit.nitrogen.rawIndex}</div>
      <div style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Unverified Sensor Index (0-1999)</div>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin:0;line-height:1.5;">${audit.nitrogen.interpretationEn}</p>
      <div style="font-size:0.8rem;color:var(--text-muted);border-top:1px solid var(--border);padding-top:8px;">
        <b>Agronomic Function:</b> Vegetative growth, chlorophyll synthesis, tillering.
      </div>
    </div>

    <!-- Phosphorus Panel -->
    <div class="nutrient-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.85rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Phosphorus (P)</span>
        <span class="status-pill pill-info">${audit.phosphorus.status}</span>
      </div>
      <div class="nutrient-val-badge">${audit.phosphorus.rawIndex}</div>
      <div style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Unverified Sensor Index (0-1999)</div>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin:0;line-height:1.5;">${audit.phosphorus.interpretationEn}</p>
      <div style="font-size:0.8rem;color:var(--text-muted);border-top:1px solid var(--border);padding-top:8px;">
        <b>Agronomic Function:</b> Root expansion, energy transfer (ATP), uniform ripening.
      </div>
    </div>

    <!-- Potassium Panel -->
    <div class="nutrient-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.85rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Potassium (K)</span>
        <span class="status-pill pill-info">${audit.potassium.status}</span>
      </div>
      <div class="nutrient-val-badge">${audit.potassium.rawIndex}</div>
      <div style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Unverified Sensor Index (0-1999)</div>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin:0;line-height:1.5;">${audit.potassium.interpretationEn}</p>
      <div style="font-size:0.8rem;color:var(--text-muted);border-top:1px solid var(--border);padding-top:8px;">
        <b>Agronomic Function:</b> Stomatal regulation, disease resilience, lodging prevention.
      </div>
    </div>
  `;
}

// ---- Page 6: Irrigation Intelligence ----
function renderIrrigationIntelligence() {
  const urgencyCard = document.getElementById('irrigationUrgencyCard');
  const stagesCard = document.getElementById('irrigationStagesCard');
  if (!urgencyCard || !window.decisionEngine) return;
  const sel = document.getElementById('targetCropDropdown');
  const cropId = sel ? sel.value : 'wheat';
  const irri = decisionEngine.runIrrigationAssessment(cropId);

  let urgencyColor = '#16a34a';
  if (irri.urgency.includes('HIGH')) urgencyColor = '#dc2626';
  else if (irri.urgency.includes('LIGHT') || irri.urgency.includes('EXCESS')) urgencyColor = '#f59e0b';

  urgencyCard.innerHTML = `
    <div class="card-title"><span class="icon">💧</span>Measured Moisture &amp; Irrigation Recommendation</div>
    <div style="display:flex;align-items:center;gap:20px;margin:16px 0;">
      <div style="font-size:3rem;font-weight:800;font-family:var(--font-mono);color:${urgencyColor};line-height:1;">
        ${irri.currentMoisture.toFixed(1)}%
      </div>
      <div>
        <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Target Sowing Range for ${irri.cropEvaluated}</div>
        <div style="font-size:1.1rem;font-weight:700;color:var(--text-primary);">${irri.targetRange[0]}% – ${irri.targetRange[1]}%</div>
      </div>
    </div>
    <div style="padding:14px;border-radius:8px;background:${urgencyColor}15;border-left:4px solid ${urgencyColor};margin-bottom:14px;">
      <div style="font-size:0.95rem;font-weight:700;color:${urgencyColor};margin-bottom:4px;">${irri.urgency.replace(/_/g, ' ')}</div>
      <div style="font-size:0.85rem;color:var(--text-primary);line-height:1.5;">${irri.recommendationEn}</div>
      <div style="font-size:0.82rem;color:var(--text-secondary);margin-top:4px;"><i>${irri.recommendationHi}</i></div>
    </div>
    <div style="font-size:0.82rem;color:var(--text-muted);">
      <b>Water Source Context:</b> ${irri.waterSourceConsiderationEn}
    </div>
  `;

  let stagesHtml = '';
  if (irri.criticalStages && irri.criticalStages.length > 0) {
    stagesHtml = '<div style="display:flex;flex-direction:column;gap:8px;margin-top:12px;">';
    irri.criticalStages.forEach(st => {
      const isCrit = st.importance === 'CRITICAL';
      stagesHtml += `
        <div style="padding:10px 14px;border-radius:6px;background:var(--card-bg);border:1px solid var(--border);border-left:3px solid ${isCrit ? '#dc2626' : '#22c55e'};display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-size:0.85rem;font-weight:700;color:var(--text-primary);">${st.stageEn} (${st.das})</div>
            <div style="font-size:0.75rem;color:var(--text-muted);">${st.stageHi}</div>
          </div>
          <span style="font-size:0.72rem;font-weight:800;padding:3px 8px;border-radius:6px;background:${isCrit ? 'rgba(239,68,68,0.1)' : 'rgba(34,197,94,0.1)'};color:${isCrit ? '#dc2626' : '#16a34a'};">
            ${st.importance}
          </span>
        </div>`;
    });
    stagesHtml += '</div>';
  } else {
    stagesHtml = '<div style="color:var(--text-muted);font-size:0.85rem;padding:12px;">Select a target crop to view critical irrigation growth stages.</div>';
  }

  stagesCard.innerHTML = `
    <div class="card-title"><span class="icon">📅</span>Critical Irrigation Growth Stages (${irri.cropEvaluated})</div>
    <p style="font-size:0.82rem;color:var(--text-muted);margin:0 0 6px;">Water stress during these stages leads to irrevocable yield loss.</p>
    ${stagesHtml}
  `;
}

// ---- Page 9: Sampling History Table & CSV Export ----
function renderSamplingHistory() {
  const tbody = document.getElementById('samplingHistoryTableBody');
  if (!tbody) return;
  const samples = lastSamples || [];

  if (samples.length === 0) {
    tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text-muted);padding:24px;">No samples recorded yet. Run an Auto Mapping mission to collect field survey points.</td></tr>';
    return;
  }

  let html = '';
  samples.forEach((s, i) => {
    const lat = s.lat ? s.lat.toFixed(5) : '0.00000';
    const lng = s.lng ? s.lng.toFixed(5) : '0.00000';
    const sampleId = s.sampleId || `SMP-${i+1}`;
    html += `
      <tr>
        <td style="font-weight:700;font-family:var(--font-mono);">${sampleId}</td>
        <td>Row ${s.row}, Col ${s.col}</td>
        <td style="font-family:var(--font-mono);font-size:0.78rem;">${lat}, ${lng}</td>
        <td style="font-weight:700;">${s.moisture.toFixed(1)}%</td>
        <td>${s.temp.toFixed(1)}°C</td>
        <td style="font-weight:700;">${s.ph.toFixed(1)}</td>
        <td>${s.n}</td>
        <td>${s.p}</td>
        <td>${s.k}</td>
        <td><span class="status-pill pill-optimal">VALID</span></td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

function exportSamplesCSV() {
  const samples = lastSamples || [];
  if (samples.length === 0) {
    alert("No sample records available to export.");
    return;
  }
  let csv = "SampleID,Row,Col,Latitude,Longitude,MoisturePct,SoilTempC,pH,NitrogenIndex,PhosphorusIndex,PotassiumIndex,AmbientTempC,AmbientHumPct\\n";
  samples.forEach((s, i) => {
    const sid = s.sampleId || `SMP-${i+1}`;
    csv += `${sid},${s.row},${s.col},${s.lat||0},${s.lng||0},${s.moisture},${s.temp},${s.ph},${s.n},${s.p},${s.k},${s.ambientTemp||0},${s.ambientHum||0}\\n`;
  });
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `agrobot_field_samples_${Date.now()}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// ---- Page 11: Field Diagnostic Report ----
function renderFieldReport() {
  const card = document.getElementById('reportPreviewCard');
  if (!card || !window.decisionEngine) return;
  const report = decisionEngine.generateReport('en');
  const avg = report.fieldSummary;

  let cropsHtml = '';
  report.discoverySummary.forEach((c, idx) => {
    cropsHtml += `
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #e2e8f0;font-size:0.85rem;">
        <span><b>${idx+1}. ${c.icon} ${c.cropNameEn} (${c.cropNameHi})</b> — ${c.tagEn}</span>
        <span style="font-weight:800;color:#16a34a;">${c.suitabilityScore}/100</span>
      </div>`;
  });

  card.innerHTML = `
    <div style="border-bottom:2px solid #22c55e;padding-bottom:14px;margin-bottom:18px;display:flex;justify-content:space-between;align-items:flex-start;">
      <div>
        <h1 style="margin:0;font-size:1.5rem;font-weight:800;color:#0f172a;">Agro-Bot Field Intelligence &amp; Crop Decision Report</h1>
        <div style="font-size:0.85rem;color:#64748b;margin-top:4px;"><b>Region:</b> ${report.region} | <b>Season:</b> ${report.season} | <b>Water Source:</b> ${report.waterSource}</div>
      </div>
      <div style="text-align:right;font-size:0.75rem;color:#64748b;">
        <div><b>Generated:</b> ${report.generatedAt}</div>
        <div><b>Engine:</b> AgroDecisionEngine v2.0-UP</div>
      </div>
    </div>

    <!-- Field Averages Overview -->
    <div style="margin-bottom:20px;">
      <h3 style="font-size:0.95rem;text-transform:uppercase;color:#475569;margin:0 0 8px;">1. Field Measurement Summary</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;">
        <div style="padding:10px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
          <div style="font-size:0.7rem;color:#64748b;font-weight:700;">AVERAGE MOISTURE</div>
          <div style="font-size:1.3rem;font-weight:800;color:#0f172a;">${avg.moisture.toFixed(1)}%</div>
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
          <div style="font-size:0.7rem;color:#64748b;font-weight:700;">AVERAGE SOIL pH</div>
          <div style="font-size:1.3rem;font-weight:800;color:#0f172a;">${avg.ph.toFixed(1)}</div>
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
          <div style="font-size:0.7rem;color:#64748b;font-weight:700;">SOIL TEMPERATURE</div>
          <div style="font-size:1.3rem;font-weight:800;color:#0f172a;">${avg.soilTemp.toFixed(1)}°C</div>
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
          <div style="font-size:0.7rem;color:#64748b;font-weight:700;">N / P / K SENSOR INDEX</div>
          <div style="font-size:1.1rem;font-weight:800;color:#0f172a;">${Math.round(avg.nitrogen)} / ${Math.round(avg.phosphorus)} / ${Math.round(avg.potassium)}</div>
        </div>
      </div>
    </div>

    <!-- Mode A Discovery Summary -->
    <div style="margin-bottom:20px;">
      <h3 style="font-size:0.95rem;text-transform:uppercase;color:#475569;margin:0 0 8px;">2. Mode A: Top Ranked Suitable Crops</h3>
      ${cropsHtml}
    </div>

    <!-- Irrigation Intelligence Summary -->
    <div style="margin-bottom:20px;">
      <h3 style="font-size:0.95rem;text-transform:uppercase;color:#475569;margin:0 0 8px;">3. Irrigation Intelligence Guidance</h3>
      <div style="padding:12px;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:6px;font-size:0.85rem;color:#166534;">
        <b>${report.irrigationAdvice.urgency}:</b> ${report.irrigationAdvice.recommendationEn}
      </div>
    </div>

    <!-- Scientific Safeguards Disclaimer -->
    <div style="padding:12px;background:#fffbeb;border:1px solid #fef3c7;border-radius:6px;font-size:0.75rem;color:#92400e;line-height:1.5;">
      <b>Scientific Safeguard Notice:</b> ${report.scientificSafeguards.npkNotice} ${report.scientificSafeguards.weatherNotice}
    </div>
  `;
}

function downloadReportHTML() {
  const card = document.getElementById('reportPreviewCard');
  if (!card) return;
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Agro-Bot Field Diagnostic Report</title>
    <style>body{font-family:system-ui,-apple-system,sans-serif;padding:30px;color:#1e293b;background:#fff;max-width:850px;margin:0 auto;}</style>
    </head>
    <body>
      ${card.innerHTML}
    </body>
    </html>
  `;
  const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `agrobot_field_report_${Date.now()}.html`;
  a.click();
  URL.revokeObjectURL(url);
}

// Lab Comparison Storage
let labComparisons = JSON.parse(localStorage.getItem('agrobot_lab_records') || '[]');

function saveLabComparison() {
  const labName = document.getElementById('labNameInput').value.trim();
  const reportId = document.getElementById('labReportIdInput').value.trim();
  const oc = parseFloat(document.getElementById('labOcInput').value) || 0;
  const labPh = parseFloat(document.getElementById('labPhInput').value) || 0;
  const labN = parseFloat(document.getElementById('labNInput').value) || 0;
  const labP = parseFloat(document.getElementById('labPInput').value) || 0;
  const labK = parseFloat(document.getElementById('labKInput').value) || 0;

  if (!labName || !reportId) {
    alert("Please provide the Laboratory Name and Report ID.");
    return;
  }

  const avg = decisionEngine ? decisionEngine.getFieldAverages() : { ph: 7.0, nitrogen: 100, phosphorus: 50, potassium: 70 };
  const record = {
    timestamp: new Date().toLocaleDateString(),
    labName,
    reportId,
    labPh,
    roverPh: avg.ph.toFixed(1),
    phVariance: (avg.ph - labPh).toFixed(1),
    labOc: oc,
    labN, labP, labK,
    roverIndices: `${Math.round(avg.nitrogen)} / ${Math.round(avg.phosphorus)} / ${Math.round(avg.potassium)}`
  };

  labComparisons.push(record);
  localStorage.setItem('agrobot_lab_records', JSON.stringify(labComparisons));
  renderLabComparisonLog();
  alert("Laboratory comparison record saved successfully!");
}

function renderLabComparisonLog() {
  const container = document.getElementById('labComparisonLog');
  if (!container) return;
  if (labComparisons.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted);font-size:0.8rem;">No laboratory validation comparisons logged yet.</div>';
    return;
  }
  let html = '<div style="margin-top:10px;font-weight:700;font-size:0.8rem;color:var(--text-muted);text-transform:uppercase;">Logged Comparison Records:</div>';
  labComparisons.forEach((c, idx) => {
    html += `
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:6px;padding:8px 12px;margin-top:6px;font-size:0.82rem;display:flex;justify-content:space-between;align-items:center;">
        <div>
          <b>${c.labName} (${c.reportId})</b>: Lab pH ${c.labPh} vs Rover pH ${c.roverPh} (Diff: ${c.phVariance}) | Lab NPK: ${c.labN}/${c.labP}/${c.labK} kg/ha vs Rover Index: ${c.roverIndices}
        </div>
        <span style="font-size:0.75rem;color:var(--text-muted);">${c.timestamp}</span>
      </div>`;
  });
  container.innerHTML = html;
}

// Initial render calls on window load
window.addEventListener('DOMContentLoaded', () => {
  renderSamplingHistory();
  renderLabComparisonLog();
});
"""

# Append rendering_functions before the closing </script> tag
script_close_idx = html.rfind('</script>')
if script_close_idx != -1:
    html = html[:script_close_idx] + '\n' + rendering_functions + '\n' + html[script_close_idx:]
    print("Injected rendering functions before </script>.")

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Part 3 completed successfully! Target file size:", os.path.getsize(target_path))
