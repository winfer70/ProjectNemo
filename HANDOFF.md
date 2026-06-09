# HANDOFF — ProjectNemo / Care Schedule + Calendar Rebuild
Date: 2026-06-09

## What Was Accomplished

### Aquarium Data Full Sync (from Google AI chronicle)
Complete review of tank specs, livestock, care schedule, and stocking plan. Memory files fully rewritten.

### DB Fixes (livestock)
- Amano Shrimp qty: 6 → **5** (lost 2 to failed molts)
- Kuhli Loach: `in_tank` → **`planned`** (not actually in tank yet)
- Pearl Gourami notes: updated to reflect +1 female planned for Step A (target: 1M+2F)
- Corydoras confirmed: **False Julii** (*Corydoras trilineatus*), qty=7, in_tank

### Calendar Full Rebuild (deleted 16 old → 13 new tasks)
Previous schedule was generic/wrong. New schedule matches confirmed weekly plan:

| ID | Days | Task |
|----|------|------|
| 17 | daily | Poranna kontrola |
| 18 | Mon [0] | Karmienie — płatki + ½ JBL Pronovo |
| 19 | Tue [1] | Karmienie — płatki |
| 20 | Wed [2] | Karmienie — ½ JBL Pronovo + ¼ tabletki glonowej |
| 21 | Thu [3] | Karmienie — płatki (POST w dniu obsady) |
| 22 | Fri [4] | POST — brak karmienia |
| 23 | Sat [5] | Karmienie — płatki + ½ JBL Pronovo |
| 24 | Sun [6] | Karmienie — płatki + ¼ tabletki glonowej |
| 25 | Mon+Thu | Seachem Stability — 15ml (3 kapsle) |
| 26 | Sun [6] | Test wody — NO2 + NO3 |
| 27 | every 30d | Odkurzanie podłoża (start 2026-06-27) |
| 28 | every 90d | Serwis filtra Fluval 307 (start 2026-08-29) |
| 29 | every 180d | Przegląd półroczny (start 2026-11-28) |

**Note:** Water change is NOT a recurring task — conditional on NO3 > 25ppm (test Sunday first).

### Dosing Pump Channels Defined (Jebao Doser 3.4 — not yet purchased)
- Ch1: Seachem Prime
- Ch2: Seachem Stability
- Ch3: Liquid Carbon
- Ch4: Liquid Fertilizer
- **Frequency TBD** — currently testing daily, will define schedule once NH3/NO2 starts moving

## Current State

### Livestock (live DB as of 2026-06-09)
| Species | Latin | Qty | Status |
|---------|-------|-----|--------|
| Pearl Gourami | Trichopodus leerii | 2 | in_tank (1M+1F, +1F planned Step A) |
| Five-Banded Barb | Desmopuntius pentazona | 18 | in_tank |
| Corydoras False Julii | Corydoras trilineatus | 7 | in_tank |
| Amano Shrimp | Caridina multidentata | 5 | in_tank |
| Raccoon Tetra | Hyphessobrycon procyon | 12 | planned (Step A) |
| Panda Garra | Garra flavatra | 4 | planned (Step A) |
| Kuhli Loach | Pangio kuhlii | 6 | planned |
| Otocinclus | Otocinclus vittatus | 6 | planned (Step C) |
| Apistogramma "Double Red" | Apistogramma agassizii | 2 | planned (Step C) |

### Pending Verifications (from previous sessions)
- **BLE fix** (commit 5cdff82): hard-reload Chrome on tablet → connect Fluval → move R slider → confirm `d1 a1 03 XX` where XX ≤ 0x64
- **Modal scroll fix** (commit aaff3b8): test on Android Brave — scroll to bottom of long modal (livestock / calendar edit)

### Zigbee (arriving Tuesday June 10)
SONOFF SNZB-02LD + ZBDongle-E → plug into REDACTED-HOST USB (1m extension) → Zigbee2MQTT pair → HA temp entity → ProjectNemo integration

## Exact Next Actions

1. **Confirm Step A day**: Thu June 12 or Sat June 14 — then tell Claude to create the Step A calendar task (12x Raccoon Tetra + 4x Panda Garra + 1x Female Pearl Gourami + 30ml Stability, no feeding)
2. **Tablet verification**: BLE fix + modal scroll — test both
3. **Tuesday June 10**: Pair Zigbee sensors
4. **Monitor NH3/NO2 daily** — once spike detected, define Stability + liquid carbon/fertilizer dosing frequency

## Blockers
- Step A calendar task: waiting for purchase day confirmation (Thu or Sat)
- Dosing frequency: waiting for water test data to show cycle response
- n8n webhooks: Telegram bot token + chat ID still needed for power alerts
