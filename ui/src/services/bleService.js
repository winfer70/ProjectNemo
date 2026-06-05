/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Confirmed UUIDs from nRF Connect (XX:XX:XX:XX:XX:XX):
 *   Service:    0000fff0-0000-1000-8000-00805f9b34fb  (0xFFF0)
 *   Write char: 0000fff2-0000-1000-8000-00805f9b34fb  (0xFFF2, WRITE + WRITE NO RESPONSE)
 *   Notify:     0000fff1-0000-1000-8000-00805f9b34fb  (0xFFF1, responses)
 *
 * Packet format (Aquasky 2.0 XOR protocol — unconfirmed for Roma, best known guess):
 *   XOR key: 0x0E
 *   Per-channel: [0x54, 0x03, 0x5A, ch, val>>8, val&0xFF]  (then XOR each byte)
 *   where val = clamp(percent, 0-100) * 10  (0–1000 scale)
 *   Channels: R=1, G=2, B=3, W=4
 */

const XOR_KEY      = 0x0E
const SERVICE_UUID = '0000fff0-0000-1000-8000-00805f9b34fb'
const WRITE_UUID   = '0000fff2-0000-1000-8000-00805f9b34fb'

const CH_R = 1
const CH_G = 2
const CH_B = 3
const CH_W = 4

let _device    = null
let _writeChar = null

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _xor(bytes) {
  return bytes.map(b => b ^ XOR_KEY)
}

function _buildPacket(channelId, percent) {
  const val = Math.max(0, Math.min(100, Math.round(percent))) * 10
  return new Uint8Array(_xor([0x54, 0x03, 0x5A, channelId, (val >> 8) & 0xFF, val & 0xFF]))
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

export async function connect() {
  const device = await navigator.bluetooth.requestDevice({
    filters: [
      { namePrefix: 'Roma&Shaker2.0_' },
      { namePrefix: 'Roma' },
      { namePrefix: 'Fluval' },
    ],
    optionalServices: [SERVICE_UUID],
  })

  const server = await device.gatt.connect()
  const service = await server.getPrimaryService(SERVICE_UUID)
  _writeChar = await service.getCharacteristic(WRITE_UUID)
  _device = device

  device.addEventListener('gattserverdisconnected', () => {
    _device = null
    _writeChar = null
    window.dispatchEvent(new CustomEvent('ble:disconnected'))
  })
}

export function isConnected() {
  return _device !== null && _device.gatt.connected && _writeChar !== null
}

/** r, g, b, w are 0–100 percent. */
export async function setChannels(r, g, b, w) {
  if (!_writeChar) throw new Error('BLE not connected — call connect() first')

  for (const [ch, val] of [[CH_R, r], [CH_G, g], [CH_B, b], [CH_W, w]]) {
    const pkt = _buildPacket(ch, val)
    if (_writeChar.writeValueWithoutResponse) {
      await _writeChar.writeValueWithoutResponse(pkt)
    } else {
      await _writeChar.writeValue(pkt)
    }
  }
}

export async function disconnect() {
  if (_device && _device.gatt.connected) {
    _device.gatt.disconnect()
  }
  _device = null
  _writeChar = null
}
