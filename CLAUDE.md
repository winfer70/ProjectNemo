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

Built and working locally. Not deployed to any server. Next action: deploy to a server (likely REDACTED-HOST or REDACTED-HOST).

## Key Files

- `docker-compose.yml` — full stack definition
- `api/main.py` — FastAPI entry point
- `ui/src/App.vue` — main UI shell
- `homeassistant/config/custom_components/fluvalble/` — custom HA integration
- `firmware/nemo-sensor.yaml` — ESPHome sensor config
- `N8N_SETUP.md`, `TABLET_SETUP.md`, `VOICE_SETUP.md` — integration docs

## graphify

No graphify graph yet. Run `graphify hook install` then `graphify claude install` to set up.
After setup, read `graphify-out/GRAPH_REPORT.md` before answering architecture questions.
