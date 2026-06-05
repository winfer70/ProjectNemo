import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useWaterTestsStore = defineStore('waterTests', () => {
  const parameters = ref([])
  const sessions = ref([])
  const latestSession = ref(null)

  async function fetchParameters() {
    const r = await axios.get('/api/water-tests/parameters')
    parameters.value = r.data
  }

  async function fetchLatest() {
    const r = await axios.get('/api/water-tests/sessions/latest')
    latestSession.value = r.data
  }

  async function fetchSessions(limit = 20) {
    const r = await axios.get(`/api/water-tests/sessions?limit=${limit}`)
    sessions.value = r.data
  }

  async function createSession(tested_at, notes, readings, scan_cache_id = null) {
    const r = await axios.post('/api/water-tests/sessions', { tested_at, notes, readings, scan_cache_id })
    await fetchLatest()
    await fetchSessions()
    return r.data
  }

  async function fetchTrend(paramKey, n = 8) {
    const r = await axios.get(`/api/water-tests/trends/${paramKey}?n=${n}`)
    return r.data
  }

  // Check if tank is cycled: NH3=0 and NO2=0 for 3 consecutive sessions
  const isCycled = () => {
    if (sessions.value.length < 3) return false
    return sessions.value.slice(0, 3).every(s => {
      const nh3 = s.readings.find(r => r.parameter_key === 'ammonia')
      const no2 = s.readings.find(r => r.parameter_key === 'nitrite')
      return nh3?.value === 0 && no2?.value === 0
    })
  }

  return { parameters, sessions, latestSession, fetchParameters, fetchLatest, fetchSessions, createSession, fetchTrend, isCycled }
})
