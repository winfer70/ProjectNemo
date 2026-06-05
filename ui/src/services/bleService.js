/**
 * Fluval Roma/Shaker 2.0 — Web Bluetooth singleton service.
 *
 * PROTOCOL CONFIRMED via HCI snoop (btsnoop_hci.log from Fluval Connect app):
 *
 *   Service: 0xFFF0
 *   FFF1 (handle 0x0010): NOTIFY — device echoes all commands + sends state
 *   FFF2 (handle 0x0013): WRITE WITHOUT RESPONSE + WRITE — host sends commands here
 *   FFF1 CCCD (handle 0x0011): subscribe with WriteWithResponse → enables FFF1 notify
 *
 *   Frame format (all use Write WITHOUT Response to FFF2):
 *     cd 1a MM DD HH mm ss 00   — datetime sync, sent once at connect
 *     d0 ff                     — query current state
 *     d1 a1 CMD VALUE           — single-byte command
 *       CMD 0x01: mode  0x00=auto/schedule, 0x02=manual
 *       CMD 0x02: overall brightness 0–255
 *       CMD 0x03: channel R, 0–255
 *       CMD 0x04: channel G, 0–255
 *       CMD 0x05: channel B, 0–255
 *       CMD 0x06: channel W, 0–255
 *     d1 a2 CMD V1 V2 ... 00    — multi-byte (schedule entries, not used here)
 *
 *   Device echoes every accepted command as FFF1 notify: d2 a1 CMD VALUE
 *   Device sends current state as: d2 af 00 0f 01 vv 02 vv 03 vv vv 04 vv vv 05 vv vv 06 vv vv
 *
 * Write queue serializes sends. setChannels debounced 60ms for slider smoothness.
 */

const SERVICE_UUID = '0000fff0-0000-1000-8000-00805f9b34fb'
const FFF1_UUID    = '0000fff1-0000-1000-8000-00805f9b34fb'
const FFF2_UUID    = '0000fff2-0000-1000-8000-00805f9b34fb'

let _device        = null
let _fff2          = null
let _writeChain    = Promise.resolve()
let _debounceTimer = null
let _modeSet       = false

// ---------------------------------------------------------------------------
// Frame builders
// ---------------------------------------------------------------------------

function _cmd1(cmd, val) {
  return new Uint8Array([0xd1, 0xa1, cmd, val])
}

// ---------------------------------------------------------------------------
// Serialized write queue — Write Without Response, rate-limited by chaining
// ---------------------------------------------------------------------------

function _enqueue(pkt, label) {
  _writeChain = _writeChain.then(async () => {
    const hex = Array.from(pkt).map(b => b.toString(16).padStart(2, '0')).join(' ')
    console.log(`[fluval] ${label} → ${hex}`)
    try {
      if (_fff2.writeValueWithoutResponse) {
        await _fff2.writeValueWithoutResponse(pkt)
      } else {
        await _fff2.writeValue(pkt)  // older Web BT API fallback
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

  // FFF1 subscriptions receive echo of every command + state notifications
  const fff1 = await service.getCharacteristic(FFF1_UUID)
  await fff1.startNotifications()
  fff1.addEventListener('characteristicvaluechanged', (e) => {
    const bytes = Array.from(new Uint8Array(e.target.value.buffer))
    console.log('[fluval] FFF1 notify:', bytes.map(b => b.toString(16).padStart(2, '0')).join(' '))
  })

  _fff2       = await service.getCharacteristic(FFF2_UUID)
  _device     = device
  _modeSet    = false
  _writeChain = Promise.resolve()
  console.log('[fluval] connected')

  // Datetime sync (sets device RTC for schedule; required before commands)
  const now = new Date()
  const sync = new Uint8Array([
    0xcd, 0x1a,
    now.getMonth() + 1,
    now.getDate(),
    now.getHours(),
    now.getMinutes(),
    now.getSeconds(),
    0x00,  // checksum — real value unknown from log, 0x00 as placeholder
  ])
  _enqueue(sync, 'sync')

  // Query current state — FFF1 notify will show channel values
  _enqueue(new Uint8Array([0xd0, 0xff]), 'query')

  device.addEventListener('gattserverdisconnected', () => {
    _device = _fff2 = null
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
  const to255 = v => Math.round(clamp(v) * 2.55)

  if (!_modeSet) {
    _enqueue(_cmd1(0x01, 0x02), 'mode-manual')
    _modeSet = true
  }

  _enqueue(_cmd1(0x03, to255(r)), 'ch-R')
  _enqueue(_cmd1(0x04, to255(g)), 'ch-G')
  _enqueue(_cmd1(0x05, to255(b)), 'ch-B')
  _enqueue(_cmd1(0x06, to255(w)), 'ch-W')
}

export function disconnect() {
  clearTimeout(_debounceTimer)
  if (_device && _device.gatt.connected) _device.gatt.disconnect()
  _device = _fff2 = null
  _modeSet = false
}
