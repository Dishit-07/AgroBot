# -*- coding: utf-8 -*-
"""
Builds the upgraded 12-page Agro-Bot Dashboard
Location: D:\Graphic hackathon\rover\dashboard\v1.html
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

backup_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'v1_backup.html')
target_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'v1.html')

with open(backup_path, 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. New CSS for Decision Intelligence & 12 Pages
decision_css = """
/* ============================================================
   DECISION INTELLIGENCE & 12-PAGE EXTENSIONS
   ============================================================ */

/* Context Bar */
.context-bar {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}
.context-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 150px;
  flex: 1;
}
.context-item label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.5px;
}
.context-select {
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--card-bg);
  color: var(--text-primary);
  font-size: 0.88rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}
.context-select:focus {
  border-color: var(--accent);
}

/* Crop Discovery Grid (Mode A) */
.crop-discovery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 18px;
  margin-top: 14px;
}
.crop-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}
.crop-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.crop-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.crop-icon-name {
  display: flex;
  align-items: center;
  gap: 12px;
}
.crop-card-icon {
  font-size: 2.2rem;
  line-height: 1;
}
.crop-card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}
.crop-card-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-style: italic;
}
.crop-suitability-badge {
  font-size: 0.75rem;
  font-weight: 800;
  padding: 5px 12px;
  border-radius: 8px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.badge-highly-suitable { background: rgba(34,197,94,0.15); color: #16a34a; border: 1px solid rgba(34,197,94,0.3); }
.badge-potentially-suitable { background: rgba(59,130,246,0.15); color: #2563eb; border: 1px solid rgba(59,130,246,0.3); }
.badge-needs-attention { background: rgba(245,158,11,0.15); color: #d97706; border: 1px solid rgba(245,158,11,0.3); }
.badge-not-recommended { background: rgba(239,68,68,0.15); color: #dc2626; border: 1px solid rgba(239,68,68,0.3); }

.crop-score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.crop-score-bar-bg {
  flex: 1;
  height: 8px;
  background: rgba(0,0,0,0.06);
  border-radius: 4px;
  overflow: hidden;
}
.crop-score-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, #eab308, #22c55e);
}
.crop-score-num {
  font-size: 0.92rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: var(--text-primary);
}

.limiting-factor-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 4px;
}
.limiting-factor-item {
  font-size: 0.8rem;
  padding: 6px 10px;
  border-radius: 6px;
  display: flex;
  gap: 6px;
  align-items: flex-start;
  line-height: 1.4;
}
.limit-critical {
  background: rgba(239,68,68,0.1);
  color: #b91c1c;
  border-left: 3px solid #dc2626;
}
.limit-attention {
  background: rgba(245,158,11,0.1);
  color: #b45309;
  border-left: 3px solid #f59e0b;
}

/* Mode B Gap Table */
.gap-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin-top: 12px;
}
.gap-table th, .gap-table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}
.gap-table th {
  background: rgba(0,0,0,0.03);
  color: var(--text-muted);
  font-weight: 700;
  font-size: 0.78rem;
  text-transform: uppercase;
}
.status-pill {
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  display: inline-block;
  white-space: nowrap;
}
.pill-optimal { background: rgba(34,197,94,0.15); color: #16a34a; }
.pill-warning { background: rgba(245,158,11,0.15); color: #d97706; }
.pill-danger { background: rgba(239,68,68,0.15); color: #dc2626; }
.pill-info { background: rgba(59,130,246,0.15); color: #2563eb; }

/* Action Cards */
.action-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin-bottom: 10px;
  box-shadow: var(--shadow-sm);
}
.action-card.critical { border-left: 4px solid #dc2626; }
.action-card.important { border-left: 4px solid #f59e0b; }
.action-card.good { border-left: 4px solid #16a34a; }
.action-card-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.action-card-desc {
  font-size: 0.84rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Nutrient Panels */
.nutrient-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  margin-top: 14px;
}
.nutrient-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.nutrient-val-badge {
  font-size: 2.2rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: var(--text-primary);
}
.safeguard-banner {
  background: rgba(245,158,11,0.12);
  border: 1px solid rgba(245,158,11,0.3);
  border-left: 4px solid #f59e0b;
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  font-size: 0.85rem;
  color: #92400e;
  line-height: 1.5;
  margin-bottom: 16px;
}

/* Print/Report formatting */
@media print {
  .sidebar, .mobile-header, .tab-bar, .context-bar, button { display: none !important; }
  .main-content { margin-left: 0 !important; padding: 0 !important; }
  .page { display: block !important; }
}
"""

# Insert new CSS before </style>
orig = orig.replace('</style>', decision_css + '\n</style>', 1)

# 2. Update Sidebar Navigation Tabs (12 tabs)
new_tabs = """    <div class="tab-bar" id="tabBar">
      <button class="tab active" onclick="switchTab(0,this)" id="tab0">
        <span class="tab-icon">📊</span>
        <span class="tab-label-text">Overview</span>
      </button>
      <button class="tab" onclick="switchTab(1,this)" id="tab1">
        <span class="tab-icon">🗺️</span>
        <span class="tab-label-text">Field Intelligence Map</span>
      </button>
      <button class="tab" onclick="switchTab(2,this)" id="tab2">
        <span class="tab-icon">🧪</span>
        <span class="tab-label-text">Soil Analysis</span>
      </button>
      <button class="tab" onclick="switchTab(3,this)" id="tab3">
        <span class="tab-icon">🌱</span>
        <span class="tab-label-text">Crop Discovery</span>
      </button>
      <button class="tab" onclick="switchTab(4,this)" id="tab4">
        <span class="tab-icon">🎯</span>
        <span class="tab-label-text">Target Crop Analysis</span>
      </button>
      <button class="tab" onclick="switchTab(5,this)" id="tab5">
        <span class="tab-icon">🌿</span>
        <span class="tab-label-text">Nutrient Management</span>
      </button>
      <button class="tab" onclick="switchTab(6,this)" id="tab6">
        <span class="tab-icon">💧</span>
        <span class="tab-label-text">Irrigation Intelligence</span>
      </button>
      <button class="tab" onclick="switchTab(7,this)" id="tab7">
        <span class="tab-icon">🎮</span>
        <span class="tab-label-text">Rover Control</span>
      </button>
      <button class="tab" onclick="switchTab(8,this)" id="tab8">
        <span class="tab-icon">🔄</span>
        <span class="tab-label-text">Auto Mapping</span>
      </button>
      <button class="tab" onclick="switchTab(9,this)" id="tab9">
        <span class="tab-icon">📋</span>
        <span class="tab-label-text">Sampling History</span>
      </button>
      <button class="tab" onclick="switchTab(10,this)" id="tab10">
        <span class="tab-icon">🎙️</span>
        <span class="tab-label-text">Ask Agro-Bot</span>
      </button>
      <button class="tab" onclick="switchTab(11,this)" id="tab11">
        <span class="tab-icon">📑</span>
        <span class="tab-label-text">Field Reports</span>
      </button>
    </div>"""

# Replace existing tab-bar in orig
tb_start = orig.find('<div class="tab-bar"')
tb_end = orig.find('</div>', orig.find('id="tab6"')) + 6
orig = orig[:tb_start] + new_tabs + orig[tb_end:]

print("Updated sidebar tab bar with all 12 navigation buttons!")

# Write preliminary update
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(orig)
print("Updated CSS and Tabs in v1.html!")
