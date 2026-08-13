# ProjectNemo

Aquarium monitoring and automation system. Built, not yet deployed.

## Stack

- **UI**: Vue 3 + Vite + Pinia (stores: sensors, maintenance, schedule, waterTests)
- **API**: FastAPI (Python) — routers: sensors, dosing, maintenance, schedule, supplies, water_tests, devices
- **Services**: Home Assistant (HA), InfluxDB, n8n, MQTT (Mosquitto), Zigbee2MQTT
- **Firmware**: ESPHome (`firmware/nemo-sensor.yaml`) — temperature, pH, salinity sensors
- **Custom HA component**: `fluvalble` — BLE-controlled Fluval aquarium light (config_flow, number, protocol)
- **Deploy target**: docker-compose.yml (all services in one stack)

## Current State

Deployed and running on the **deployment host** (`<DEPLOYMENT_HOST_LAN_IP>` wired / `<DEPLOYMENT_HOST_WIFI_IP>` WiFi, SSH alias `<DEPLOYMENT_HOST_ALIAS>`).
Code lives at `/home/kamilo/nemo/ProjectNemo/`. Services: nemo-ui :3000, nemo-api :8000, nemo-homeassistant :8123, nemo-influxdb :8086, nemo-mosquitto :1883.
Next action: Tapo P110 HA integration (add in HA UI → get entity IDs → update `.env` TAPO_*).

## Key Files

- `docker-compose.yml` — full stack definition
- `api/main.py` — FastAPI entry point
- `ui/src/App.vue` — main UI shell
- `homeassistant/config/custom_components/fluvalble/` — custom HA integration
- `firmware/nemo-sensor.yaml` — ESPHome sensor config
- `N8N_SETUP.md`, `TABLET_SETUP.md`, `VOICE_SETUP.md` — integration docs

## Branch Rules

- Integration branch: `dev`
- All work on `feature/<name>` branches — never commit directly to `dev` or `main`
- Deploy only via `./release.sh` — merges dev→main, SQLite backup, docker compose up --build
- Prod target: deployment host `<DEPLOYMENT_HOST_LAN_IP>` (wired) / `<DEPLOYMENT_HOST_WIFI_IP>` (WiFi), SSH user `kamilo`
- `.env` and `homeassistant/config/secrets.yaml` NOT in git — already on the deployment host

## graphify

This project has a graphify knowledge graph at `graphify-out/`.

Rules:
- Before answering architecture or codebase questions, read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure
- If `graphify-out/wiki/index.md` exists, navigate it instead of reading raw files
- After modifying code files in this session, run `PYTHONUTF8=1 python -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
