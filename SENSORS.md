# Project Nemo — Sensor & Hardware Reference

Last updated: June 2026. Prices in EUR, sourcing for **County Meath, Ireland**.
Check Amazon.co.uk, DigiKey Ireland, Farnell Ireland, RS Components Ireland, Seahorse Aquariums (Dublin).

---

## Already Purchased ✅

| Item | Order | Arriving |
|------|-------|---------|
| SONOFF ZBDongle-E (Zigbee 3.0 USB Coordinator) | Amazon €17.77 (order 406-2957130-1783569) | Tuesday |
| SONOFF SNZB-02LD (Zigbee waterproof temp probe) | same order | Tuesday |

The SNZB-02LD covers **continuous temperature monitoring over Zigbee** immediately — no DS18B20 needed for basic temp. DS18B20 still useful if you want ESPHome-level precision (<1s refresh, calibrate_linear) alongside pH/TDS on the same ESP32 node.

---

## Summary of Totals (Ireland pricing, June 2026)

| Phase | What | Est. Cost |
|-------|------|-----------|
| Already ordered | ZBDongle-E + SNZB-02LD | €17.77 ✅ |
| A — Core electronics | ESP32 + pH sensor + ADS1115 + PSU/box + GFCI | €75–100 |
| B — Extended electronics | TDS + ORP sensors | €20–175 |
| Manual test kits | API Master Kit + KH + Fe + Chlorine | ~€73–80 |
| **Total Phase A + kits** | | **~€165–197** |
| **Total all phases + kits** | | **~€185–372** |

---

## Phase A — Core Electronics (Order Next)

### 1. ESP32 NodeMCU v3 (WROOM-32U variant)

- **Purpose:** Brain of sensor node. Reads pH + temp probes, acts as BLE proxy for Fluval light, connects to HA over WiFi.
- **Interface:** WiFi 802.11 b/g/n, BLE 4.2, I2C, OneWire, ADC1 pins
- **Est. price:** €4.50–6.50 + ~€2.50 for U.FL antenna
- **Where to buy:** DigiKey Ireland (digikey.ie), Amazon.co.uk
- **Recommended variant:** **ESP32-WROOM-32U** — U.FL connector for external antenna. Critical near metal aquarium cabinets, pump motors, and heater coils. Standard NodeMCU works but signal is weaker.
- **ADC2 warning:** GPIO 0, 2, 4, 12–15, 25–27 cannot be used for analog sensors when WiFi is active. Always use ADC1 pins (GPIO 32–39).
- **ESPHome BLE Proxy:** Add to ESPHome config to forward all BLE packets to HA over WiFi — replaces tablet Web Bluetooth entirely (see BLE Proxy section below).

### 2. DS18B20 Waterproof Temperature Probe + 4.7kΩ 1% Metal Film Resistor

> ⚠️ **CRITICAL: Do NOT buy the stainless steel version.**
> Cheap "stainless steel" probes from AliExpress/Amazon use 304 steel or chrome plating. Acidic Amazon biotope water (tannins, pH 6.0–6.8) pits this metal over weeks/months, leaching chromium and nickel into the tank. Kills invertebrates (Amano shrimp are first to die).

- **Purpose:** Optional continuous temp — supplement/replace SNZB-02LD if you want sub-second ESPHome refresh and calibrate_linear.
- **Buy instead:** **Plastic/PVC-coated DS18B20** probe. Polish search: "DS18B20 w osłonie plastikowej" or "DS18B20 PVC". On Amazon.co.uk search "DS18B20 PVC waterproof probe".
- **Fallback:** If you buy stainless, seal the metal cap completely with marine-grade adhesive heat-shrink tubing + 100% aquarium-safe silicone at the seam.
- **Resistor note:** Buy **1% tolerance metal film** 4.7kΩ resistor (not 5% carbon film). Reduces temperature jitter in ESPHome.
- **Interface:** OneWire → GPIO4
- **Accuracy:** ±0.5°C
- **Est. price:** €5–8 (probe + resistor)
- **Where to buy:** Amazon.co.uk, RS Components Ireland

### 3. DFRobot Gravity Analog pH Sensor Kit (SEN0161-V2)

- **Purpose:** Periodic pH spot-checks — **not** continuous.
- **Measures:** pH 0–14
- **Safe range (Amazon biotope):** **6.0–6.8**
- **Interface:** Analog 0–3.3V → ADS1115 (preferred) or ESP32 GPIO34 (ADC1)
- **Accuracy:** ±0.1 pH after calibration
- **Est. price:** €34–42 ex-VAT
- **Where to buy:** Farnell Ireland (farnell.com/en-IE), RS Components Ireland (ie.rs-online.com)
- **Model:** DFRobot SEN0161-V2 (V2 has onboard 3.3V regulator — no level shifter needed)

#### Why periodic, not permanent:
Biofilm and tannins coat glass electrode within 1–2 weeks in blackwater tanks. Constant immersion = probe life 6–12 months. Stored in KCl between uses = 2+ years.

#### How to use:
1. Keep probe in small bottle of **KCl storage solution** (~€5) between uses
2. Tap "Start pH Reading" in dashboard
3. Dip probe, wait **5 minutes** for stabilisation (timer shown on screen)
4. App logs reading automatically
5. Return probe to KCl bottle

#### ESPHome calibration + YAML:
Calibrate at ESPHome level via `calibrate_linear`. Use median + moving average combo filter:

```yaml
sensor:
  - platform: adc
    pin: GPIO34
    name: "pH Probe Voltage"
    attenuation: 11db   # REQUIRED — without this, input clips to 0–1.1V, reading is garbage
    filters:
      - median:
          window_size: 7
          send_every: 1
      # median kills EMI spike samples; moving_average smooths organic drift
      - sliding_window_moving_average:
          window_size: 15
          send_every: 1
      - calibrate_linear:
          - 2.03 -> 4.0   # voltage at pH 4.0 buffer (measure yours)
          - 2.47 -> 7.0   # voltage at pH 7.0 buffer (measure yours)
    unit_of_measurement: "pH"
```

> ⚠️ `attenuation: 11db` is mandatory. Default range is 0–1.1V — your DFRobot board outputs 0–3.3V. Missing this = completely wrong values and no error.

- **Notes:** Recalibrate every 1–2 months with pH 4.0 and 7.0 buffers. Replacement probes ~€20.

### 4. pH Calibration Buffer Solutions

- **Purpose:** Required for calibrating pH probe.
- **Buy:** **Pre-mixed liquid bottles** (not dry powder sachets — liquids are cleaner for spot-check dipping). pH 4.01 + pH 7.00.
- **Brands:** Hanna Instruments or Milwaukee (both available on Amazon.co.uk shipping to Ireland)
- **Irish search:** "Płyn kalibracyjny pH 4.01 / 7.00" on Amazon.co.uk or "pH calibration buffer liquid"
- **Est. price:** €8–12 for both
- **Where to buy:** Amazon.co.uk, any aquarium shop

### 5. SONOFF ZBDongle-E — ✅ ALREADY ORDERED

Arriving Tuesday. Notes:
- Connect to **REDACTED-HOST** server (10.0.0.104) via USB
- Use a **1m USB extension cable** to physically separate from USB 3.0 ports — USB 3.0 radiates 2.4GHz noise that degrades Zigbee range significantly
- Pairs with Zigbee2MQTT already configured in ProjectNemo

### 6. SONOFF SNZB-02LD — ✅ ALREADY ORDERED

Arriving Tuesday. Notes:
- IP65 waterproof probe version — probe goes in tank, unit sits outside
- Pairs via ZBDongle-E → Zigbee2MQTT → HA
- Covers continuous temperature monitoring immediately — no ESP32 or DS18B20 needed for temp alone
- Alert thresholds: < 24.5°C, > 27.5°C

### 7. ADS1115 16-Bit External ADC Module

> ⚠️ **Recommended upgrade over raw ESP32 ADC pins.**
> ESP32's internal ADC is non-linear, especially near 0V and 3.3V. Significant distortion on pH curves near extreme values. ADS1115 over I2C gives 16-bit resolution and hardware-filtered readings.

- **Purpose:** High-resolution analog reads for pH (and TDS in Phase B) instead of ESP32 internal ADC.
- **Interface:** I2C → ESP32 GPIO21 (SDA), GPIO22 (SCL)
- **Est. price:** €4.50–8.00 (basic modules); €14 DFRobot Gravity clip version
- **Where to buy:** Amazon.co.uk, RS Components Ireland
- **ESPHome config:**
  ```yaml
  i2c:
    sda: GPIO21
    scl: GPIO22

  ads1115:
    - address: 0x48

  sensor:
    - platform: ads1115
      multiplexer: 'A0_GND'
      gain: 6.144
      name: "pH Probe Voltage (ADS1115)"
  ```

### 8. Project Box + 5V/3A Power Supply + GFCI/RCD Adapter

- **Purpose:** Enclosure for ESP32 near tank. PSU runs 24/7.
- **PSU requirement:** **5V/3A minimum** — not 2A. WiFi + BLE + analog sensors + future relay modules will brownout a 2A supply under peak load.
- **Est. price:** €15–22 (box ~€5, PSU ~€8–10, GFCI ~€15)
- **Where to buy:** Local hardware shop in Navan/Ashbourne for box + GFCI. Amazon.co.uk for PSU.

> ⚠️ **SAFETY — GFCI/RCD adapter is mandatory.**
> You are placing DIY mains-powered electronics (the 5V PSU) next to water. A GFCI (Ground Fault Circuit Interrupter) / RCD plug adapter trips instantly on current leakage to water. ~€15 from any Irish hardware shop (Woodies, Atlantic Homecare, etc.). Non-negotiable.

> **Drip loop:** Route all probe cables DOWN from the project box before going UP into it. Water droplets track down cables — a drip loop prevents them reaching the PCB/connectors.

---

## Phase B — Extended Electronics (Add After Phase A Stable)

### 9. TDS / Conductivity Sensor

> ⚠️ **Ground loop warning:** Running an analog TDS sensor and analog pH sensor in the same body of water on the same power supply creates a ground loop — current leaks through the water between probes, producing wild incorrect readings. If you run both simultaneously, you must use a **DFRobot Gravity Analog Signal Isolator** on one of the analog lines, or power one sensor board via an isolated DC-DC converter (e.g. B0505S module).

**Option B1 — Budget: DFRobot Gravity TDS Sensor (SEN0244)**
- Measures Total Dissolved Solids — general water quality proxy
- Safe range: 100–400 ppm (tropical freshwater)
- Interface: Analog → ADS1115 A1 channel
- Accuracy: ±10% (trend monitoring only)
- Est. price: ~€20
- Where to buy: DFRobot store, Amazon.co.uk, AliExpress

**Option B2 — Accurate: Atlas Scientific EZO-EC Conductivity Kit**
- Lab-grade, temperature-compensated
- Interface: I2C (shares bus with ADS1115 and other Atlas modules)
- Accuracy: ±2%
- Est. price: ~€200–230
- Start with B1. Upgrade to Atlas only if trend data shows B1 insufficient.

### 10. Atlas Scientific EZO-ORP Circuit + ORP Probe

- Oxidation-Reduction Potential — catches declining water quality before nitrate spikes
- Safe range: +200 to +400 mV
- Interface: I2C
- Est. price: ~€145 (circuit ~€46 + probe ~€99)
- Atlas Scientific (atlas-scientific.com) — ships to Ireland

---

## Manual Test Kits — Log Results Into App

Cannot be measured affordably with continuous sensors. Test with kit, log into Project Nemo, app tracks trends.

Frequency: weekly during cycling/setup, biweekly once stable.

### 11. API Freshwater Master Test Kit (covers pH, High-pH, NH3, NO2, NO3)

- **Best value** — 800+ combined tests
- Est. price: €45–49
- Where to buy: **Seahorse Aquariums, Dublin** (seahorseaquariums.ie) — ships daily to Meath. Or Petworld.ie.
- Note: JBL ProAquaTest CombiSet is equivalent and often better-stocked in Ireland — check both.

> ⚠️ **Ammonia false positive with Seachem Prime:** If you use Seachem Prime (or any dechlorinator that detoxifies ammonia by binding it), API ammonia test reads positive for 24–48h even when ammonia is neutralized. The app should suppress ammonia alerts if a water change was logged within the last 24 hours.

> ⚠️ **Nitrate Bottle #2 shake:** API Nitrate test uses a zinc suspension in Bottle #2. Shake vigorously for **60 full seconds** before using. Zinc settles into a solid brick at the bottom — skipping this gives false low readings. App should show a 60-second countdown timer when logging a Nitrate test.

### 12. API KH Test Kit (Carbonate Hardness)

- Measures water's pH buffering capacity — low KH = overnight pH crash
- Safe range: 4–8 dKH
- Est. price: ~€9.99
- Where to buy: Seahorse Aquariums (seahorseaquariums.ie), Amazon.co.uk

### 13. JBL Iron (Fe) Test

- Iron: key plant micronutrient. Too low = yellow leaves. Too high = algae.
- Safe range: 0.05–0.1 mg/L
- **Test immediately after fertilizer dosing** — not before water change. Most aquarium iron tests only detect chelated iron (Fe-EDTA/Fe-DTPA). If using unchelated ferrous iron or gluconate, test will read 0 even with sufficient iron.
- Est. price: ~€12.50
- Where to buy: Seahorse Aquariums, local Irish aquarium shops (JBL is dominant brand in Ireland)

### 14. Free Chlorine Test Strips

- Verifies dechlorinator worked before adding tap water to tank
- Safe range: 0 mg/L
- Est. price: €6–9
- Where to buy: Amazon.co.uk, Irish pool/hardware shops, Seahorse Aquariums

---

## Safe Ranges Quick Reference

| Parameter | Type | Safe Range | Unit | Alert Low | Alert High |
|-----------|------|-----------|------|-----------|------------|
| Temperature | Continuous (Zigbee) | **25–26°C** (Amazon biotope) | °C | < 24.5 | > 27.5 |
| pH | Periodic spot-check | **6.0–6.8** | — | rate drop > 0.5 in 4h | > 7.0 |
| TDS | Continuous (Phase B) | 100–400 | ppm | < 100 | > 500 |
| ORP | Continuous (Phase B) | +200 to +400 | mV | < 150 | > 450 |
| KH / Alkalinity | Manual kit | 4–8 | dKH | < 3 | > 12 |
| Nitrate | Manual kit | 0–25 | mg/L | — | > 25 |
| Nitrite | Manual kit | 0 | mg/L | — | > 0.1 |
| Ammonia | Manual kit | 0 | mg/L | — | > 0.25 (suppress 24h after water change) |
| Copper | Manual kit | 0–0.02 | mg/L | — | > 0.05 |
| Iron | Manual kit | 0.05–0.1 | mg/L | < 0.05 | > 0.3 |
| Free Chlorine | Manual kit | 0 | mg/L | — | > 0 |

**pH alert note:** Static < 5.8 threshold too coarse for blackwater biotope. Alert on **rate of change** instead — pH drop > 0.5 units in 4 hours signals a pH crash before buffering is exhausted.

---

## App Logic Requirements (ProjectNemo UI)

These must be implemented in the water tests UI:

1. **Nitrate logging flow:** Show 60-second countdown timer ("Shake Bottle #2!") when user taps "Log Nitrate Test"
2. **Ammonia alert suppression:** If water change logged in last 24h, suppress ammonia alert. Show note: "Ammonia reading may be elevated 24–48h after using Seachem Prime"
3. **Iron test reminder:** Show tip "Test iron immediately after fertilizer dosing for accurate baseline"
4. **pH rate-of-change alert:** HA automation — alert if pH drops > 0.5 units within 4 hours (not just static threshold)

---

## BLE Proxy — ESP32 vs. Tablet

The tablet currently uses Web Bluetooth (Chrome) to control the Fluval light via BLE directly.

**Alternative: ESP32 as BLE Proxy for Home Assistant**

The ESP32 can act as a Bluetooth proxy — all BLE devices near the tank (Fluval light, future BLE sensors) appear as native HA entities. HA then controls them directly, no tablet BLE needed.

Add to ESPHome config:
```yaml
esp32_ble_tracker:
  scan_parameters:
    interval: 110ms
    window: 110ms
    active: true

bluetooth_proxy:
  active: true   # active=true enables bidirectional control (send commands, not just receive)
```

| AppREDACTED-HOST | Pros | Cons |
|----------|------|------|
| Tablet Web BT (current) | Instant slider control, already works | Android can kill BT background tasks; requires Chrome flag |
| ESP32 BLE proxy | HA-native, never sleeps, survives tablet reboot | Fluval protocol may not be natively supported by HA BLE stack — needs validation |

**Recommendation:** Keep tablet Web BT for now (it works). Add ESP32 BLE proxy when the ESP32 node is built — test if HA detects Fluval automatically.

---

## Connectivity Map (ESP32 pins)

```
ESP32 GPIO4  → DS18B20 data (OneWire) + 4.7kΩ 1% metal film to VCC  [optional, SNZB-02LD covers temp]
ESP32 GPIO21 → I2C SDA → ADS1115 (pH/TDS analog) + Atlas EZO probes [Phase B]
ESP32 GPIO22 → I2C SCL → ADS1115 + Atlas EZO probes                  [Phase B]
ADS1115 A0   → DFRobot pH analog output
ADS1115 A1   → DFRobot TDS analog output                              [Phase B]
ESP32 VIN    → 5V/3A from USB power supply
ESP32        → WiFi → Home Assistant (ESPHome native API)
ESP32        → BLE proxy → Fluval Shaker RGBW light (+ future BLE sensors)
```

Note: GPIO34/35/36/39 are input-only ADC pins — safe fallback if not using ADS1115.
If using ADS1115 (recommended), pH/TDS do NOT connect to ESP32 ADC pins directly.

---

## Ireland Sourcing Quick Reference

| Item | Supplier | Est. Price |
|------|----------|-----------|
| ESP32 WROOM-32U | DigiKey Ireland (digikey.ie) or Amazon.co.uk | €4.50–6.50 |
| U.FL antenna | Amazon.co.uk | ~€2.50 |
| DS18B20 PVC probe | Amazon.co.uk (search "DS18B20 PVC waterproof") | €5–8 |
| DFRobot SEN0161-V2 pH | Farnell Ireland (farnell.com/en-IE) | €34–42 |
| pH calibration liquid | Amazon.co.uk (Hanna/Milwaukee brand) | €8–12 |
| ADS1115 ADC module | Amazon.co.uk or RS Components Ireland | €4.50–8 |
| 5V/3A PSU | Amazon.co.uk | €8–10 |
| Project box | Woodies / Atlantic Homecare Meath / local electrical wholesaler | ~€5 |
| GFCI/RCD adapter | Woodies / Atlantic Homecare / any hardware shop | ~€15 |
| API Freshwater Master Kit | Seahorse Aquariums Dublin (seahorseaquariums.ie) | €45–49 |
| API KH Test Kit | Seahorse Aquariums | ~€9.99 |
| JBL Iron Test | Seahorse Aquariums / Petworld.ie | ~€12.50 |
| Free Chlorine strips | Amazon.co.uk / Seahorse Aquariums | €6–9 |
| Analog Signal Isolator | DFRobot store / Amazon.co.uk | ~€12 [Phase B, if running pH+TDS] |
