import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useScheduleStore = defineStore('schedule', () => {
  const feedings = ref([])
  const feedingHistory = ref([])
  const dosingTasks = ref([])
  const feedStatusByTank = ref({}) // { [tankId]: { paused, resume_in_secs, paused_entities } }
  const statusPollIntervals = {} // tankId -> interval handle, not reactive

  const EMPTY_STATUS = { paused: false, resume_in_secs: null, paused_entities: [] }

  function feedStatusFor(tankId) {
    return feedStatusByTank.value[tankId] ?? EMPTY_STATUS
  }

  async function fetchFeedings(tankId = 1) {
    const r = await axios.get('/api/schedule/feedings', { params: { tank_id: tankId } })
    feedings.value = r.data
  }

  async function fetchHistory(tankId = 1) {
    const r = await axios.get('/api/schedule/feedings/history', { params: { tank_id: tankId } })
    feedingHistory.value = r.data
  }

  async function fetchDosing() {
    const r = await axios.get('/api/dosing')
    dosingTasks.value = r.data
  }

  async function pollFeedStatus(tankId = 1) {
    const r = await axios.get('/api/actions/feed-status', { params: { tank_id: tankId } })
    feedStatusByTank.value = { ...feedStatusByTank.value, [tankId]: r.data }
    if (!r.data.paused && statusPollIntervals[tankId]) {
      clearInterval(statusPollIntervals[tankId])
      delete statusPollIntervals[tankId]
    }
  }

  function startStatusPolling(tankId = 1) {
    if (statusPollIntervals[tankId]) clearInterval(statusPollIntervals[tankId])
    statusPollIntervals[tankId] = setInterval(() => pollFeedStatus(tankId), 5000)
  }

  async function feedNow(tankId = 1) {
    await axios.post('/api/actions/feed-now', null, { params: { tank_id: tankId } })
    feedStatusByTank.value = { ...feedStatusByTank.value, [tankId]: { paused: true, resume_in_secs: 180, paused_entities: [] } }
    startStatusPolling(tankId)
    await fetchHistory(tankId)
  }

  async function cancelFeed(tankId = 1) {
    await axios.post('/api/actions/cancel-feed', null, { params: { tank_id: tankId } })
    feedStatusByTank.value = { ...feedStatusByTank.value, [tankId]: { ...EMPTY_STATUS } }
    if (statusPollIntervals[tankId]) {
      clearInterval(statusPollIntervals[tankId])
      delete statusPollIntervals[tankId]
    }
  }

  async function completeDose(taskId) {
    await axios.post(`/api/dosing/${taskId}/complete`, {})
    await fetchDosing()
  }

  async function restockSupply(supplyId, newAmount) {
    await axios.post(`/api/dosing/supplies/${supplyId}/restock`, { new_amount: newAmount })
    await fetchDosing()
  }

  async function updateDosingTask(taskId, data) {
    await axios.put(`/api/dosing/${taskId}`, data)
    await fetchDosing()
  }

  async function createDosingTask(data) {
    await axios.post('/api/dosing', data)
    await fetchDosing()
  }

  return {
    feedings, feedingHistory, dosingTasks, feedStatusByTank, feedStatusFor,
    fetchFeedings, fetchHistory, fetchDosing, pollFeedStatus,
    feedNow, cancelFeed, completeDose, restockSupply,
    updateDosingTask, createDosingTask, startStatusPolling,
  }
})
