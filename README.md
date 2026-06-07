# Project Nemo — Quick Start

## First-time deploy on REDACTED-HOST

```bash
# 1. Clone / copy project to REDACTED-HOST
cd /opt/nemo

# 2. Configure
cp .env.example .env
nano .env   # fill in HA token, InfluxDB token, domain, n8n webhook IDs

# Also edit homeassistant/config/secrets.yaml with mqtt_password, influxdb_token, lan_ip

# 3. Generate Mosquitto password
docker compose up -d mosquitto
docker exec -it nemo-mosquitto mosquitto_passwd -c /mosquitto/config/passwd nemo
# → enter password matching MQTT_PASSWORD in .env
docker compose restart mosquitto

# 4. Start everything
docker compose up -d

# 5. Home Assistant first run
# Open http://[LAN_IP]:8123 → create account → follow onboarding
# Add integrations: TP-Link Tapo, ESPHome (auto-discovers after ESP32 flashed)

# 6. Flash ESP32
cd firmware
esphome run nemo-sensor.yaml
# After first boot: copy DS18B20 address from serial output → edit nemo-sensor.yaml
# Calibrate pH: measure raw voltage at pH 4.0 and pH 7.0 buffers → edit calibrate_linear
# Reflash: esphome run nemo-sensor.yaml

# 7. Test dashboard
open http://[LAN_IP]:3000
```

## Service ports
| Service | Port | Access |
|---------|------|--------|
| Nemo Dashboard | 3000 | LAN + https://nemo.[domain] |
| Nemo API | 8000 | Internal |
| Home Assistant | 8123 | LAN only (internal) |
| InfluxDB | 8086 | Internal |
| Zigbee2MQTT UI | 8080 | LAN |
| Mosquitto MQTT | 1883 | Internal |

## Useful commands
```bash
docker compose logs -f nemo-api      # API logs
docker compose logs -f homeassistant # HA logs
docker compose restart nemo-api      # restart after code changes
docker compose pull && docker compose up -d  # update all images
```

## Project structure
```
ProjectNemo/
├── docker-compose.yml          ← Start here
├── .env.example                ← Copy to .env
├── homeassistant/config/       ← HA config + custom Fluval BLE component
├── mosquitto/config/           ← MQTT broker config
├── zigbee2mqtt/config/         ← Zigbee coordinator config
├── nginx/conf.d/               ← Reverse proxy for public subdomain
├── api/                        ← FastAPI backend (Python)
├── ui/                         ← Vue 3 frontend
├── firmware/                   ← ESPHome config + wiring guide
├── N8N_SETUP.md                ← Telegram notification workflow guide
├── VOICE_SETUP.md              ← Alexa emulated_hue setup
├── TABLET_SETUP.md             ← Fully Kiosk Browser kiosk config
├── STOCKING_PLAN.md            ← Aquarium stocking stages + timeline
├── SUPPLIES.md                 ← Consumables + dosing reference
└── SENSORS.md                  ← Hardware purchase guide with prices
```
