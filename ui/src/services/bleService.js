/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Actual service/char UUIDs determined by discoverServices() at first connect.
 * Once confirmed, SERVICE_UUID / WRITE_UUID / REGISTER_UUID can be hardcoded.
 *
 * Color packet: [0x54, r, g, b, w]  values 0-100, no XOR.
 */

// Candidate service UUIDs — all must be in optionalServices at requestDevice time.
const CANDIDATE_SERVICES = [
  '00001001-0000-1000-8000-00805f9b34fb', // Aquasky 2.0 (most likely match)
  '00001000-0000-1000-8000-00805f9b34fb', // Roma AI claim (wrong, kept for fallback)
  '0000180a-0000-1000-8000-00805f9b34fb', // Device Information
  '0000ffe0-0000-1000-8000-00805f9b34fb', // Generic custom
  '0000fff0-0000-1000-8000-00805f9b34fb', // Generic custom
]

// Known char UUIDs inside the control service
const WRITE_UUID    = '00001002-0000-1000-8000-00805f9b34fb' // Aquasky write char
const REGISTER_UUID = '00001005-0000-1000-8000-00805f9b34fb'

let _device    = null
let _writeChar = null

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _clamp(v) {
  return Math.max(0, Math.min(100, Math.round(v)))
}

/**
 * Walk all primary services, log their UUIDs + char UUIDs, return a
 * human-readable string. Used for diagnostics when init fails.
 */
async function _dumpServices(server) {
  try {
    const services = await server.getPrimaryServices()
    const lines = []
    for (const svc of services) {
      let charList = ''
      try {
        const chars = await svc.getCharacteristics()
        charList = chars.map(c => c.uuid).join(', ')
      } catch (_) { charList = '(no access)' }
      lines.push(`SVC ${svc.uuid} → [${charList}]`)
    }
    return lines.join('\n') || 'no services found'
  } catch (e) {
    return `getPrimaryServices failed: ${e.message}`
  }
}

async function _initSession(server) {
  // Try each candidate service until one exists on this device.
  let service = null
  let foundUUID = null
  for (const uuid of CANDIDATE_SERVICES) {
    try {
      service = await server.getPrimaryService(uuid)
      foundUUID = uuid
      break
    } catch (_) { /* not present */ }
  }

  if (!service) {
    const dump = await _dumpServices(server)
    throw new Error(`No matching service found.\n${dump}`)
  }

  console.log(`[BLE] Connected via service ${foundUUID}`)

  // Try register char (optional — not all firmware versions need it)
  try {
    const regChar = await service.getCharacteristic(REGISTER_UUID)
    await regChar.writeValue(new Uint8Array([0x0F]))
  } catch (_) { /* char may not exist on this model */ }

  // Locate write characteristic
  let writeChar = null
  try {
    writeChar = await service.getCharacteristic(WRITE_UUID)
  } catch (_) {
    // Fallback: use first writable characteristic in the service
    const chars = await service.getCharacteristics()
    writeChar = chars.find(c => c.properties.write || c.properties.writeWithoutResponse)
    if (!writeChar) throw new Error(`No writable char in service ${foundUUID}`)
    console.log(`[BLE] Using fallback write char ${writeChar.uuid}`)
  }

  // Time sync
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

  // Switch to manual mode (override Pro/Auto schedule)
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
    optionalServices: CANDIDATE_SERVICES,
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

/** r, g, b, w are 0–100 percent. Matches FluvalConnect: Red, Green, Blue, White. */
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
