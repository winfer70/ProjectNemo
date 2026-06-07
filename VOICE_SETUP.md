# Voice Assistant Setup — Alexa via emulated_hue

## What works
"Alexa, turn on the aquarium light"
"Alexa, turn off the aquarium filter"
"Alexa, feed the fish"  (triggers HA script → pauses filter 10 min)

## How it works
Home Assistant's `emulated_hue` integration makes HA impersonate a Philips Hue bridge.
Alexa discovers HA entities on the LAN. No cloud subscription, no Nabu Casa, no monthly cost.

## Requirements
- Alexa device on the same LAN as REDACTED-HOST
- HA container must bind port 80 (docker-compose.yml already sets this)
- emulated_hue configured in configuration.yaml (already done)

## Setup Steps

### 1. Verify port 80 binding
```bash
docker compose ps | grep homeassistant
# Should show 0.0.0.0:80->80/tcp
```

### 2. Check emulated_hue config in homeassistant/config/configuration.yaml
Entities exposed:
- switch.tapo_light → "Aquarium Light"
- switch.tapo_filter → "Aquarium Filter"
- switch.tapo_heater → "Aquarium Heater"
- script.feed_fish → "Feed Fish"

### 3. Discover devices in Alexa app
1. Open Alexa app → Devices → (+) → Add Device → Other
2. Tap "Discover Devices"
3. Wait ~30 seconds — Alexa scans LAN for Hue bridges
4. The 4 entities above should appear as smart plugs

### 4. Test voice commands
- "Alexa, turn on aquarium light" → light switches on
- "Alexa, feed the fish" → filter pauses 10 min, then auto-restarts

## Troubleshooting
- Alexa can't find devices: ensure Alexa device is on the same VLAN as REDACTED-HOST
- Check HA logs: `docker logs nemo-homeassistant | grep emulated_hue`
- Port 80 conflict: if another service uses port 80 on REDACTED-HOST, change the HA port
  mapping in docker-compose.yml and update `listen_port` in emulated_hue config

## Google Home (future)
Dropped for now — requires Nabu Casa ($6.50/mo). May revisit if a free local option appears.
