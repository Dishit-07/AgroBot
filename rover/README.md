# 🚜 Agro-Bot: Autonomous Agricultural Rover & Decision Support Platform

[![Arduino ESP32](https://img.shields.io/badge/Platform-ESP32%20DevKit%20V1-blue.svg?logo=espressif)](https://www.espressif.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Decision Engine](https://img.shields.io/badge/Agronomic%20Engine-Uttar%20Pradesh%20%26%20India-brightgreen.svg)](#-agronomic-knowledge-base)
[![Sensor: SN-3002](https://img.shields.io/badge/Soil%20Probe-SN--3002%207--in--1%20Modbus%20RS485-orange.svg)](#-hardware-specifications--pin-mapping)
[![Tests Passing](https://img.shields.io/badge/Test%20Suite-31%2F31%20Passing-success.svg)](#-automated-testing)
[![Languages](https://img.shields.io/badge/Bilingual-English%20%7C%20%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80-purple.svg)](#-bilingual-voice-agro-bot)

**Agro-Bot** is an autonomous precision-agriculture rover and location-aware, explainable agricultural decision-support platform. Moving beyond passive sensor monitoring, Agro-Bot actively navigates fields, deploys a motorized 7-in-1 industrial soil probe into the earth, collects geo-tagged spatial samples, models field heterogeneity, and translates physical measurements into actionable, transparent farming advice.

Configured primarily for **Uttar Pradesh, India** (covering all 9 UP agro-climatic zones and 75 districts), its modular architecture easily scales to any agricultural region worldwide.

---

## 📌 Table of Contents

- [Key Capabilities](#-key-capabilities)
  - [Mode A: Crop Discovery](#mode-a-crop-discovery-what-should-i-grow)
  - [Mode B: Target Crop & Soil Gap Analysis](#mode-b-target-crop--soil-gap-analysis-what-should-i-improve)
  - [Spatial Intelligence & Field Zoning](#spatial-intelligence--field-zoning)
  - [Nutrient Gap Analysis & Management](#nutrient-gap-analysis--management)
  - [Irrigation Intelligence & Barometric Forecast](#irrigation-intelligence--barometric-forecast)
  - [Bilingual Voice Agro-Bot](#bilingual-voice-agro-bot)
  - [Autonomous Serpentine Mapping](#autonomous-serpentine-mapping)
- [Hardware Architecture & Pin Mapping](#-hardware-architecture--pin-mapping)
  - [Components List](#components-list)
  - [ESP32 Pinout Map](#esp32-pinout-map)
  - [SN-3002 Modbus RS485 Register Mapping](#sn-3002-modbus-rs485-register-mapping)
- [Software & System Architecture](#-software--system-architecture)
- [Agronomic Knowledge Base](#-agronomic-knowledge-base)
- [Web Dashboard (12 Tabs)](#-web-dashboard-12-tabs)
- [REST API Reference](#-rest-api-reference)
- [Installation & Setup](#-installation--setup)
  - [1. Firmware Upload (Arduino IDE)](#1-firmware-upload-arduino-ide)
  - [2. Launching the Web Dashboard](#2-launching-the-web-dashboard)
  - [3. Connecting the Dashboard to Agro-Bot](#3-connecting-the-dashboard-to-agro-bot)
- [Automated Testing](#-automated-testing)
- [Project Directory Structure](#-project-directory-structure)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🌟 Key Capabilities

### Mode A: Crop Discovery ("What should I grow?")
When a farmer scans an uncultivated field without a predetermined crop:
1. Agro-Bot collects multi-point, geo-tagged samples across the field.
2. It compares live measurements (**Moisture, Soil Temp, pH, N, P, K**, plus ambient temperature, humidity, and barometric pressure) against verified regional crop requirements.
3. It filters candidates by the active **sowing season** (Kharif, Rabi, Zaid), **agro-climatic zone**, and **farmer irrigation access** (Tube well, Canal, Rainfed, Drip).
4. Crops are ranked into three distinct tiers:
   - 🟢 **Highly Suitable**: All soil and environmental parameters fall within optimal reference ranges.
   - 🟡 **Potentially Suitable**: Viable, but flags explicit limitations (e.g., irrigation dependency or marginal pH).
   - 🔴 **Needs Attention / Restricted**: Identified critical limiting factors (e.g., acid soil penalty, severe nutrient deficit, or season mismatch).
5. **No Blind Averaging**: Avoids recommending a crop solely based on a high composite score if any critical parameter (e.g., waterlogging sensitivity or pH threshold) is breached.

### Mode B: Target Crop & Soil Gap Analysis ("What should I improve?")
When a farmer selects a specific crop (e.g., *Wheat, Rice, Sugarcane, Mustard, Potato, Maize, Pulses*):
* **Parameter-by-Parameter Gap Matrix**:
  | Parameter | Measured Value | Reference Range | Status | Agronomic Action |
  |---|---|---|---|---|
  | **Soil pH** | 5.8 | 6.0 – 7.5 | Needs Attention | Acidic: Apply Agricultural Lime (calcium carbonate) before sowing |
  | **Nitrogen (N)** | 28 mg/kg | 40 – 70 mg/kg | Deficient | Apply split basal Urea + Vermicompost |
  | **Phosphorus (P)**| 12 mg/kg | 15 – 30 mg/kg | Moderate | Single Superphosphate (SSP) / DAP band placement |
  | **Potassium (K)** | 35 mg/kg | 30 – 50 mg/kg | Adequate | MOP top-dressing during vegetative stage |
  | **Moisture** | 18.5% | 20 – 30% | Low | Pre-sowing Palewa irrigation recommended |
  | **Soil Temp** | 22.4°C | 15 – 25°C | Optimal | Ideal for Rabi seed germination |
* **Categorized Action Plans**:
  - **Pre-sowing Corrections**: Lime or Gypsum requirement, basal fertilization, and pre-sowing irrigation.
  - **In-season Management**: Top-dressing timings (e.g., Crown Root Initiation stage in wheat), foliar sprays, and weed control.
  - **Mandatory Laboratory Test Alerts**: Explicitly alerts the farmer when parameters like Soil Organic Carbon (SOC), Electrical Conductivity (EC), or micronutrients (Zinc/Iron/Boron) require wet-chemistry laboratory validation before committing heavy fertilizer expenses.

### Spatial Intelligence & Field Zoning
Fields are rarely uniform. Treating an entire plot as a single homogenous block leads to over-fertilization in fertile zones and crop failure in stressed zones.
* **Coefficient of Variation (CV)**: Calculates spatial variability across sample coordinates for moisture, pH, and nutrients. Classifies the field as *Homogeneous* ($CV < 15\%$), *Moderate Variability*, or *High Heterogeneity* ($CV > 30\%$).
* **Zoning Engine**: Dynamically clusters points into distinct field zones:
  - **Zone A (Stress Zone)**: Stressed / Deficient — prioritizes soil conditioning and targeted irrigation.
  - **Zone B (Prime Zone)**: Optimal productivity — standard agronomic package.
  - **Zone C (Excess / Risk Zone)**: High moisture / nutrient accumulation — risk of lodging or root rot; drainage priority.
* **Variable-Rate Prescriptions**: Delivers zone-specific irrigation schedules and nutrient amendment guidance.

### Nutrient Gap Analysis & Management
* Evaluates Nitrogen ($N$), Phosphorus ($P$), and Potassium ($K$) independently instead of conflating them into a misleading single "soil health" score.
* Differentiates between fast-acting mineral fertilizers (Urea, DAP, MOP, SSP) and sustainable organic inputs (Farmyard Manure, Vermicompost, Bio-fertilizers like *Rhizobium*, *Azotobacter*, and PSB).
* Strictly informs the farmer that raw probe NPK values represent rapid screening indices and requires soil buffering/lab tests before final kilogram-per-hectare chemical calculations.

### Irrigation Intelligence & Barometric Forecast
* Dynamically combines SN-3002 volumetric soil moisture with BMP180 atmospheric pressure gradient trends to predict imminent rainfall.
* Tailors irrigation urgency:
  - **High Urgency**: Low soil moisture + high ambient temperature + falling barometric pressure absent.
  - **Postpone Irrigation**: Rain forecast detected via negative barometric gradient ($dP/dt < -1.5\text{ hPa/hr}$) — saves water and avoids nutrient leaching.
  - **Excess Water Drainage**: Detects saturation/waterlogging in crops sensitive to wet feet (e.g., Chickpea, Lentil, Mustard).

### Bilingual Voice Agro-Bot
* Integrated conversational agricultural voice assistant supporting **Native Hindi** (*हिन्दी*) and **English**.
* Built using the browser's native Web Speech API (Speech Recognition + Speech Synthesis) for zero-latency, high-fidelity offline voice interaction.
* Deeply synchronized with the active field report and decision engine:
  - *Example Hindi Query*: *"क्या इस खेत में आलू उगाना सही रहेगा?"*
  - *Voice Reply*: *"खेत का pH 6.10 आलू के लिए अनुकूल है, लेकिन मिट्टी में नमी केवल 2.3% है। बुवाई से पहले पलेवा सिंचाई आवश्यक है।"*

### Autonomous Serpentine Mapping
* Configurable autonomous grid traversal (e.g., $3 \times 3$, $4 \times 4$, or custom dimensions).
* Smooth servo easing smoothly deploys the probe arm from transport position ($180^\circ$) to ground penetration ($0^\circ$).
* Automated dwell timer ($4000\text{ ms}$) ensures sensor stabilization in the soil before Modbus registers are captured.
* Dual confirmation beeps via active buzzer notify field operators upon sample logging, after which the probe automatically retracts before moving to the next waypoint.

---

## ⚡ Hardware Architecture & Pin Mapping

### Components List
| Category | Component | Description |
|---|---|---|
| **Controller** | ESP32 DevKit V1 (30-pin) | 240 MHz Dual-Core, 520 KB SRAM, Dual UART, Wi-Fi 802.11 b/g/n |
| **Soil Probe** | SN-3002 7-in-1 Industrial Sensor | RS485 Modbus RTU: Moisture, Soil Temp, pH, N, P, K |
| **RS485 Transceiver**| MAX485 Module | TTL to RS485 converter with hardware Flow Control (DE/RE) |
| **Environmental** | DHT11 | Ambient Temperature & Relative Humidity |
| **Atmospheric** | Bosch BMP180 | Barometric Pressure & Temperature (I2C) |
| **Air Quality** | MQ-135 Sensor | Broad-spectrum gas / AQI analog detection |
| **Orientation / Safety**| MPU6050 6-DOF IMU | 3-axis Gyroscope & 3-axis Accelerometer (Pitch/Roll terrain safety) |
| **Localization** | NEO-6M GPS Module | Microstrip antenna, NMEA sentence streaming over UART |
| **Actuators** | L298N H-Bridge Driver | 4-Wheel Drive DC gear-motors |
| **Servos** | MG995 / SG90 Servos | Servo 1: Probe vertical deployment; Servo 2: Solar panel sun-tracking |
| **Solar Tracking** | Dual LDRs (Left / Right) | Autonomous single-axis solar angle optimization |
| **Auditory Alert** | 5V Active Buzzer | Acoustic status & waypoint sampling confirmation |
| **Power Supply** | 3S 18650 Li-ion (12V) + Buck Converter | Dedicated 12V motor power rail & regulated 5V/3.3V logic rails |

---

### ESP32 Pinout Map

> [!IMPORTANT]
> All permanent hardware connections follow the fixed pin assignment below. Never change these pin definitions in firmware:

```
                          ESP32 DevKit V1 (30-pin)
                             +-----------------+
                             | [USB Connector] |
        3.3V Power Out ------| 3V3         GND |------ Ground Rail
               EN / Reset ---| EN          D23 |------ GPS RX (HardwareSerial 1)
        Solar LDR Left ------| D36 (VP)    D22 |------ I2C SCL (MPU6050, BMP180)
       Solar LDR Right ------| D39 (VN)    D1  |------ TX0 (Serial Monitor Debug)
        MQ-135 Gas ADC ------| D34         D3  |------ RX0 (Serial Monitor Debug)
      Motor IN1 (Left) ------| D32         D21 |------ I2C SDA (MPU6050, BMP180)
     Motor IN2 (Left)  ------| D33         D19 |------ Servo Arm (Probe Deployment)
     Motor IN3 (Right) ------| D25         D18 |------ Servo Solar (Sun Tracking)
      DHT11 Temp/Hum   ------| D27         D5  |------ GPS TX (HardwareSerial 1)
        Digital LDR In ------| D26         D17 |------ RS485 TX (DI, HardwareSerial 2)
     Motor IN4 (Right) ------| D14         D16 |------ RS485 RX (RO, HardwareSerial 2)
         Active Buzzer ------| D13         D4  |------ RS485 Flow Control (DE + RE)
                             | 5V          GND |
                             +-----------------+
```

---

### SN-3002 Modbus RS485 Register Mapping

The SN-3002 industrial probe communicates at **4800 Baud, 8 Data Bits, 1 Stop Bit, No Parity** (Slave Address: `0x01`).

```
Request 1: Read Moisture, Temperature, EC, and pH (Function Code 0x03)
TX >> 01 03 00 00 00 04 44 09
RX << 01 03 08 [Moist_H Moist_L] [Temp_H Temp_L] [EC_H EC_L] [pH_H pH_L] [CRC_L CRC_H]

Request 2: Read Nitrogen, Phosphorus, Potassium (Function Code 0x03)
TX >> 01 03 00 04 00 03 44 0A
RX << 01 03 06 [N_H N_L] [P_H P_L] [K_H K_L] [CRC_L CRC_H]
```

* **Soil Moisture**: Register `0x0000`, scale: $\text{Value} \div 10.0$ ($0.0 - 100.0\%$)
* **Soil Temperature**: Register `0x0001`, scale: $\text{Value} \div 10.0$ (Supports two's-complement negative temperatures)
* **Soil pH**: Register `0x0003`, scale: $\text{Value} \div 10.0$ ($0.0 - 14.0\text{ pH}$)
* **Nitrogen ($N$)**: Register `0x0004`, units: $\text{mg/kg}$ ($\text{ppm}$)
* **Phosphorus ($P$)**: Register `0x0005`, units: $\text{mg/kg}$ ($\text{ppm}$)
* **Potassium ($K$)**: Register `0x0006`, units: $\text{mg/kg}$ ($\text{ppm}$)

---

## 💻 Software & System Architecture

```mermaid
graph TD
    subgraph AgroBot_Hardware["Agro-Bot Physical Rover"]
        ESP32["ESP32 Dual-Core (FreeRTOS)"]
        SN3002["SN-3002 7-in-1 Probe (UART2 / RS485)"]
        ENV["DHT11 + BMP180 + MQ-135 + LDR"]
        NAV["TinyGPSPlus (UART1) + MPU6050 (I2C)"]
        ACT["L298N 4WD + Dual Servos + Buzzer"]
        
        SN3002 -->|Modbus RTU 4800 baud| ESP32
        ENV -->|Analog / I2C / 1-Wire| ESP32
        NAV -->|NMEA / I2C 400kHz| ESP32
        ESP32 -->|PWM / GPIO| ACT
    end

    subgraph Firmware_Engine["ESP32 Embedded Web Engine"]
        REST["REST API WebServer (Port 80)"]
        WiFi_Dual["WiFi AP+STA Mode\nHotspot + 'AGRO-ROVER' (192.168.4.1)"]
        PNA["Private Network Access (PNA)\n& Wildcard CORS Controller"]
        LoopDecouple["Decoupled Timers\nSoil: 2.5s | Fast Sensors: 500ms"]
        
        ESP32 <--> LoopDecouple
        LoopDecouple <--> REST
        REST <--> PNA
        REST <--> WiFi_Dual
    end

    subgraph Browser_Dashboard["12-Tab Responsive Web Dashboard"]
        UI["Modern Web Interface (v1.html)"]
        DE["Decision Engine (decision_engine.js)"]
        Voice["Bilingual Voice AI (Hindi & English)"]
        Zoning["Spatial Zoning & Heterogeneity Engine"]
        Report["Diagnostic Report & Print Engine"]
        
        UI <--> DE
        DE <--> Zoning
        DE <--> Voice
        DE <--> Report
    end

    WiFi_Dual <===>|HTTP / JSON (Polling / Control)| UI
```

### Key Firmware Highlights:
* **Timer Decoupling**: Soil probe Modbus polling ($2.5\text{ s}$) is completely decoupled from high-speed sensors ($500\text{ ms}$). This ensures that serial Modbus read cycles never starve `server.handleClient()`.
* **Private Network Access (PNA) Compliance**: Emits `Access-Control-Allow-Private-Network: true` on both `OPTIONS` preflight and data payloads, preventing Chromium security blocks when loading dashboards from `file:///` or `localhost`.
* **Fail-Safe AP Fallback**: Bootstraps in `WIFI_AP_STA` dual mode. If mobile hotspot connection fails, it instantly broadcasts an access point `AGRO-ROVER` at `192.168.4.1`, guaranteeing zero field downtime.
* **Terrain Safety Interlock**: Emergency shutdown triggers if MPU6050 measures roll or pitch exceeding $35^\circ$, protecting the rover chassis and motorized probe arm from rollover damage.

---

## 🌾 Agronomic Knowledge Base

The built-in agronomic database in [`decision_engine.js`](dashboard/decision_engine.js) holds peer-reviewed reference criteria for major crops, cross-referenced with **ICAR** (Indian Council of Agricultural Research) and **UP State Agricultural University** publications:

| Crop | Botanical Name | Season | Optimal pH | Optimal Moisture | Temp Range | Sowing Window | Water Sensitivity |
|---|---|---|---|---|---|---|---|
| **Wheat** (*गेहूँ*) | *Triticum aestivum* | Rabi | 6.0 – 7.5 | 20 – 30% | 15 – 25°C | Nov 1 – Dec 15 | Sensitive to early drought & terminal heat |
| **Rice / Paddy** (*धान*) | *Oryza sativa* | Kharif | 5.5 – 7.0 | 70 – 100% | 22 – 35°C | Jun 15 – Jul 25 | Semi-aquatic; tolerates prolonged saturation |
| **Sugarcane** (*गन्ना*) | *Saccharum officinarum* | Annual/Spring | 6.0 – 7.8 | 40 – 60% | 20 – 35°C | Feb – Mar / Oct | High water requirement; sensitive to drought |
| **Mustard** (*सरसों*) | *Brassica juncea* | Rabi | 6.0 – 7.5 | 18 – 28% | 12 – 25°C | Oct 1 – Oct 25 | Highly sensitive to waterlogging |
| **Potato** (*आलू*) | *Solanum tuberosum* | Rabi | 5.0 – 6.5 | 30 – 50% | 15 – 22°C | Oct 15 – Nov 15 | Acid-tolerant; sensitive to tuber rot |
| **Maize** (*मक्का*) | *Zea mays* | Kharif / Spring | 5.8 – 7.2 | 25 – 45% | 18 – 32°C | Jun 20 – Jul 15 | Sensitive to water stagnation |
| **Chickpea / Gram** (*चना*) | *Cicer arietinum* | Rabi | 6.0 – 8.0 | 15 – 25% | 15 – 25°C | Oct 15 – Nov 10 | **Extreme** waterlogging sensitivity |
| **Pigeonpea / Arhar** (*अरहर*)| *Cajanus cajan* | Kharif | 6.0 – 7.5 | 20 – 35% | 20 – 35°C | Jun 15 – Jul 15 | Deep-rooted; susceptible to wilt under flooding |
| **Lentil / Masoor** (*मसूर*) | *Lens culinaris* | Rabi | 6.0 – 7.5 | 18 – 28% | 15 – 25°C | Oct 20 – Nov 15 | Sensitive to excess moisture |
| **Pearl Millet / Bajra** (*बाजरा*)| *Pennisetum glaucum*| Kharif | 5.5 – 7.5 | 12 – 25% | 25 – 35°C | Jun 25 – Jul 20 | Drought-hardy; thrives in light sandy loam |
| **Barley / Jau** (*जौ*) | *Hordeum vulgare* | Rabi | 6.5 – 8.5 | 15 – 25% | 12 – 22°C | Oct 25 – Nov 20 | High salinity / sodicity tolerance |

### Supported Uttar Pradesh Agro-Climatic Zones
The engine natively accounts for soil profiles across all 9 UP agro-ecological regions:
1. **Tarai Zone** (High organic matter, heavy alluvial, high water table)
2. **Western Plain Zone** (Productive loam, canal/tube-well irrigated, intensive sugarcane/wheat)
3. **Mid-Western Plain Zone** (Alluvial loam to sandy loam)
4. **South-Western Semi-Arid Zone** (Low rainfall, prone to salinity/alkalinity)
5. **Central Plain Zone** (Gangetic alluvium, sodic Usar patches requiring gypsum)
6. **Bundelkhand Zone** (Black soils *Kabar/Mar* and red soils *Rakar/Parwa*, drought prone)
7. **North-Eastern Plain Zone** (Calcareous alluvium, prone to seasonal flooding)
8. **Eastern Plain Zone** (Rich alluvium, micro-nutrient zinc/boron deficiencies)
9. **Vindhyan Zone** (Red and gravelly soils, undulating terrain, rainfed pulse/oilseed)

---

## 🖥️ Web Dashboard (12 Tabs)

The unified interface in [`v1.html`](dashboard/v1.html) is responsive, works offline without CDN dependencies, and provides 12 specialized operations tabs:

1. 📊 **Overview**: Live metric cards, circular gauges (Moisture, pH, Temp, AQI, Health), weather card, rover orientation HUD, and one-click field alert banners.
2. 🗺️ **Field Intelligence Map & Zoning**: Interactive GPS grid canvas displaying spatial variability, sample markers, and Zone A / B / C spatial clustering.
3. 🧪 **Soil Analysis**: Parameter-by-parameter breakdown of raw SN-3002 measurements vs calibrated agronomic indicators.
4. 🌱 **Crop Discovery**: Evaluates all regional candidates, ranks suitability scores, and explains limiting agronomic factors.
5. 🎯 **Target Crop Analysis**: Dedicated soil readiness gap analysis table with pre-sowing and in-season corrective advice.
6. 🌿 **Nutrient Management**: Independent $N$, $P$, $K$ gap analysis with balanced inorganic and organic amendment guidance.
7. 💧 **Irrigation Intelligence**: Volumetric soil moisture combined with barometric weather pressure gradient forecasting.
8. 🎮 **Rover Control**: Real-time virtual D-pad teleoperation, solar tracker manual override, probe arm deployment slider, and buzzer toggle.
9. 🔄 **Autonomous Mapping**: Grid parameters configuration ($N \times M$ rows/cols), live waypoint progress tracker, and sample data table.
10. 📜 **Sampling History**: Comprehensive tabular log of every geo-tagged sample with export capabilities.
11. 📑 **Field Report Generator**: Formal, printable extension-ready agronomic report with signature fields and lab testing warnings.
12. 💬 **Bilingual Voice Agro-Bot**: Interactive audio conversational AI in Devanagari Hindi and English.

---

## 📡 REST API Reference

The ESP32 firmware hosts an asynchronous REST server on port `80`:

| Endpoint | Method | Query Parameters | Description |
|---|---|---|---|
| `/data` | `GET` | — | Returns comprehensive real-time rover telemetry, sensor payload, and probe status |
| `/samples` | `GET` | — | Returns array of all stored geo-tagged autonomous survey sample points |
| `/control` | `GET` | `?move=fwd\|back\|left\|right\|stop` | Controls 4WD motor actuation |
| `/servo` | `GET` | `?arm=<0-180>&solar=<0-180>` | Actuates probe deployment servo or solar angle servo |
| `/solar` | `GET` | `?mode=auto\|manual` | Toggles autonomous dual-LDR solar sun-tracking mode |
| `/buzzer` | `GET` | `?state=on\|off` | Controls acoustic signaling buzzer |
| `/auto/start` | `GET` | `?length=<int>&width=<int>` | Initiates autonomous serpentine field survey grid |
| `/auto/stop` | `GET` | — | Aborts autonomous survey and stops motors immediately |
| `/api/soil` | `GET` | — | Dedicated endpoint returning purely SN-3002 RS485 Modbus soil parameters |

### Sample `/data` JSON Payload
```json
{
  "sat": 7,
  "lat": 26.846712,
  "lng": 80.946158,
  "alt": 123.4,
  "time": "11:24:05",
  "roll": 1.2,
  "pitch": -0.8,
  "yaw": 45.1,
  "temp": 28.4,
  "hum": 62.0,
  "gas": 1420,
  "press": 1012.3,
  "day": true,
  "soilMoisture": 24.5,
  "soilTemp": 22.1,
  "ph": 6.8,
  "nitrogen": 45,
  "phosphorus": 18,
  "potassium": 42,
  "sensorStatus": "VALID",
  "probeState": "RETRACTED",
  "sensorQuality": "HIGH_VALID",
  "sensorStabilized": true,
  "solarAngle": 90,
  "solarAuto": true,
  "auto": false
}
```

---

## 🚀 Installation & Setup

### 1. Firmware Upload (Arduino IDE)
1. Install [Arduino IDE](https://www.arduino.cc/en/software) (version 2.0+ recommended).
2. Install the **ESP32 Board Package**:
   * Navigate to **File > Preferences > Additional Boards Manager URLs**:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   * Open **Tools > Board > Boards Manager**, search for `esp32`, and install `esp32 by Espressif Systems`.
3. Install Required Arduino Libraries:
   * `DHT sensor library` by Adafruit
   * `Adafruit Unified Sensor`
   * `Adafruit BMP085 Library`
   * `TinyGPSPlus` by Mikal Hart
   * `ESP32Servo` by Kevin Harrington
   * `MPU6050` by Electronic Cats (or I2Cdevlib)
4. Open the firmware:
   * Open [`app/app_new/app_new.ino`](app/app_new/app_new.ino) in Arduino IDE.
5. Configure Wi-Fi Credentials (optional):
   ```cpp
   const char *staSSID = "AGRO-BOT"; // Enter your mobile hotspot SSID
   const char *staPASS = "agro12345"; // Enter hotspot password
   ```
   *(Note: If hotspot connection fails, the rover will automatically broadcast its own Wi-Fi network `AGRO-ROVER`)*.
6. Connect the ESP32 via micro-USB, select board **ESP32 Dev Module**, choose the correct COM port, and click **Upload**.

---

### 2. Launching the Web Dashboard
Because the dashboard is built with zero build steps or heavy node frameworks:
* **Option A (Direct Browser)**: Double-click or open [`dashboard/v1.html`](dashboard/v1.html) in any modern web browser (Google Chrome, Microsoft Edge, Brave).
* **Option B (Local Web Server)**:
  ```bash
  cd "D:\Graphic hackathon\rover\dashboard"
  python -m http.server 8000
  ```
  Then navigate to `http://localhost:8000/v1.html`.

---

### 3. Connecting the Dashboard to Agro-Bot

1. **Find Rover IP**:
   * Open the Arduino Serial Monitor at **115200 baud**.
   * Note the Station IP (e.g. `192.168.1.105`) or connect your laptop's Wi-Fi directly to the rover's fallback network:
     * **WiFi SSID**: `AGRO-ROVER`
     * **Password**: `agro12345`
     * **Fallback IP**: `192.168.4.1`
2. **Configure in Dashboard**:
   * In the top-right header of the dashboard, click the **⚙ (Settings)** icon.
   * Enter the IP address in the **ESP32 Rover IP Address** box.
   * Click **⚡ Test Rover Connection**. You will see:
     ```
     ✓ Success! Connected to Rover.
     Moisture: 24.5% | Temp: 22.1°C | pH: 6.8 | Probe: VALID
     ```
   * Click **Save Configuration**. The status pill will turn green: `● LIVE`.

---

## 🧪 Automated Testing

Agro-Bot includes a complete 31-test automated verification suite in [`test_suite.js`](test_suite.js) that validates all core agronomic decision logic without requiring live hardware:

```bash
node test_suite.js
```

### Test Suite Output
```text
============================================================
AGRO-BOT MASTER DECISION INTELLIGENCE TEST SUITE (PHASE 8)
============================================================

--- Test Group 1: Optimal Rabi Conditions (Wheat) ---
✅ PASS: Wheat ranks #1 under optimal Rabi conditions
✅ PASS: Wheat receives high score (>=90)
✅ PASS: Wheat tagged HIGHLY_SUITABLE
✅ PASS: Target crop readiness is READY
✅ PASS: No pre-sowing chemical amendments needed
✅ PASS: Irrigation correctly identifies sufficient moisture

--- Test Group 2: Acidic & Drought Stress (pH 5.2, M 18%) ---
✅ PASS: Wheat heavily penalized under severe acidity/drought
✅ PASS: Critical limiting factors flagged for Wheat
✅ PASS: Gap analysis status is ATTENTION_MANDATORY
✅ PASS: Mandatory Lime application prescribed
✅ PASS: Mandatory Palewa irrigation prescribed
✅ PASS: Agro-Bot voice bot warns against planting wheat in acidic soil

--- Test Group 3: Alkaline / Sodic Soil (pH 8.6, Central UP) ---
✅ PASS: Gypsum application prescribed for alkaline sodic soil
✅ PASS: ESP laboratory testing mandated

--- Test Group 4: Waterlogged Soil (Moisture 92%) ---
✅ PASS: Rice is suitable under high water availability
✅ PASS: Chickpea is rejected under saturated soil
✅ PASS: Rice irrigation acknowledges 92% moisture as sufficient for paddy
✅ PASS: Chickpea irrigation correctly flags 92% moisture as EXCESS_DRAINAGE_REQUIRED

--- Test Group 5: Zero Data Boundary Safety ---
✅ PASS: Crop discovery handles zero data gracefully without crashing
✅ PASS: Confidence reduced when no survey data present
✅ PASS: Irrigation intelligence reports DATA_INSUFFICIENT on 0 moisture

--- Test Group 6: Season Mismatch Gate ---
✅ PASS: Rice flagged with season mismatch alert in Rabi

--- Test Group 7: Invalid GPS Nodes ---
✅ PASS: Zoning functions with grid coordinates even when GPS is 0
✅ PASS: GPS invalidity preserved per node

--- Test Group 8: Spatial Field Heterogeneity Classification ---
✅ PASS: High CV detected and field classified as heterogeneous
✅ PASS: Zone A (deficiency) node identified
✅ PASS: Zone B (optimal) node identified
✅ PASS: Zone C (excess) node identified

--- Test Group 9: Voice Assistant Multi-Script Integration ---
✅ PASS: Hindi irrigation query replies in native Hindi
✅ PASS: Hindi problem query flags moisture/pH
✅ PASS: English query returns coherent English advice

============================================================
TEST SUMMARY: 31 PASSED, 0 FAILED
============================================================
```

---

## 📁 Project Directory Structure

```text
D:\Graphic hackathon\rover\
├── README.md                          # Comprehensive project documentation (this file)
├── test_suite.js                      # 31-test agronomic decision intelligence automated test suite
├── app\
│   └── app_new\
│       ├── app_new.ino                # Primary ESP32 firmware (REST server, state machine, sensor loop)
│       ├── SoilSensor.h               # SN-3002 high-level driver header
│       ├── SoilSensor.cpp             # 7-in-1 register decoding, calibration scaling & error handling
│       ├── ModbusRS485.h              # Low-level RS485 communication header
│       └── ModbusRS485.cpp            # HardwareSerial2 transceiver, CRC16 calculation & framing
└── dashboard\
    ├── v1.html                        # 12-tab agricultural operations dashboard & bilingual voice AI
    └── decision_engine.js             # Explainable agronomic decision engine & UP regional database
```

---

## 🔮 Roadmap & Future Enhancements

- [ ] **Centimeter-Accurate RTK-GPS**: Integration of u-blox ZED-F9P RTK GNSS for centimeter-level field boundary surveying.
- [ ] **Onboard Edge AI Vision**: ESP32-CAM or Raspberry Pi sidecar running lightweight MobileNet models for real-time foliar pest & disease identification.
- [ ] **LoRaWAN Telemetry**: Long-range 868/915 MHz sub-GHz telemetry for communication across kilometer-scale rural farmlands beyond Wi-Fi range.
- [ ] **Automated Liquid Fertilizer Micro-Doser**: Peristaltic pump mechanism for closed-loop localized micronutrient soil spot-amendment during rover transit.

---

## 📄 License & Acknowledgments

This project is open-source under the [MIT License](LICENSE).

Developed for agricultural innovation, student hackathons, and farmers across Uttar Pradesh and India. Built upon agronomic guidelines published by the **Indian Council of Agricultural Research (ICAR)**, **Chandra Shekhar Azad University of Agriculture and Technology (Kanpur)**, and **Narendra Deva University of Agriculture and Technology (Ayodhya)**.
