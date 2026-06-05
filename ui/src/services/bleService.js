/**
 * Fluval Aquasky 2.0 — Web Bluetooth singleton service.
 *
 * Packet format (mirrors homeassistant/config/custom_components/fluvalble/protocol.py):
 *   full_packet = [0x54, payload_len, 0x5A, ...payload]
 *   on-wire     = each byte ^ 0x0E
 *
 * Single-channel payload: [channel_id, raw >> 8, raw & 0xFF]
 *   where raw = clamp(percent, 0, 100) * 10  (0–1000 range)
 */

const XOR_KEY = 0x0E
const WRITE_CHAR_UUID = '00001002-0000-1000-8000-00805f9b34fb'
const SERVICE_DISCOVERY = '0000180a-0000-1000-8000-00805f9b34fb'
const SERVICE_CONTROL = '00001001-0000-1000-8000-00805f9b34fb'

const CHANNEL_R = 0x01
const CHANNEL_G = 0x02
const CHANNEL_B = 0x03
const CHANNEL_W = 0x04
const CHANNEL_5 = 0x05

// Module-level singletons — bleService is intentionally not a class.
let _device = null
let _char = null

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _xorEncrypt(bytes) {
  return bytes.map(b => b ^ XOR_KEY)
}

/**
 * Build the on-wire Uint8Array for a single-channel command.
 * Matches build_single_channel_command() in protocol.py.
 */
function _buildSingleChannelPacket(channelId, percent) {
  const raw = Math.max(0, Math.min(100, percent)) * 10
  const payload = [channelId, (raw >> 8) & 0xFF, raw & 0xFF]
  const header = [0x54, payload.length, 0x5A]
  return new Uint8Array(_xorEncrypt([...header, ...payload]))
}

/**
 * Iterate all primary GATT services and return the first characteristic
 * whose UUID matches WRITE_CHAR_UUID.
 * The write char lives in SERVICE_CONTROL (0x1001), but we iterate defensively.
 */
async function _findWriteChar(server) {
  const services = await server.getPrimaryServices()
  for (const svc of services) {
    try {
      const chars = await svc.getCharacteristics()
      for (const c of chars) {
        if (c.uuid === WRITE_CHAR_UUID) return c
      }
    } catch (_err) {
      // Service may not expose characteristics — skip silently.
    }
  }
  throw new Error(`Write characteristic ${WRITE_CHAR_UUID} not found on any GATT service`)
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Prompt the user to select a Fluval / Aquasky device and open GATT.
 * Must be called from a user-gesture handler (button click).
 *
 * Falls back to acceptAllDevices if the name-prefix filter finds nothing —
 * useful when the device is not actively advertising its name.
 */
export async function connect() {
  let device
  try {
    device = await navigator.bluetooth.requestDevice({
      filters: [
        { namePrefix: 'Fluval' },
        { namePrefix: 'Aquasky' },
      ],
      optionalServices: [SERVICE_CONTROL, SERVICE_DISCOVERY],
    })
  } catch (_filterErr) {
    // Name filters yielded nothing — open the full picker.
    device = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: [SERVICE_CONTROL, SERVICE_DISCOVERY],
    })
  }

  const server = await device.gatt.connect()
  _char = await _findWriteChar(server)
  _device = device

  // Notify the app when the peripheral drops the connection.
  device.addEventListener('gattserverdisconnected', () => {
    _device = null
    _char = null
    window.dispatchEvent(new CustomEvent('ble:disconnected'))
  })
}

/** Returns true when a GATT connection is open and the write char is ready. */
export function isConnected() {
  return _device !== null && _device.gatt.connected && _char !== null
}

/**
 * Write one GATT command per channel (r, g, b, w, ch5 are 0–100 percent).
 * Mirrors the single-channel loop used by the HA custom component.
 */
export async function setChannels(r, g, b, w, ch5 = 0) {
  if (!_char) throw new Error('BLE not connected — call connect() first')

  const channelMap = [
    [CHANNEL_R, r],
    [CHANNEL_G, g],
    [CHANNEL_B, b],
    [CHANNEL_W, w],
    [CHANNEL_5, ch5],
  ]

  for (const [id, val] of channelMap) {
    const packet = _buildSingleChannelPacket(id, val)
    // writeValueWithoutResponse is the correct ATT Write Command for lighting.
    // Falls back to the older writeValue for browsers that don't yet expose it.
    if (_char.writeValueWithoutResponse) {
      await _char.writeValueWithoutResponse(packet)
    } else {
      await _char.writeValue(packet)
    }
  }
}

/** Close the GATT connection and clear all module state. */
export async function disconnect() {
  if (_device && _device.gatt.connected) {
    _device.gatt.disconnect()
  }
  _device = null
  _char = null
}
