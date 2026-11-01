# -*- coding: utf-8 -*-
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('D:/Graphic hackathon/rover/dashboard/v1.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- VERIFYING TABS AND PAGES ---")
for i in range(12):
    t = f'id="tab{i}"'
    p = f'id="page{i}"'
    print(f"Tab {i} present: {t in text} | Page {i} present: {p in text}")

print("\n--- VERIFYING DECISION ENGINE HOOKS ---")
print("decision_engine.js script tag:", '<script src="decision_engine.js"></script>' in text)
print("decisionEngine initialized:", 'window.decisionEngine = decisionEngine;' in text)
print("poll data ingest:", 'decisionEngine.ingestLiveData(d)' in text)
print("samples ingest:", 'decisionEngine.ingestSamples(samples)' in text)
print("getAgrobotAnswer connected:", 'decisionEngine.getAgrobotAnswer(question, lang)' in text)
print("renderCropDiscovery defined:", 'function renderCropDiscovery()' in text)
print("renderTargetCropAnalysis defined:", 'function renderTargetCropAnalysis()' in text)
print("renderNutrientManagement defined:", 'function renderNutrientManagement()' in text)
print("renderIrrigationIntelligence defined:", 'function renderIrrigationIntelligence()' in text)
print("renderFieldMapZoning defined:", 'function renderFieldMapZoning()' in text)
print("renderSamplingHistory defined:", 'function renderSamplingHistory()' in text)
print("renderFieldReport defined:", 'function renderFieldReport()' in text)
print("exportSamplesCSV defined:", 'function exportSamplesCSV()' in text)
print("saveLabComparison defined:", 'function saveLabComparison()' in text)

# Extract JavaScript to verify syntax with Node
script_start = text.rfind('<script>') + 8
script_end = text.rfind('</script>')
js_content = text[script_start:script_end]

with open('D:/Graphic hackathon/rover/dashboard/temp_test.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("\nExtracted JS to temp_test.js, size:", len(js_content), "bytes")
