/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * Confirmed UUIDs (nRF Connect, XX:XX:XX:XX:XX:XX):
 *   Service:    0000fff0-0000-1000-8000-00805f9b34fb
 *   FFF1: NOTIFY, FFF2: WRITE, FFF3: NOTIFY+WRITE
 *
 * Protocol: bare application frames — NO 0x54 encryption wrapper.
 *
 * Frames tried (watch FFF1/FFF3 notify in console to see which gets a response):
 *   Frame A-8:  [0x68, CMD, R, G, B, W, XOR_CRC]           — 8-bit 0-255
 *   Frame AL-8: [0x68, LEN, CMD, R, G, B, W, XOR_CRC]      — 8-bit with length byte
 *   Frame A-16: [0x68, CMD, R_H,R_L, G_H,G_L, B_H,B_L, W_H,W_L, XOR_CRC]  — 16-bit 0-1000
 *   Frame B:    [LEN, SEQ, 0x11, 0x02, R, G, B, W, XOR_CRC] — Telink SDK template
 *
 *   CMD 0x02 = manual mode (sent once on first setChannels call)
 *   CMD 0x04 = set brightness
 *
 * Write queue serializes all GATT writes — prevents "already in progress" errors.
 * setChannels is debounced 60ms to absorb rapid slider events.
 */

const SERVICE_UUID  = '0000fff0-0000-1000-8000-00805f9b34fb'
const FFF1_UUID     = '0000fff1-0000-1000-8000-00805f9b34fb'
const FFF2_UUID     = '0000fff2-0000-1000-8000-00805f9b34fb'
const FFF3_UUID     = '0000fff3-0000-1000-8000-00805f9b34fb'

let _device       = null
let _fff2         = null
let _fff3         = null
let _seq          = 0
let _modeSet      = false
let _writeChain   = Promise.resolve()
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

/** [0x68, LEN, CMD, ...data, XOR_CRC] where LEN = bytes after LEN (cmd+data+crc) */
function _frameAL(cmd, data) {
  const lenByte = 1 + data.length + 1
  const frame = [0x68, lenByte, cmd, ...data]
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
  console.log('[fluval] connected — FFF1/FFF3 subscribed')

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

  const clamp = v => Math.max(0, Math.min(100, Math.round(v)))
  const to255  = v => Math.round(clamp(v) * 2.55)
  const to1000 = v => clamp(v) * 10

  if (!_modeSet) {
    _enqueue(_fff2, _frameA(0x02, [0x00]),  'FFF2 mode:A')
    _enqueue(_fff2, _frameAL(0x02, [0x00]), 'FFF2 mode:AL')
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

  _enqueue(_fff2, _frameA(0x04, [r8, g8, b8, w8]), 'FFF2 A-8bit')
  _enqueue(_fff2, _frameAL(0x04, [r8, g8, b8, w8]), 'FFF2 AL-8bit')
  _enqueue(_fff2, _frameA(0x04, data16),             'FFF2 A-16bit')
  _enqueue(_fff2, _frameB(0x11, 0x02, [r8, g8, b8, w8]), 'FFF2 B')
}

export function disconnect() {
  clearTimeout(_debounceTimer)
  if (_device && _device.gatt.connected) _device.gatt.disconnect()
  _device = _fff2 = _fff3 = null
  _modeSet = false
}
