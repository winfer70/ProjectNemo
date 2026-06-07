import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import * as bleService from '../services/bleService'

export const useSensorsStore = defineStore('sensors', () => {
  const current = ref({ temperature: null, ph: null, tds: null, orp: null })
  const devices = ref([])
  const supplyWarnings = ref([])
  const wsConnection = ref(null)
  const bleConnected = ref(false)
  let ws = null

  async function fetchCurrent() {
    const r = await axios.get('/api/sensors/current')
    current.value = r.data
  }

  async function fetchDevices() {
    const r = await axios.get('/api/devices')
    devices.value = r.data
  }

  async function fetchSupplies() {
    const r = await axios.get('/api/supplies')
    supplyWarnings.value = r.data.filter(s => s.low)
  }

  async function toggleDevice(entityId) {
    await axios.post(`/api/devices/${encodeURIComponent(entityId)}/toggle`)
    await fetchDevices()
  }

  async function setFluvalChannels(r, g, b, w, ch5 = 0) {
    await axios.put('/api/devices/fluval/channels', { r, g, b, w, ch5 })
  }

  function connectWs() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    ws = new WebSocket(`${proto}://${location.host}/ws/live`)
    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data)
      if (data.type === 'live') {
        current.value = data.sensors
        devices.value = data.devices
      } else if (data.type === 'invalidate') {
        window.dispatchEvent(new CustomEvent('nemo:invalidate', { detail: { domain: data.domain } }))
      }
    }
    ws.onclose = () => setTimeout(connectWs, 5000)
  }

  function connectWS() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    const socket = new WebSocket(`${proto}://${location.hostname}:8000/ws/ble`)
    wsConnection.value = socket
    socket.onmessage = async (evt) => {
      try {
        const data = JSON.parse(evt.data)
        if (data.type === 'fluval_channels') {
          await bleService.setChannels(data.r, data.g, data.b, data.w, data.ch5 ?? 0)
        }
      } catch (err) {
        // BLE may not be connected yet — ignore silently so the WS stays open.
        console.warn('[nemo] BLE setChannels failed:', err)
      }
    }
    socket.onclose = () => {
      wsConnection.value = null
      setTimeout(connectWS, 3000)
    }
  }

  function disconnectWs() {
    if (ws) ws.close()
  }

  // Auto-start the BLE command WebSocket and reset bleConnected on GATT drop.
  connectWS()
  window.addEventListener('ble:disconnected', () => { bleConnected.value = false })

  return {
    current, devices, supplyWarnings, wsConnection, bleConnected,
    fetchCurrent, fetchDevices, fetchSupplies, toggleDevice, setFluvalChannels,
    connectWs, disconnectWs, connectWS,
  }
})
