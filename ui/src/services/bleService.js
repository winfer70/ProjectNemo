/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Protocol (reverse-engineered, Roma&Shaker2.0 generation):
 *   Service:   00001000-0000-1000-8000-00805f9b34fb
 *   Write:     00001001-0000-1000-8000-00805f9b34fb
 *   Register:  00001005-0000-1000-8000-00805f9b34fb
 *
 * Init sequence (required before color commands):
 *   1. Write [0x0F] to register char 1005
 *   2. Write time-sync array [yy, mm, dd, dow, hh, min, sec] to write char 1001
 *
 * Color packet (write char 1001):
 *   [0x54, ch1_pink, ch2_blue, ch3_cold_white, ch4_warm_white]
 *   Values 0–100 (no XOR encoding on this generation).
 *
 * Channel mapping from UI (r, g, b, w):
 *   r → ch1 Red
 *   g → ch2 Green
 *   b → ch3 Blue
 *   w → ch4 White
 */

const SERVICE_UUID   = '00001000-0000-1000-8000-00805f9b34fb'
const WRITE_UUID     = '00001001-0000-1000-8000-00805f9b34fb'
const REGISTER_UUID  = '00001005-0000-1000-8000-00805f9b34fb'

let _device   = null
let _writeChar = null

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _clamp(v) {
  return Math.max(0, Math.min(100, Math.round(v)))
}

async function _initSession(server) {
  const service = await server.getPrimaryService(SERVICE_UUID)

  // Step 1: wake the hardware register
  const regChar = await service.getCharacteristic(REGISTER_UUID)
  await regChar.writeValue(new Uint8Array([0x0F]))

  // Step 2: sync light's internal clock
  const writeChar = await service.getCharacteristic(WRITE_UUID)
  const now = new Date()
  await writeChar.writeValue(new Uint8Array([
    now.getFullYear() % 100,
    now.getMonth() + 1,
    now.getDate(),
    now.getDay(),
    now.getHours(),
    now.getMinutes(),
    now.getSeconds(),
  ]))

  // Step 3: switch to manual mode (overrides Pro/Auto schedule)
  await writeChar.writeValue(new Uint8Array([0x52, 0x00]))

  return writeChar
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
  _writeChar = await _initSession(server)
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

/**
 * r, g, b, w are 0–100 percent. Matches FluvalConnect: Red, Green, Blue, White.
 */
export async function setChannels(r, g, b, w) {
  if (!_writeChar) throw new Error('BLE not connected — call connect() first')

  const packet = new Uint8Array([0x54, _clamp(r), _clamp(g), _clamp(b), _clamp(w)])
  await _writeChar.writeValue(packet)
}

export async function disconnect() {
  if (_device && _device.gatt.connected) {
    _device.gatt.disconnect()
  }
  _device = null
  _writeChar = null
}
