import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useSensorsStore = defineStore('sensors', () => {
  const current = ref({ temperature: null, ph: null, tds: null, orp: null })
  const devices = ref([])
  const supplyWarnings = ref([])
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

  function disconnectWs() {
    if (ws) ws.close()
  }

  return { current, devices, supplyWarnings, fetchCurrent, fetchDevices, fetchSupplies, toggleDevice, setFluvalChannels, connectWs, disconnectWs }
})
