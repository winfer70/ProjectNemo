# HANDOFF — ProjectNemo
Date: 2026-09-01 (session wrap)

## Current state
- Git `dev` vs live vesemir HA: **live `automations.yaml` was edited 2026-08-31** (office strip move) and is **not committed**. Backup on vesemir: `automations.yaml.bak_` (same day).
- Secrets rotation 2026-09-01 updated live `homeassistant/config/secrets.yaml` and ProjectNemo `.env` `INFLUXDB_INIT_ADMIN_TOKEN`. Git copies stay placeholders. Do not commit live secrets.
- InfluxDB (`nemo-influxdb`) and HA (`nemo-homeassistant`) were restarted during rotation; both came back.

## This session (HA)

Moved **office automations** from device **AkwariumSalon** (Meross `smart_switch_201117…`) to **ListwaBiuro** (`switch.0xa4c1387daaa98e50_l1`–`_l5`):

| Automation | Notes |
|---|---|
| Office Aqara single press | `c3c16e19` — mapped by function (monitors/dock/LED/USB) |
| Office Aqara double press | `ae080d72` — no master switch; toggles all l1–l5 + `switch.office_led` |
| Desk WłącznikBiurko | `c3eeeffd` — master pre-power branch removed |

User tested buttons: **working**. Those three automations were **disabled** (`off`) at reload time — user enabled them for the test.

Mapping used:
- `_outlet_1` → `_l1` Monitor_1
- `_outlet_2` → `_l2` Monitor_2
- `_outlet_3` → `_l4` Biurko_LED
- `_outlet_4` → `_l3` StacjaDokująca
- `_outlet_5` → `_l5` Usb desk led
- master `_outlet` → all l1–l5 (Zigbee strip has no master)

## Do next

1. **Satel keypad:** set PIN to match HA `alarm_code` (see HomeAI HANDOFF / `rotated-alarm-pin.txt`). Until then `alarm_auto_arm_away_presence` / `alarm_auto_disarm_presence` will fail.
2. Commit live `automations.yaml` from vesemir onto a `feature/` branch from `dev` (diff vs git; do not commit `secrets.yaml`).
3. ntfy app + tablet UI (still pending).
4. Pre-existing `influxdb.include.component_config` schema bug — not this session.

## Blockers
Satel PIN mismatch until keypad is updated. Do not call alarm services to “test” the new code from an agent.
