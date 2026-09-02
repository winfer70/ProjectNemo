from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ha_url: str = "http://homeassistant:8123"
    ha_token: str = ""

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

    # Tank 2 (Akwarium Salon) - single Meross power strip, individually
    # controlled outlets. No separate air pump outlet: filter+pump share one
    # switch, so feeding-pause only needs to toggle tapo_filter_entity_2.
    tapo_filter_entity_2: str = "switch.smart_switch_20111713503031290d1748e1e93cb12d_outlet_2"
    tapo_heater_entity_2: str = "switch.smart_switch_20111713503031290d1748e1e93cb12d_outlet_3"
    tapo_light_entity_2: str = "switch.smart_switch_20111713503031290d1748e1e93cb12d_outlet_1"

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
