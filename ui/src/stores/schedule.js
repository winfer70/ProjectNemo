import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useScheduleStore = defineStore('schedule', () => {
  const feedings = ref([])
  const feedingHistory = ref([])
  const dosingTasks = ref([])
  const feedStatus = ref({ paused: false, resume_in_secs: null, paused_entities: [] })
  let statusPollInterval = null

  async function fetchFeedings() {
    const r = await axios.get('/api/schedule/feedings')
    feedings.value = r.data
  }

  async function fetchHistory() {
    const r = await axios.get('/api/schedule/feedings/history')
    feedingHistory.value = r.data
  }

  async function fetchDosing() {
    const r = await axios.get('/api/dosing')
    dosingTasks.value = r.data
  }

  async function pollFeedStatus() {
    const r = await axios.get('/api/actions/feed-status')
    feedStatus.value = r.data
    if (!r.data.paused && statusPollInterval) {
      clearInterval(statusPollInterval)
      statusPollInterval = null
    }
  }

  function startStatusPolling() {
    if (statusPollInterval) clearInterval(statusPollInterval)
    statusPollInterval = setInterval(pollFeedStatus, 5000)
  }

  async function feedNow() {
    await axios.post('/api/actions/feed-now')
    feedStatus.value = { paused: true, resume_in_secs: 180, paused_entities: [] }
    startStatusPolling()
    await fetchHistory()
  }

  async function cancelFeed() {
    await axios.post('/api/actions/cancel-feed')
    feedStatus.value = { paused: false, resume_in_secs: null, paused_entities: [] }
    if (statusPollInterval) {
      clearInterval(statusPollInterval)
      statusPollInterval = null
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
    feedings, feedingHistory, dosingTasks, feedStatus,
    fetchFeedings, fetchHistory, fetchDosing, pollFeedStatus,
    feedNow, cancelFeed, completeDose, restockSupply,
    updateDosingTask, createDosingTask, startStatusPolling,
  }
})
