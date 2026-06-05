/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Confirmed UUIDs (nRF Connect, XX:XX:XX:XX:XX:XX):
 *   Service:    0000fff0-0000-1000-8000-00805f9b34fb
 *   FFF1: NOTIFY, FFF2: WRITE, FFF3: NOTIFY+WRITE
 *
 * Protocol: bare application frames — NO 0x54 encryption wrapper.
 * The 0x54 wrapper is for older Aquasky firmware only (NUS-based devices).
 * This device generation (Telink TLSR825x / 0xFFF0 service) uses raw frames.
 *
 * Frame A (0x68 header, from Aquasky protocol research):
 *   [0x68, CMD, ...data, XOR_CRC]
 *   CMD 0x02 = manual mode:  data=[0x00]
 *   CMD 0x04 = brightness:   data=[R_H,R_L, G_H,G_L, B_H,B_L, W_H,W_L] (0–1000 per channel)
 *
 * Frame B (LEN/SEQ header, Telink SDK template):
 *   [LEN, SEQ, 0x11, 0x02, R, G, B, W, XOR_CRC]
 *   R/G/B/W = 0–255
 *
 * Both variants tried in setChannels(); first non-empty notify response determines
 * which the device accepts.
 */

const SERVICE_UUID  = '0000fff0-0000-1000-8000-00805f9b34fb'
const FFF1_UUID     = '0000fff1-0000-1000-8000-00805f9b34fb'
const FFF2_UUID     = '0000fff2-0000-1000-8000-00805f9b34fb'
const FFF3_UUID     = '0000fff3-0000-1000-8000-00805f9b34fb'

let _device    = null
let _fff2      = null
let _fff3      = null
let _seq       = 0
let _modeSet   = false

// ---------------------------------------------------------------------------
// Frame builders
// ---------------------------------------------------------------------------

function _xorCrc(bytes) {
  return bytes.reduce((acc, b) => acc ^ b, 0)
}

/** Frame A: bare 0x68 header frame, no encryption wrapper */
function _frameA(cmd, data) {
  const frame = [0x68, cmd, ...data]
  frame.push(_xorCrc(frame))
  return new Uint8Array(frame)
}

/** Frame B: Telink SDK [LEN, SEQ, CMD_H, CMD_L, ...data, CRC] */
function _frameB(cmdH, cmdL, data) {
  const body = [_seq & 0xFF, cmdH, cmdL, ...data]
  const len  = body.length + 1  // +1 for LEN byte itself
  const crc  = _xorCrc(body)
  _seq = (_seq + 1) & 0xFF
  return new Uint8Array([len, ...body, crc])
}

// ---------------------------------------------------------------------------
// Write helpers
// ---------------------------------------------------------------------------

async function _write(char, pkt, label) {
  const hex = Array.from(pkt).map(b => b.toString(16).padStart(2,'0')).join(' ')
  console.log(`[fluval] ${label} → ${hex}`)
  try {
    if (char.writeValueWithoutResponse) {
      await char.writeValueWithoutResponse(pkt)
    } else {
      await char.writeValue(pkt)
    }
  } catch (err) {
    console.warn(`[fluval] write error on ${label}:`, err.message)
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

  // Subscribe FFF1 — some devices gate command processing until CCCD is written
  const fff1 = await service.getCharacteristic(FFF1_UUID)
  await fff1.startNotifications()
  fff1.addEventListener('characteristicvaluechanged', (e) => {
    const bytes = Array.from(new Uint8Array(e.target.value.buffer))
    console.log('[fluval] FFF1 notify:', bytes.map(b => b.toString(16).padStart(2,'0')).join(' '))
  })

  // Subscribe FFF3 notifications too
  _fff3 = await service.getCharacteristic(FFF3_UUID)
  await _fff3.startNotifications()
  _fff3.addEventListener('characteristicvaluechanged', (e) => {
    const bytes = Array.from(new Uint8Array(e.target.value.buffer))
    console.log('[fluval] FFF3 notify:', bytes.map(b => b.toString(16).padStart(2,'0')).join(' '))
  })

  _fff2    = await service.getCharacteristic(FFF2_UUID)
  _device  = device
  _modeSet = false
  _seq     = 0
  console.log('[fluval] connected — FFF1/FFF3 subscribed, will write to FFF2+FFF3')

  device.addEventListener('gattserverdisconnected', () => {
    _device = _fff2 = _fff3 = null
    _modeSet = false
    window.dispatchEvent(new CustomEvent('ble:disconnected'))
  })
}

export function isConnected() {
  return _device !== null && _device.gatt.connected
}

/**
 * Set all four channels (R, G, B, W), 0–100 percent.
 * Sends both Frame A and Frame B variants to both FFF2 and FFF3 —
 * one of the four combinations will be correct.
 * Once we confirm which works (from notify logs), prune the rest.
 */
export async function setChannels(r, g, b, w) {
  if (!_fff2 && !_fff3) throw new Error('BLE not connected')

  const toVal  = pct => Math.max(0, Math.min(100, Math.round(pct))) * 10
  const to255  = pct => Math.round(Math.max(0, Math.min(100, pct)) * 2.55)
  const [rv, gv, bv, wv] = [r, g, b, w].map(toVal)

  // --- Frame A: 0x68-header, values 0–1000 ---
  if (!_modeSet) {
    const modeA = _frameA(0x02, [0x00])
    if (_fff2) await _write(_fff2, modeA, 'FFF2 modeA')
    if (_fff3) await _write(_fff3, modeA, 'FFF3 modeA')
    _modeSet = true
  }

  const brightnessA = _frameA(0x04, [
    (rv >> 8) & 0xFF, rv & 0xFF,
    (gv >> 8) & 0xFF, gv & 0xFF,
    (bv >> 8) & 0xFF, bv & 0xFF,
    (wv >> 8) & 0xFF, wv & 0xFF,
  ])
  if (_fff2) await _write(_fff2, brightnessA, 'FFF2 frameA')
  if (_fff3) await _write(_fff3, brightnessA, 'FFF3 frameA')

  // --- Frame B: Telink [LEN,SEQ,0x11,0x02,R,G,B,W,CRC], values 0–255 ---
  const [r8, g8, b8, w8] = [r, g, b, w].map(to255)
  const brightnessB = _frameB(0x11, 0x02, [r8, g8, b8, w8])
  if (_fff2) await _write(_fff2, brightnessB, 'FFF2 frameB')
  if (_fff3) await _write(_fff3, brightnessB, 'FFF3 frameB')
}

export async function disconnect() {
  if (_device && _device.gatt.connected) _device.gatt.disconnect()
  _device = _fff2 = _fff3 = null
  _modeSet = false
}
