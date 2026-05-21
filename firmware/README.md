# Nemo Sensor Node — Wiring Guide

## Hardware
- ESP32 NodeMCU WROOM-32U (38-pin version, U.FL external antenna connector)
- DS18B20 waterproof stainless steel temperature probe (~1m cable)
- 4.7kΩ resistor (pull-up for OneWire bus)
- DFRobot Gravity pH Sensor Kit SEN0161-V2
- Project box + 5V/2A USB power supply

## Wiring Diagram

```
ESP32 WROOM-32U
┌──────────────────────────────────────────────┐
│                                              │
│ 3V3 ──────────────────┬──── DS18B20 VCC      │
│                       │                      │
│                     [4.7kΩ]                  │
│                       │                      │
│ GPIO4 ─────────────────┴──── DS18B20 DATA    │
│                                              │
│ GND ─────────────────────── DS18B20 GND      │
│                                              │
│ 3V3 ─────────────────────── DFRobot pH VCC   │
│ GND ─────────────────────── DFRobot pH GND   │
│ GPIO34 (ADC1) ────────────── DFRobot pH OUT  │
│                                              │
│ VIN (5V) ────────────────── USB PSU 5V       │
│ GND ─────────────────────── USB PSU GND      │
│                                              │
│ [U.FL] ──── External 2.4GHz antenna          │
└──────────────────────────────────────────────┘
```

## Important Notes

**ADC pins:** Only use ADC1 pins (GPIO 32–39) for analog sensors.
ADC2 (GPIO 0, 2, 4, 12–15, 25–27) cannot be used when WiFi is active.
- GPIO34 → pH (ADC1, input-only)
- GPIO33 → TDS/Phase B (ADC1, input-only)
- GPIO4 → DS18B20 OneWire (digital, fine on GPIO4)

**External antenna:** WROOM-32U has a U.FL connector. Attach an external 2.4GHz antenna
for better WiFi and BLE stability near the metal aquarium cabinet, pump motors, and glass.
A cheap 3dBi U.FL antenna from AliExpress/Botland (~€2) makes a significant difference.

**Power:** Use a stable 5V/2A USB PSU. Unstable power = spurious ADC readings.
Keep power cable away from heater and pump cables to reduce EMI.

**DFRobot pH board:** The SEN0161-V2 has an onboard 3.3V regulator — safe to power
from ESP32 3V3 pin (max ~200mA from ESP32 3V3 rail, pH board draws ~10mA).

## First Boot Steps

1. Flash firmware: `esphome run firmware/nemo-sensor.yaml`
2. Check serial output for DS18B20 address (copy into nemo-sensor.yaml `address` field)
3. Dip pH probe in pH 7.0 buffer → record raw voltage from HA entity
4. Dip pH probe in pH 4.0 buffer → record raw voltage
5. Enter both values in `calibrate_linear` section of nemo-sensor.yaml
6. Reflash: `esphome run firmware/nemo-sensor.yaml`
7. Verify in HA: temperature and pH entities visible with correct values

## Phase B: Adding TDS (DFRobot Gravity SEN0244)

1. Connect TDS probe analog OUT → GPIO33
2. Uncomment the TDS sensor block in nemo-sensor.yaml
3. Reflash
4. Calibrate with a known TDS solution if needed (DFRobot provides a formula)

## pH Calibration Schedule

Recalibrate every 1–2 months, or any time readings drift more than ±0.1 from buffer value.
Keep probe in KCL 3M storage solution between uses — never in distilled water or tap water.
