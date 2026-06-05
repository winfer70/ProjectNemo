/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Confirmed UUIDs (nRF Connect, XX:XX:XX:XX:XX:XX):
 *   Service:    0000fff0-0000-1000-8000-00805f9b34fb
 *   FFF1: NOTIFY, FFF2: WRITE, FFF3: NOTIFY+WRITE
 *
 * Protocol: still unknown — probing.
 * FFF3 is NOTIFY+WRITE (writable), suspicious for a "response only" char.
 * Trying FFF3 as the actual command channel in addition to FFF2.
 *
 * Frame variants sent on each setChannels():
 *   FFF2 A-8bit:   [0x68, 0x04, R, G, B, W, XOR_CRC]                 8-bit 0-255
 *   FFF2 A-16bit:  [0x68, 0x04, R_H,R_L, G_H,G_L, B_H,B_L, W_H,W_L, XOR] 16-bit 0-1000
 *   FFF2 MH:       [0x56, R, G, B, W, 0x00, 0xF0, 0xAA]              Magic Home / Zengge
 *   FFF3 A-8bit:   same A-8bit frame → FFF3
 *   FFF3 MH:       same MH frame → FFF3
 *
 * Watch console for FFF1/FFF3 notify lines — that identifies the working frame+char combo.
 * Once found, prune the rest and hardcode the winner.
 *
 * Write queue serializes all GATT writes — prevents "already in progress" errors.
 * setChannels is debounced 60ms to absorb rapid slider events.
 */

const SERVICE_UUID  = '0000fff0-0000-1000-8000-00805f9b34fb'
const FFF1_UUID     = '0000fff1-0000-1000-8000-00805f9b34fb'
const FFF2_UUID     = '0000fff2-0000-1000-8000-00805f9b34fb'
const FFF3_UUID     = '0000fff3-0000-1000-8000-00805f9b34fb'

let _device        = null
let _fff2          = null
let _fff3          = null
let _seq           = 0
let _modeSet       = false
let _writeChain    = Promise.resolve()
let _debounceTimer = null

// ---------------------------------------------------------------------------
// Frame builders
// ---------------------------------------------------------------------------

function _xorCrc(bytes) {
  return bytes.reduce((acc, b) => acc ^ b, 0)
}

/** [0x68, CMD, ...data, XOR_CRC] */
function _frameA(cmd, data) {
  const frame = [0x68, cmd, ...data]
  frame.push(_xorCrc(frame))
  return new Uint8Array(frame)
}

/** [LEN, SEQ, CMD_H, CMD_L, ...data, XOR_CRC] — Telink SDK template */
function _frameB(cmdH, cmdL, data) {
  const body = [_seq & 0xFF, cmdH, cmdL, ...data]
  const len  = body.length + 1
  const crc  = _xorCrc(body)
  _seq = (_seq + 1) & 0xFF
  return new Uint8Array([len, ...body, crc])
}

/** [0x56, R, G, B, W, 0x00, 0xF0, 0xAA] — Magic Home / Zengge protocol */
function _frameMH(r, g, b, w) {
  return new Uint8Array([0x56, r, g, b, w, 0x00, 0xF0, 0xAA])
}

// ---------------------------------------------------------------------------
// Serialized write queue — one ATT Write Request in flight at a time
// ---------------------------------------------------------------------------

function _enqueue(char, pkt, label) {
  _writeChain = _writeChain.then(async () => {
    const hex = Array.from(pkt).map(b => b.toString(16).padStart(2, '0')).join(' ')
    console.log(`[fluval] ${label} → ${hex}`)
    try {
      if (char.writeValueWithResponse) {
        await char.writeValueWithResponse(pkt)
      } else {
        await char.writeValue(pkt)
      }
    } catch (err) {
      console.warn(`[fluval] write error (${label}):`, err.message)
    }
  })
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

  const fff1 = await service.getCharacteristic(FFF1_UUID)
  await fff1.startNotifications()
  fff1.addEventListener('characteristicvaluechanged', (e) => {
    const bytes = Array.from(new Uint8Array(e.target.value.buffer))
    console.log('[fluval] FFF1 notify:', bytes.map(b => b.toString(16).padStart(2, '0')).join(' '))
  })

  _fff3 = await service.getCharacteristic(FFF3_UUID)
  await _fff3.startNotifications()
  _fff3.addEventListener('characteristicvaluechanged', (e) => {
    const bytes = Array.from(new Uint8Array(e.target.value.buffer))
    console.log('[fluval] FFF3 notify:', bytes.map(b => b.toString(16).padStart(2, '0')).join(' '))
  })

  _fff2       = await service.getCharacteristic(FFF2_UUID)
  _device     = device
  _modeSet    = false
  _seq        = 0
  _writeChain = Promise.resolve()
  console.log('[fluval] connected — FFF1/FFF3 subscribed, probing FFF2+FFF3')

  device.addEventListener('gattserverdisconnected', () => {
    _device = _fff2 = _fff3 = null
    _modeSet = false
    window.dispatchEvent(new CustomEvent('ble:disconnected'))
  })
}

export function isConnected() {
  return _device !== null && _device.gatt.connected
}

/** Debounced: rapid slider events collapse into one write per 60ms */
export function setChannels(r, g, b, w) {
  if (!_fff2) return
  clearTimeout(_debounceTimer)
  _debounceTimer = setTimeout(() => _doSetChannels(r, g, b, w), 60)
}

function _doSetChannels(r, g, b, w) {
  if (!_fff2) return

  const clamp  = v => Math.max(0, Math.min(100, Math.round(v)))
  const to255  = v => Math.round(clamp(v) * 2.55)
  const to1000 = v => clamp(v) * 10

  if (!_modeSet) {
    // manual mode on both chars
    _enqueue(_fff2, _frameA(0x02, [0x00]), 'FFF2 mode')
    _enqueue(_fff3, _frameA(0x02, [0x00]), 'FFF3 mode')
    _modeSet = true
  }

  const r8 = to255(r), g8 = to255(g), b8 = to255(b), w8 = to255(w)
  const rv = to1000(r), gv = to1000(g), bv = to1000(b), wv = to1000(w)
  const data16 = [
    (rv >> 8) & 0xFF, rv & 0xFF,
    (gv >> 8) & 0xFF, gv & 0xFF,
    (bv >> 8) & 0xFF, bv & 0xFF,
    (wv >> 8) & 0xFF, wv & 0xFF,
  ]

  // FFF2 probes
  _enqueue(_fff2, _frameA(0x04, [r8, g8, b8, w8]), 'FFF2 A-8bit')
  _enqueue(_fff2, _frameA(0x04, data16),             'FFF2 A-16bit')
  _enqueue(_fff2, _frameMH(r8, g8, b8, w8),          'FFF2 MH')

  // FFF3 probes — same frames to the writable NOTIFY+WRITE char
  _enqueue(_fff3, _frameA(0x04, [r8, g8, b8, w8]), 'FFF3 A-8bit')
  _enqueue(_fff3, _frameMH(r8, g8, b8, w8),          'FFF3 MH')
}

export function disconnect() {
  clearTimeout(_debounceTimer)
  if (_device && _device.gatt.connected) _device.gatt.disconnect()
  _device = _fff2 = _fff3 = null
  _modeSet = false
}
