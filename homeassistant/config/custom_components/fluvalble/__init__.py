"""Fluval Shaker RGBW BLE custom component for Home Assistant.

Extends mrzottel/fluvalble to expose all 5 channels as number entities
(R, G, B, W, and the undocumented channel 5 / moonlight).

Protocol (reverse-engineered):
  - GATT char: 00001002-0000-1000-8000-00805f9b34fb
  - Header: [0x54, payload_len, 0x5A]
  - XOR cipher: each byte XOR 0x0E
  - Channel values: 0–1000 (mapped to 0–100% in HA)
  - Command format: [channel_byte, val_high, val_low, ...]
"""
DOMAIN = "fluvalble"
