# Project Nemo — Sensor & Hardware Reference

Use this file to validate prices and availability before purchasing.
Prices are estimates (May 2026) — check Amazon.pl, Botland.com.pl, AliExpress, and local aquarium shops.

---

## Summary of Totals

| Phase | What | Est. Cost |
|-------|------|-----------|
| A — Core electronics | ESP32 + temp + pH + Zigbee dongle | €85–110 |
| B — Extended electronics | TDS + ORP sensors | €20–175 |
| Manual test kits | 7 kits (one-time purchase) | ~€57 |
| **Total Phase A + kits** | | **~€142–167** |
| **Total all phases + kits** | | **~€162–342** |

---

## Phase A — Core Electronics (Order First)

### 1. ESP32 NodeMCU v3 (WROOM-32U recommended)
- **Purpose:** Brain of the sensor node. Reads all probes, acts as BLE proxy for the Fluval light, connects to Home Assistant over WiFi.
- **Interface:** WiFi 802.11 b/g/n, I2C, OneWire, ADC pins
- **Est. price:** €8–10
- **Where to buy:** Botland, AliExpress, Amazon
- **Recommended variant:** **ESP32-WROOM-32U** — has a U.FL connector for an external antenna. The external antenna dramatically improves WiFi + BLE stability near a metal aquarium cabinet, pump motors, and ballasts. Add a cheap U.FL antenna (~€2). Standard NodeMCU is fine as a fallback but may have weaker signal.
- **Notes:** Get the 38-pin version. Runs ESPHome firmware — no custom code needed. ADC2 pins (GPIO 0, 2, 4, 12–15, 25–27) **cannot be used for analog sensors when WiFi is active** — always use ADC1 pins (GPIO 32–39).

### 2. DS18B20 Waterproof Temperature Probe + 4.7kΩ Resistor
- **Purpose:** Continuous water temperature measurement.
- **Measures:** Temperature in °C
- **Safe range (freshwater):** 22–28°C (tropical community fish)
- **Interface:** OneWire (single data pin, GPIO4)
- **Accuracy:** ±0.5°C
- **Est. price:** €5–7 (probe + resistor together)
- **Where to buy:** Botland, AliExpress, Amazon
- **Notes:** Get the stainless steel waterproof version with ~1m cable. The 4.7kΩ resistor goes between data and VCC (pull-up). ESPHome `dallas` component handles it natively.

### 3. DFRobot Gravity Analog pH Sensor Kit (SEN0161-V2)
- **Purpose:** Periodic pH spot-checks — **not** a 24/7 continuous sensor for this setup.
- **Measures:** pH 0–14
- **Safe range (Amazon biotope):** **6.0–6.8** (soft, acidic blackwater; tannins from driftwood will pull pH down naturally)
- **Interface:** Analog (0–3.3V), connect to ESP32 GPIO34 (ADC1)
- **Accuracy:** ±0.1 pH after calibration
- **Est. price:** €50–70 (includes BNC probe)
- **Where to buy:** DFRobot official store, Amazon, Botland
- **Model number to search:** DFRobot SEN0161-V2 (get the V2 — has onboard 3.3V regulator, works cleanly with ESP32 without level shifters)

#### Why periodic, not permanent:
In a blackwater Amazon tank, biofilm and tannins coat the glass electrode within 1–2 weeks, causing drift. Constant immersion also shortens probe life to 6–12 months vs. 2+ years if stored in KCL solution between uses.

#### How to use:
1. Keep probe stored in a small bottle of **KCL storage solution** (buy separately, ~€5) between uses
2. On the dashboard: tap **"Start pH Reading"** button on Screen 2
3. Dip probe into tank, wait **5 minutes** for stabilisation (timer shown on screen)
4. App automatically logs the reading once stable
5. Return probe to storage bottle

#### ESPHome calibration:
Do calibration at the **ESPHome level** (not in the API) using `calibrate_linear` filter — so Home Assistant always receives the corrected pH value even if the Nemo API is down. Add a `sliding_window_moving_average` filter (window size 10) to smooth out EMI noise from heater/pump.

- **Notes:** Re-calibrate every 1–2 months with pH 4.0 and 7.0 buffers. Replacement probes ~€20.

### 4. pH Calibration Buffer Solutions
- **Purpose:** Required for calibrating the pH probe. Without these the readings will drift.
- **What to buy:** pH 4.0 buffer + pH 7.0 buffer (sachets or bottles)
- **Est. price:** €5–10 for a pack of both
- **Where to buy:** Any aquarium shop, Amazon
- **Notes:** Buy the pre-mixed sachet type (e.g. Hanna Instruments or generic). Keep sealed until use.

### 5. SONOFF ZBDongle-E (Zigbee 3.0 USB Coordinator)
- **Purpose:** Adds Zigbee support to the REDACTED-HOST server. Required for any future Zigbee devices (smart sensors, bulbs, plugs). Also future-proofs the setup.
- **Chip:** EFR32MG21 (EmberZNet firmware)
- **Interface:** USB-A → USB port on REDACTED-HOST server
- **Est. price:** €15–20
- **Where to buy:** Amazon, SONOFF official store
- **Important:** Use a 1m USB extension cable to move it away from the server — USB 3.0 ports cause interference with 2.4GHz Zigbee. This is officially recommended.
- **Model:** SONOFF Zigbee 3.0 USB Dongle Plus-E (the "E" variant, not "P")

### 6. Project Box + 5V Micro-USB Power Supply
- **Purpose:** Weatherproof enclosure for the ESP32 near the tank. The ESP32 runs 24/7.
- **Est. price:** €8–12 (box ~€5, PSU ~€5)
- **Where to buy:** Botland, local electronics shop, Amazon
- **Notes:** Make sure the PSU is 5V/2A minimum. Cable feed holes needed for probes.

---

## Phase B — Extended Electronics (Optional, Add Later)

### 7. TDS / Conductivity Sensor

**Option B1 — Budget: DFRobot Gravity TDS Sensor (SEN0244)**
- **Purpose:** Measures Total Dissolved Solids — a general water quality proxy. High TDS = more dissolved waste/minerals.
- **Safe range (freshwater):** 100–400 ppm (soft/medium water for tropical fish); planted tanks 200–400 ppm
- **Interface:** Analog (GPIO33 or similar)
- **Accuracy:** ±10% (sufficient for trend monitoring)
- **Est. price:** ~€20
- **Where to buy:** DFRobot store, Amazon, AliExpress
- **Notes:** Good "is something wrong?" indicator. Not a substitute for individual parameter testing.

**Option B2 — Accurate: Atlas Scientific EZO-EC Conductivity Kit**
- **Purpose:** Lab-grade conductivity with temperature compensation. More reliable long-term.
- **Interface:** I2C (shares bus with other Atlas EZO circuits)
- **Accuracy:** ±2%
- **Est. price:** ~€200–230 (full kit with probe)
- **Where to buy:** Atlas Scientific official store (atlas-scientific.com)
- **Recommendation:** Start with DFRobot. Upgrade to Atlas if you want high accuracy.

### 8. Atlas Scientific EZO-ORP Circuit + ORP Probe
- **Purpose:** Measures Oxidation-Reduction Potential — indicates how well the water can break down waste. Low ORP = water quality declining, denitrification issues.
- **Safe range (freshwater):** +200 to +400 mV (healthy aerobic system)
- **Interface:** I2C (shares bus with other Atlas EZO circuits — easy to add)
- **Accuracy:** ±1 mV
- **Est. price:** ~€145 (circuit ~€46 + ORP probe ~€99)
- **Where to buy:** Atlas Scientific (atlas-scientific.com)
- **Notes:** ORP is a "canary in the coal mine" — it catches problems before parameters like nitrate visibly spike. Very useful for planted tanks.

---

## Manual Test Kits — Log Results Into the App

These parameters **cannot be measured with affordable continuous electronic sensors** at home scale. You test with a kit, read the result, and log it into Project Nemo. The app tracks trends and alerts you if values are out of range.

Test frequency recommendation: weekly during initial setup, biweekly once stable.

### 9. KH / Total Alkalinity / Carbonate Hardness
- **What it is:** KH (Karbonathärte) = Carbonate Hardness = Total Alkalinity in freshwater. **These are the same parameter.** Measures the water's buffering capacity — how well it resists pH swings.
- **Unit:** dKH (German degrees) or ppm. 1 dKH = 17.9 ppm.
- **Safe range (freshwater):** 4–8 dKH (general community); planted CO2 tanks: 3–6 dKH
- **Why important:** Low KH = pH crashes overnight. Critical for stability.
- **Kit:** API KH Test Kit
- **Est. price:** ~€8–10
- **Where to buy:** Any aquarium shop, Amazon, Zooplus

### 10. Nitrate (NO3)
- **What it is:** End product of the nitrogen cycle. Accumulates between water changes. Less toxic than nitrite/ammonia but causes algae and stress at high levels.
- **Unit:** mg/L (ppm)
- **Safe range (freshwater):** < 25 mg/L for most fish; < 10 mg/L for sensitive species and planted tanks
- **Kit:** API Nitrate Test Kit
- **Est. price:** ~€10–12
- **Where to buy:** Any aquarium shop, Amazon

### 11. Nitrite (NO2)
- **What it is:** Intermediate product of the nitrogen cycle. Highly toxic to fish even at low levels. Should be 0 in a cycled tank.
- **Unit:** mg/L
- **Safe range:** 0 mg/L (any reading above 0 is a warning sign)
- **Kit:** API Nitrite Test Kit
- **Est. price:** ~€8–10
- **Where to buy:** Any aquarium shop, Amazon

### 12. Ammonia (NH3/NH4+)
- **What it is:** Primary waste product from fish, decaying food, plant matter. The most toxic parameter. Should be 0 in a cycled tank.
- **Unit:** mg/L
- **Safe range:** 0 mg/L (any reading above 0 is dangerous)
- **Kit:** API Ammonia Test Kit
- **Est. price:** ~€9–12
- **Where to buy:** Any aquarium shop, Amazon
- **Note:** This is what was listed as "Proteins" — protein breakdown produces ammonia. There is no consumer electronic ammonia sensor. Manual testing is the only practical option.

### 13. Copper (Cu)
- **What it is:** Toxic to invertebrates and fish at low levels. Usually only relevant if you've used copper-based medications or have copper pipes feeding the tank.
- **Unit:** mg/L
- **Safe range:** < 0.02 mg/L (below detection for most kits means safe)
- **Kit:** API Copper Test Kit
- **Est. price:** ~€7–9
- **Where to buy:** Any aquarium shop, Amazon
- **Test frequency:** Only after water changes if tap water may contain copper, or after using treatments.

### 14. Iron (Fe)
- **What it is:** Important for planted tanks — iron is a key micronutrient for plant growth. You dose it with fertilizer. Too low = yellow leaves. Too high = algae.
- **Unit:** mg/L
- **Safe range (planted):** 0.05–0.1 mg/L
- **Kit:** Sera Iron Test or JBL Iron Test
- **Est. price:** ~€10–12
- **Where to buy:** Aquarium shops, Amazon, Zooplus

### 15. Free Chlorine
- **What it is:** Chlorine added by water utilities to tap water. Toxic to fish and destroys beneficial bacteria. You dechlorinate before water changes — this test confirms the dechlorinator worked, or tests a new water source.
- **Unit:** mg/L
- **Safe range:** 0 mg/L (must be 0 before adding to tank)
- **Kit:** Hach Free Chlorine test strips, or JBL Cl Test
- **Est. price:** ~€5–8 for a pack of strips
- **Where to buy:** Amazon, hardware shops (pool section), aquarium shops
- **Test frequency:** Only when doing water changes or if dechlorinator reliability is in question.

---

## Safe Ranges Quick Reference Card

| Parameter | Type | Safe Range | Unit | Alert Low | Alert High |
|-----------|------|-----------|------|-----------|------------|
| Temperature | Continuous | **25–26°C** (Amazon biotope target) | °C | < 24.5 | > 27.5 |
| pH | **Periodic spot-check** | **6.0–6.8** (Amazon biotope) | — | < 5.8 | > 7.0 |
| TDS | Continuous (Phase B) | 100–400 | ppm | < 100 | > 500 |
| ORP | Continuous (Phase B) | +200 to +400 | mV | < 150 | > 450 |
| KH / Alkalinity | Manual kit | 4–8 | dKH | < 3 | > 12 |
| Nitrate | Manual kit | 0–25 | mg/L | — | > 25 |
| Nitrite | Manual kit | 0 | mg/L | — | > 0.1 |
| Ammonia | Manual kit | 0 | mg/L | — | > 0.25 |
| Copper | Manual kit | 0–0.02 | mg/L | — | > 0.05 |
| Iron | Manual kit | 0.05–0.1 | mg/L | < 0.05 | > 0.3 |
| Free Chlorine | Manual kit | 0 | mg/L | — | > 0 |

---

## What to Search For / Search Terms (for price checking)

| Item | Polish search term | English search term |
|------|-------------------|-------------------|
| ESP32 NodeMCU | "ESP32 NodeMCU v3" | "ESP32 NodeMCU 38 pin" |
| DS18B20 probe | "DS18B20 wodoodporny" | "DS18B20 waterproof probe" |
| DFRobot pH | "czujnik pH akwarium analogowy" | "DFRobot pH sensor SEN0161" |
| pH buffers | "roztwór buforowy pH 4.0 7.0" | "pH calibration buffer solution" |
| SONOFF Zigbee | "SONOFF Zigbee USB Dongle E" | "SONOFF ZBDongle-E" |
| API KH test | "test KH twardość węglanowa" | "API KH carbonate hardness test" |
| API Nitrate | "test azotanów NO3 akwarium" | "API nitrate test kit" |
| API Nitrite | "test azotynów NO2 akwarium" | "API nitrite test kit" |
| API Ammonia | "test amoniaku NH3 akwarium" | "API ammonia test kit" |
| API Copper | "test miedzi Cu akwarium" | "API copper test kit" |
| Sera Iron | "test żelaza Fe akwarium" | "Sera iron test / JBL iron test" |
| Chlorine strips | "test chloru woda" | "free chlorine test strips" |

---

## Connectivity Map (ESP32 pins)

```
ESP32 GPIO4  → DS18B20 data (OneWire) + 4.7kΩ to VCC
ESP32 GPIO34 → DFRobot pH analog output  (ADC1, 12-bit)
ESP32 GPIO33 → DFRobot TDS analog output (ADC1, 12-bit)  [Phase B]
ESP32 GPIO21 → I2C SDA → Atlas EZO-ORP / EZO-EC          [Phase B]
ESP32 GPIO22 → I2C SCL → Atlas EZO-ORP / EZO-EC          [Phase B]
ESP32 VIN    → 5V from USB power supply
ESP32        → WiFi → Home Assistant (ESPHome native API)
ESP32        → BLE proxy → Fluval Shaker RGBW light
```

Note: GPIO34/35/36/39 are input-only ADC pins on the ESP32 — perfect for analog sensors.
