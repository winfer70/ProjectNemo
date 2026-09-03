/**
 * Pinia store for water test UI — calls backend routers/water_tests.py via axios.
 *
 * Manages parameters, sessions, and trends state. Provides fetchParameters(),
 * fetchLatest(), fetchSessions(), createSession(), fetchTrend(), and isCycled()
 * computed check. All API calls proxied to nemo-api:8000 via vite.config.js.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useWaterTestsStore = defineStore('waterTests', () => {
  const parameters = ref([])
  const sessions = ref([])
  const latestSession = ref(null)
  const currentByTank = ref({})

  async function fetchParameters() {
    const r = await axios.get('/api/water-tests/parameters')
    parameters.value = r.data
  }

  async function fetchLatest() {
    const r = await axios.get('/api/water-tests/sessions/latest')
    latestSession.value = r.data
  }

  async function fetchCurrent(tankId = 1) {
    const r = await axios.get('/api/water-tests/current', { params: { tank_id: tankId } })
    currentByTank.value = { ...currentByTank.value, [Number(tankId)]: r.data?.readings || [] }
    return r.data
  }

  async function fetchSessions(limit = 20) {
    const r = await axios.get(`/api/water-tests/sessions?limit=${limit}`)
    sessions.value = r.data
  }

  async function createSession(tested_at, notes, readings, scan_cache_id = null) {
    const r = await axios.post('/api/water-tests/sessions', { tested_at, notes, readings, scan_cache_id })
    await fetchLatest()
    await fetchSessions()
    await fetchCurrent(r.data?.tank_id || 1)
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

  return {
    parameters, sessions, latestSession, currentByTank,
    fetchParameters, fetchLatest, fetchCurrent, fetchSessions, createSession, fetchTrend, isCycled,
  }
})
