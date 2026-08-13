# ProjectNemo Handoff — 2026-06-11

## Accomplished this session
- Seeded DB with real fish stock: 5 in_tank (Pearl Gourami, Penta Barb x14, False Julii Cory x7, Kuhli Loach x6, Amano Shrimp x5) + 5 arriving (Etap A/B/C)
- Day-specific feeding schedule Mon–Sun at 19:00 (Fri = fasting, Sun = test day)
- Stress-Protect added to supplies; Stability dosing tasks for each etap
- Water change: every 28 days from Jun 21, ~15% (~38L)
- STOCKING_PLAN.md fully rewritten with timeline, acclimation protocol, compatibility table
- ScheduleView TODAY tile: split layout — temp widget left (50% width, 42px, color-coded 24.5–27.5°C), tasks right
- Deployed to the deployment host dashboard (`http://<DEPLOYMENT_HOST_WIFI_IP>:3000`). Committed + pushed to dev.

## Current state
- UI: http://<DEPLOYMENT_HOST_WIFI_IP>:3000 ✓ live with split today tile
- API: http://<DEPLOYMENT_HOST_WIFI_IP>:8000 ✓
- Git: `dev` branch, all changes merged and pushed to origin
- Temp widget shows `—` until ZBDongle-E paired with SNZB-02LD

## Next actions
1. **Tuesday** — pair SNZB-02LD + ZBDongle-E (Zigbee sensor) → temp live
2. **Saturday Jun 13 (Etap A)** — buy: 12× Raccoon Tetra, 4× Panda Garra, +2 Pearl Gouramis. Acclimate 45–60 min drip. Dose Stability 15ml.
3. **Sunday Jun 21** — first water change 15% (~38L)
4. **Thursday Jun 25 (Etap B)** — buy: 12× Purple Pencilfish, 6× Otocinclus

## DB reset (if needed before Etap A)
```bash
ssh <DEPLOYMENT_HOST_ALIAS> "cd /home/kamilo/nemo/ProjectNemo && docker compose down && docker volume rm projectnemo_nemo-db && docker compose up -d --no-deps nemo-api nemo-ui"
```

## OneDrive .git corruption fix
If git fails with "not a git repository":
```bash
mv "/c/.../ProjectNemo/.git/HEAD (# Name clash*)" "/c/.../ProjectNemo/.git/HEAD"
mv "/c/.../ProjectNemo/.git/index (# Name clash*)" "/c/.../ProjectNemo/.git/index"
```
