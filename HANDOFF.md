# ProjectNemo HANDOFF — 11 June 2026

## What was accomplished this session
- Updated `api/seed_data.py` with current aquarium state from conversation summary:
  - DEFAULT_FISH: replaced with actual fish in tank (1 Pearl Gourami, 14 Penta Barbs, 7 False Julii Corydoras, 6 Kuhli Loach, 5 Amano Shrimp) + upcoming Etap A/B/C fish
  - DEFAULT_FEEDING_TIMES: ["08:00","18:00"] → ["19:00"] (single 7PM feed)
  - DEFAULT_SUPPLIES: added Aquavital Stress-Protect
  - CALENDAR_TASKS: replaced phase-based feeding tasks with day-specific schedule (Mon–Sun), updated Stability doses to Etap A (Jun 13), Etap B (Jun 25), Etap C (Jul 9), water change → every_n_days/28 starting Jun 21
- Rewrote STOCKING_PLAN.md with new Etap A/B/C timeline + water change protocol + weekly feeding table

## Current state
- seed_data.py updated — changes take effect on fresh DB (empty tables)
- If DB already has data, need to reset Docker volume to re-seed
- Etap A fish purchase is Saturday 13 June 2026 (Seahorse Aquariums or Angel Exotix)
- Water parameters confirmed: NO2=0, NO3≤10ppm, NH3=0, pH~7.4–7.6

## Exact next action
1. If website shows old data → reset DB: `docker volume rm projectnemo_nemo-db && docker compose up -d`
2. Confirm Pearl Gourami sex via video at fish shop on Sat June 13
3. Run Etap A acclimation protocol (45 min drip, lights off, 30ml Stability)
4. First water change post-Etap A: Sunday June 21 (15%, ~38L)
5. Next session: verify BLE+scroll fix on tablet, then pair SNZB-02LD+ZBDongle-E (Tuesday)

## Blockers / pending decisions
- Pearl Gourami harem ratio depends on sex confirmation at shop Saturday
- Purple Pencilfish vs Cherry Barbs for Etap B — user preference (both listed in plan)
- DB reset required if app already running with stale data
