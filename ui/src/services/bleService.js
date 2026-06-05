/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Confirmed UUIDs (nRF Connect, XX:XX:XX:XX:XX:XX):
 *   Service:    0000fff0-0000-1000-8000-00805f9b34fb
 *   Write char: 0000fff2-0000-1000-8000-00805f9b34fb  (WRITE NO RESPONSE)
 *   Notify:     0000fff1-0000-1000-8000-00805f9b34fb
 *
 * Fluval application frame protocol (from APK DEX analysis):
 *   App frame:  [0x68, CMD, ...data, CRC]  — CRC = XOR of all bytes
 *   Encryption: [0x54, (len+1)^0x54, keyByte, ...payload]
 *     rand=0 (newer, Roma/Shaker 2.0): keyByte=0x54, no XOR on payload
 *     old (Aquasky 2.0):               keyByte=0x5A, payload XOR 0x0E
 *
 *   CMD 0x02 = set mode:   data=[0x00] → manual (must send before brightness)
 *   CMD 0x03 = on/off:     data=[0x00]=off, [0x01]=on
 *   CMD 0x04 = brightness: data=[ch1_H, ch1_L, ch2_H, ch2_L, ch3_H, ch3_L, ch4_H, ch4_L]
 *              channel order: R=ch1, G=ch2, B=ch3, W=ch4
 *              values 0–1000 (percent × 10), 16-bit big-endian
 */

const SERVICE_UUID = '0000fff0-0000-1000-8000-00805f9b34fb'
const WRITE_UUID   = '0000fff2-0000-1000-8000-00805f9b34fb'

let _device     = null
let _writeChar  = null
let _modeSet    = false   // track whether we've sent manual mode this session

// ---------------------------------------------------------------------------
// Protocol helpers
// ---------------------------------------------------------------------------

function _crc(bytes) {
  return bytes.reduce((acc, b) => acc ^ b, 0)
}

/** Build Fluval application frame: [0x68, cmd, ...data, CRC] */
function _buildFrame(cmd, data) {
  const frame = [0x68, cmd, ...data]
  frame.push(_crc(frame))
  return frame
}

/**
 * Encrypt payload into wire packet.
 * useOldXor=false → rand=0 variant (Roma/Shaker 2.0, newer devices)
 * useOldXor=true  → 0x0E XOR variant (Aquasky 2.0, older devices)
 */
function _encrypt(payload, useOldXor = false) {
  const keyByte = useOldXor ? 0x5A : 0x54
  const xorKey  = useOldXor ? 0x0E : 0x00
  const encrypted = xorKey ? payload.map(b => b ^ xorKey) : [...payload]
  const lenByte = ((payload.length + 1) ^ 0x54) & 0xFF
  return new Uint8Array([0x54, lenByte, keyByte, ...encrypted])
}

async function _write(bytes) {
  if (!_writeChar) throw new Error('BLE not connected — call connect() first')
  const pkt = _encrypt(_buildFrame(...bytes))
  if (_writeChar.writeValueWithoutResponse) {
    await _writeChar.writeValueWithoutResponse(pkt)
  } else {
    await _writeChar.writeValue(pkt)
  }
}

async function _sendFrame(cmd, data) {
  const frame = _buildFrame(cmd, data)
  const pkt   = _encrypt(frame)
  if (!_writeChar) throw new Error('BLE not connected — call connect() first')
  if (_writeChar.writeValueWithoutResponse) {
    await _writeChar.writeValueWithoutResponse(pkt)
  } else {
    await _writeChar.writeValue(pkt)
  }
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

  const server  = await device.gatt.connect()
  const service = await server.getPrimaryService(SERVICE_UUID)
  _writeChar = await service.getCharacteristic(WRITE_UUID)
  _device    = device
  _modeSet   = false

  device.addEventListener('gattserverdisconnected', () => {
    _device    = null
    _writeChar = null
    _modeSet   = false
    window.dispatchEvent(new CustomEvent('ble:disconnected'))
  })
}

export function isConnected() {
  return _device !== null && _device.gatt.connected && _writeChar !== null
}

/**
 * Set all four channels (R, G, B, W) in one CMD 0x04 packet.
 * Automatically sends CMD 0x02 manual-mode override on first call.
 * r, g, b, w are 0–100 percent.
 */
export async function setChannels(r, g, b, w) {
  if (!_writeChar) throw new Error('BLE not connected — call connect() first')

  // Ensure device is in manual mode (overrides Pro/Auto schedule)
  if (!_modeSet) {
    await _sendFrame(0x02, [0x00])
    _modeSet = true
  }

  const toVal = pct => Math.max(0, Math.min(100, Math.round(pct))) * 10
  const vals  = [r, g, b, w].map(toVal)

  const data = []
  for (const v of vals) {
    data.push((v >> 8) & 0xFF, v & 0xFF)
  }

  await _sendFrame(0x04, data)
}

export async function disconnect() {
  if (_device && _device.gatt.connected) {
    _device.gatt.disconnect()
  }
  _device    = null
  _writeChar = null
  _modeSet   = false
}
