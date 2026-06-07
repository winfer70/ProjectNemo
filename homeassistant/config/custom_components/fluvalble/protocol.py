"""Fluval Shaker BLE protocol implementation."""
from __future__ import annotations

XOR_KEY = 0x0E
GATT_CHAR_UUID = "00001002-0000-1000-8000-00805f9b34fb"

CHANNEL_R = 0x01
CHANNEL_G = 0x02
CHANNEL_B = 0x03
CHANNEL_W = 0x04
CHANNEL_5 = 0x05   # UV / moonlight — undocumented

PERCENT_TO_RAW = 10   # 100% = 1000 raw


def _xor_encrypt(data: bytes) -> bytes:
    return bytes(b ^ XOR_KEY for b in data)


def build_set_channels_command(r: int, g: int, b: int, w: int, ch5: int = 0) -> bytes:
    """
    Build the BLE write payload for setting all channels simultaneously.
    r, g, b, w, ch5 are 0–100 percent values.
    """
    def pack_channel(ch_id: int, percent: int) -> list[int]:
        raw = max(0, min(100, percent)) * PERCENT_TO_RAW
        return [ch_id, (raw >> 8) & 0xFF, raw & 0xFF]

    payload = []
    for ch_id, val in [
        (CHANNEL_R, r),
        (CHANNEL_G, g),
        (CHANNEL_B, b),
        (CHANNEL_W, w),
        (CHANNEL_5, ch5),
    ]:
        payload.extend(pack_channel(ch_id, val))

    header = [0x54, len(payload), 0x5A]
    full_packet = header + payload
    return _xor_encrypt(bytes(full_packet))


def build_single_channel_command(channel_id: int, percent: int) -> bytes:
    """Build command to update a single channel without touching others."""
    raw = max(0, min(100, percent)) * PERCENT_TO_RAW
    payload = [channel_id, (raw >> 8) & 0xFF, raw & 0xFF]
    header = [0x54, len(payload), 0x5A]
    return _xor_encrypt(bytes(header + payload))
