from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ha_url: str = "http://homeassistant:8123"
    ha_token: str = ""
    # Optional - HA conversation agent entity id to target (e.g. Kamilo/Heimdall's
    # pipeline agent). Empty = HA's default configured conversation agent.
    ha_conversation_agent_id: str = ""
    # Optional - HA calendar entity id to push maintenance due-dates to (e.g.
    # a Google Calendar synced into HA via Settings > Devices & Services >
    # Add Integration > Google). Requires that integration to be configured
    # in HA first - unset (None) until then, which keeps the sync a no-op.
    ha_calendar_entity_id: str | None = None

    influxdb_url: str = "http://influxdb:8086"
    influxdb_token: str = ""
    influxdb_org: str = "nemo"
    influxdb_bucket: str = "aquarium"

    mqtt_host: str = "mosquitto"
    mqtt_port: int = 1883
    mqtt_username: str = "nemo"
    mqtt_password: str = ""

    n8n_base_url: str = ""
    n8n_webhook_alert: str = ""
    n8n_webhook_reminder: str = ""
    n8n_webhook_supply: str = ""
    n8n_webhook_daily: str = ""
    telegram_lang: str = "both"

    ntfy_url: str = ""
    ntfy_topic: str = "aquarium"
    ntfy_token: str = ""

    tapo_filter_entity: str = "switch.tapo_filter"
    tapo_heater_entity: str = "switch.tapo_heater"
    tapo_light_entity: str = "switch.tapo_light"
    tapo_air_entity: str = "switch.tapo_air_pump"

    # Tank 2 (Akwarium Salon) - single Zigbee power strip (Zigbee2MQTT,
    # 0xa4c1387daaa98e50), individually controlled outlets: L1 light, L2
    # heater, L3 filters, L4 cabinet LED, L5 USB. No separate air pump outlet:
    # filter+pump share L3, so feeding-pause only toggles tapo_filter_entity_2.
    # (Was the Meross strip until 2026-10-08; that one is back in the office.)
    tapo_filter_entity_2: str = "switch.0xa4c1387daaa98e50_l3"
    tapo_heater_entity_2: str = "switch.0xa4c1387daaa98e50_l2"
    tapo_light_entity_2: str = "switch.0xa4c1387daaa98e50_l1"

    fluval_ble_mac: str = ""
    esphome_temp_entity: str = "sensor.nemo_sensor_temperature"
    esphome_ph_entity: str = "sensor.nemo_sensor_ph"
    zigbee_temp_entity: str = "sensor.0xa4c138060885ffff_temperature"
    tank_1_name: str = "Akwarium Kuchnia"
    zigbee_temp_entity_2: str = "sensor.0xa4c138061c90ffff_temperature"
    tank_2_name: str = "Akwarium Salon"

    ollama_url: str = ""
    searxng_url: str = ""

    api_secret_key: str = ""
    log_level: str = "info"

    db_path: str = "/app/data/nemo.db"


settings = Settings()
