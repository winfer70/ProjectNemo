# Project Nemo — Stocking Plan & Dashboard Guidance

Amazon Dream biotope — 252L, planted, soft acidic water (pH 6.0–6.8), tannins from driftwood.
Location: Kitchen tiles, Dublin, Ireland (Irish tap water — use Seachem Prime always).
Filter: Fluval 307 (through-tank connection, 16mm intake).

---

## Dashboard Access Devices

Dashboard should be accessible on all of the following devices:

| Device | Role | Notes |
|--------|------|-------|
| Samsung Tab A11+ | Main tank dashboard screen | Keep this near the aquarium for always-on monitoring. |
| Samsung Galaxy Tab S11 Ultra | Personal secondary dashboard | Full dashboard access for remote checks and control. |
| Samsung phone (model TBD) | Quick mobile checks | Use responsive mobile layout / PWA shortcut for fast status checks. |

### Dashboard UI requirement
- The same Nemo dashboard must render correctly on both tablet and phone form factors (responsive breakpoints for large tablet + mobile portrait).

---

## Tank Equipment

| Item | Detail |
|------|--------|
| Tank | Fluval Shaker 252L Premium Kit |
| Filter | Fluval 307 External Canister (24/7) |
| Air | Fluval Air Pump (24/7), 2 lines → long airstone, check valves |
| Substrate | Smooth white sand |
| Hardscape | Dragon Stone (sides) + large natural driftwood root (soaking to lose buoyancy) |
| Lighting | Fluval Shaker RGBW LED (BLE, controlled via dashboard) |

### Filter media order (bottom basket → top):
1. Basket 1 + 2 — Ceramic biomedia (beneficial bacteria colony)
2. Basket 3 — Carbon + Phosphate Remover (from Fluval Value Pack — fights Irish tap water algae)
3. Basket 4 — Quick-Clear Polishing Pad (traps fine sand/dust)

### Tapo P110 plugs assigned to:
- Filter pump (Fluval 307)
- Heater
- Light (Fluval LED)
- Air pump (~3–4W baseline; wattage drop = torn diaphragm, spike = clogged airstone)

---

## Step 0 — Biological Launch (NOW → 30 May 2026)

**Goal:** Grow beneficial bacteria in the ceramic biomedia before any fish arrive.

### Actions:
- **Ghost feeding:** Add one small pinch of generic tropical flakes **every 2 days** — rotting food produces ammonia which feeds the bacteria
- **Seachem Stability:** Add daily per bottle instructions for first 7 days, then with every new fish addition
- **Hardscape:** Place soaked driftwood in tank. Hide 2 Apistogramma caves (coconut shells or glass jars disguised with sand/moss/rocks) on opposite sides — they are territorial
- **Plants:** Add Easy-Life ProFito at half-dose once a week to help plants adapt (do NOT add EasyCarbo yet — wait until after May 30th when fish and plants are actively growing)
- **Temperature:** Set heater to 25–26°C and calibrate DS18B20 probe against a kitchen thermometer this week

### Dashboard tasks during Step 0:
- Add recurring task "Ghost Feed (pinch of flakes)" every 2 days to Screen 1
- Track Seachem Stability daily dose — level bar shows bottle remaining
- Log Ammonia + Nitrite manually every 2–3 days to watch for the cycle peak
- Pre-trip validation: before driving to Seahorse Aquariums Dublin on May 30th, check Screen 3 — if NH3 or NO2 shows red, delay the trip

### The cycle progression to watch for:
```
Week 1–2:  NH3 ↑↑ (ammonia spike from ghost feeding)
Week 2–3:  NO2 ↑↑ (nitrite spike — bacteria converting ammonia)
Week 3–4:  NO3 ↑  (nitrate appears — cycle completing)
Week 4+:   NH3 = 0, NO2 = 0, NO3 rising → TANK CYCLED ✓
```
When NH3 = 0 and NO2 = 0 for 3 consecutive tests → dashboard shows "Tank Cycled ✓" banner.

---

## Stage 1 — "Ekipa Robocza" / Working Crew
**Target date: 30 May 2026 — Seahorse Aquariums Dublin (free water test)**

Before buying: bring a jar of tank water to Seahorse for their free test. If NH3 and NO2 = 0 ppm, proceed.

| Animal | Qty | Role |
|--------|-----|------|
| Krewetka Amano (Amano Shrimp) | 6 | Algae cleanup, driftwood slime |
| Ślimak Neritina (Nerite Snail) | 2 | Glass + leaf algae, won't breed |
| Otocinclus | 6 | Glass + plant leaves |
| Kiryski Sterbai (Corydoras sterbai) | 8 | Bottom; Sterbai preferred — loves warm water (25–26°C) |

**Food to buy at Seahorse:** JBL Pronovo Tab M (Corys) + JBL Pronovo Pleco Wafer XL (Otos/future Pleco)

**Wait minimum 10–14 days before Stage 2.**

### Dashboard tasks during Stage 1:
- Set Ammonia + Nitrite log frequency to **daily** — bioload spike expected
- NH3 > 0.25 mg/L → dashboard shows "WATER CHANGE RECOMMENDED" banner
- Begin Easy-Life EasyCarbo (liquid carbon) now that fish are in — daily dose per bottle
- Begin Easy-Life ProFito at full dose (weekly)
- Start Seachem Stability again for 7 days after this addition
- **Install Fluval 307 intake pre-filter sponge or 16mm mesh guard NOW** — before Kuhli Loaches arrive in Stage 2

---

## Stage 2 — "Wielka Ławica i Duchy" / Big School & Ghosts
**Target date: ~13 June 2026** (10–14 days after Stage 1 stabilises)

| Animal | Qty | Role |
|--------|-----|------|
| Rummy Nose Tetra | 25 | Mid-water schooling — buy entire school at once |
| Piskorka / Kuhli Loach | 6 | Nocturnal bottom scavengers |
| Clown Pleco (L104) | 1 | Driftwood polisher |

**Wait minimum 10–14 days before Stage 3.**

### Dashboard tasks during Stage 2:
- **Temperature sparkline is critical** — Rummy Nose nose colour fades if temp fluctuates > 1°C
- Watch 24h sparkline for sawtooth pattern (heater undersized or failing)
- Target temp: **25–26°C** (matches Sterbai + Rummy Nose preference)
- Tapo P110 heater watts — increased variance = struggling heater
- Pre-filter sponge must be installed before Kuhlis arrive
- After filter maintenance: reminder "Did you check for Kuhlis in the canister?"
- Add Seachem Stability again for 7 days after this addition

---

## Stage 3 — "Gospodarze" / Main Residents
**Target date: ~27 June 2026** (10–14 days after Stage 2 stabilises)

| Animal | Qty | Role |
|--------|-----|------|
| Apistogramma cacatuoides (pair) | 2 (1M+1F) | Bottom territory, uses caves |
| Skalar / Angelfish | 4 (buy small, €2 coin size) | Mid to top water; small = grow up with Tetras safely |

### Dashboard tasks before Stage 3:
- **50% water change 48 hours before these fish arrive**
- Target Nitrate < 10 mg/L when Angelfish enter
- Add Seachem Stability again for 7 days after this addition
- After Stage 3 stable (2–3 weeks) → drop manual test frequency to weekly

---

## Fish Introduction Protocol (All Stages)
1. Drip-acclimatize for **45 minutes** in a container before releasing
2. Keep tank lights **off for 3–4 hours** after release to reduce transit stress
3. Add Seachem Stability daily for 7 days after each new addition

---

## Ongoing Maintenance Schedule (Post-Stage 3)

| Task | Frequency | Notes |
|------|-----------|-------|
| Partial water change (20–30%) | Weekly | ~2–3 × 25L buckets; match temp; treat with Prime first |
| Easy-Life ProFito dose | Weekly | Full dose once plants are established |
| Easy-Life EasyCarbo dose | Daily | Track bottle level in app |
| Seachem Prime dose | Each water change | Always for Irish tap water |
| Manual water test (full panel) | Weekly | Screen 3 log session |
| pH spot check | Weekly or after water changes | "Start pH Reading" button, 5-min stabilise |
| Fluval 307 intake pre-filter clean | Every 7–14 days | Watch for watt increase on filter plug |
| Fluval 307 full filter service | Every 3–4 months | Steps + part checkboxes in app |
| Filter media replacement (partial) | Every 6 months | Never replace all media at once — bacteria |

---

## "Feed Now" Automation Logic
1. "Feed Now" tapped → Nemo API calls HA to **turn off filter Tapo plug for 10 minutes**
2. HA timer auto-restarts filter after 10 min (safety — food gets eaten, not sucked in)
3. Feeding timestamp logged to database

---

## Fluval 307 Flow Monitoring via Tapo P110
- Note baseline filter watt draw after each clean
- +10–20% over baseline = pre-filter sponge needs cleaning
- Sustained wattage deviation = early warning before the motor stresses

## Air Pump Monitoring via Tapo P110
- Baseline: ~3–4W
- Wattage **drop** = torn diaphragm (replace)
- Wattage **spike** = clogged airstone (clean or replace)

---

## KCL Storage Solution (pH Probe)
Keep a 50ml bottle of **KCL storage solution** next to the tank.
pH probe lives in this bottle between spot-checks — never in distilled water or tap water.
Buy: "pH electrode storage solution" or "KCL 3M" (~€5–8 / 100ml bottle lasts ~1 year).


---

## Stage 1 — "Ekipa Robocza" / Working Crew
**Target date: 30 May 2026**

| Animal | Qty | Role |
|--------|-----|------|
| Krewetka Amano (Amano Shrimp) | 6 | Algae cleanup, driftwood slime |
| Ślimak Neritina (Nerite Snail) | 2 | Glass + leaf algae |
| Otocinclus | 6 | Glass + plant leaves |
| Kiryski Sterbai (Corydoras sterbai) | 8 | Bottom cleanup; Sterbai preferred — tolerates warmer water |

**Wait minimum 10–14 days before Stage 2.**

### Dashboard tasks during Stage 1:
- Set Ammonia + Nitrite log frequency to **daily** — bioload spike expected from 22 animals at once
- Watch for NH3 > 0.25 mg/L → dashboard shows "WATER CHANGE RECOMMENDED" banner
- Monitor TDS rise from driftwood tannins — use as trigger for first water change timing
- New tank substrate (active soil) will actively strip KH → test KH every 2–3 days
- pH may drop sharply in first 2–4 weeks as substrate acidifies — **expected for Amazon biotope**

### Hardware note:
- **Fluval 307 intake guard:** Install a 16mm pre-filter sponge or stainless mesh guard on the intake strainer BEFORE adding Kuhli Loaches in Stage 2. Kuhlis will explore the intake. Options:
  - Pre-filter sponge (most common, clean every 7–14 days)
  - Stainless steel mesh guard 16mm ID (less flow restriction)
  - Add "Clean intake pre-filter" to maintenance tasks in the app

---

## Stage 2 — "Wielka Ławica i Duchy" / Big School & Ghosts
**Target date: ~13 June 2026** (10–14 days after Stage 1 stabilises)

| Animal | Qty | Role |
|--------|-----|------|
| Rummy Nose Tetra | 25 | Mid-water schooling fish — buy entire school at once |
| Piskorka / Kuhli Loach | 6 | Nocturnal bottom scavengers |
| Clown Pleco (L104) | 1 | Driftwood polisher |

**Wait minimum 10–14 days before Stage 3.**

### Dashboard tasks during Stage 2:
- **Temperature sparkline is critical** — Rummy Nose Tetras are "canaries". Nose colour fades if temp fluctuates > 1°C. Watch the 24h sparkline for sawtooth pattern (heater undersized or failing)
- Target temp: **26–28°C** (Sterbai Corydoras and Rummy Nose both prefer warmer end)
- Monitor Tapo P110 heater watts — increased variance = struggling heater
- Check that intake pre-filter sponge is installed before introducing Kuhli Loaches
- Add Tasker/n8n reminder: after any filter maintenance, "Did you check for Kuhlis in the canister?" — they crawl in

---

## Stage 3 — "Gospodarze" / Main Residents
**Target date: ~27 June 2026** (10–14 days after Stage 2 stabilises)

| Animal | Qty | Role |
|--------|-----|------|
| Apistogramma cacatuoides (pair) | 2 (1M+1F) | Bottom territory, caves |
| Skalar / Angelfish | 4 | Mid to top water, hierarchy fish |

### Dashboard tasks during Stage 3:
- **Do a 50% water change 48 hours BEFORE these fish arrive**
- Target Nitrate < 10 mg/L when Angelfish enter — they are sensitive to "old tank syndrome"
- Apistogramma will establish territories at the bottom — normal aggression expected, not a water quality issue
- After Stage 3 is stable (2–3 weeks), you can drop manual test frequency to **weekly**

---

## Cycling Phase Monitoring (Weeks 1–6)

During the nitrogen cycle you want to see this progression in your manual test logs:

```
Week 1–2:  NH3 ↑↑ (ammonia spike — source: fish waste + substrate)
Week 2–3:  NO2 ↑↑ (nitrite spike — ammonia being converted)
Week 3–5:  NO3 ↑  (nitrate appears — cycle completing)
Week 5–6:  NH3 = 0, NO2 = 0, NO3 rising → CYCLE COMPLETE
```

**Dashboard behaviour during cycling:**
- Screen 3 (Water Tests) should show NH3 and NO2 prominently with **red badges** if > 0
- Once NH3 = 0 and NO2 = 0 for 3 consecutive tests → show "Tank Cycled ✓" banner
- After cycle complete: shift focus to NO3 trend and weekly water change schedule

---

## Ongoing Maintenance Schedule (Post-Stage 3)

| Task | Frequency | Trigger |
|------|-----------|---------|
| Partial water change (30–40%) | Weekly | 7-day timer |
| Fertiliser dose | Daily | Morning routine (Screen 1) |
| Liquid carbon dose | Daily | Morning routine (Screen 1) |
| Manual water test (full panel) | Weekly | Reminder notification |
| pH spot check | Weekly or after water changes | "Start pH Reading" button (Screen 2) |
| Fluval 307 intake pre-filter clean | Every 7–14 days | Maintenance task |
| Fluval 307 full filter service | Every 3–4 months | Maintenance task with steps |
| Filter media replacement (partial) | Every 6 months | Maintenance task with checkboxes |

---

## "Feed Now" Automation Logic

When "Feed Now" is tapped on the dashboard:
1. Nemo API calls HA to **turn off the filter Tapo plug** for 10 minutes
2. HA timer auto-restarts the filter after 10 min (safety — never forget the filter is off)
3. Feeding timestamp logged to the database
4. Screen 1 shows filter "paused for feeding" countdown

This prevents food being immediately sucked into the Fluval 307 intake before fish can eat it.

---

## Flow Rate Monitoring via Tapo P110

The Fluval 307's motor watt draw changes subtly when the intake mesh gets clogged:
- **Baseline:** Note the filter's normal watt draw when newly cleaned
- **+10–20% over baseline** = pre-filter sponge needs cleaning
- Log this baseline value in the app notes after each filter service
- Screen 2 shows real-time watts — any sustained deviation from baseline is an early warning

---

## KCL Storage Solution (pH Probe)

Keep a small 50ml bottle of **KCL (Potassium Chloride) storage solution** next to the tank.
The pH probe lives in this bottle between spot-checks. Do **not** store in distilled water or tap water — this destroys the reference junction.

Buy: "pH electrode storage solution" or "KCL 3M storage solution" (~€5–8, 100ml bottle lasts a year).
