import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useScheduleStore = defineStore('schedule', () => {
  const feedings = ref([])
  const feedingHistory = ref([])
  const dosingTasks = ref([])
  const filterPausedSecs = ref(0)
  let pauseTimer = null

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

  async function feedNow() {
    await axios.post('/api/actions/feed-now')
    filterPausedSecs.value = 600
    pauseTimer = setInterval(() => {
      filterPausedSecs.value--
      if (filterPausedSecs.value <= 0) clearInterval(pauseTimer)
    }, 1000)
    await fetchHistory()
  }

  async function completeDose(taskId) {
    await axios.post(`/api/dosing/${taskId}/complete`, {})
    await fetchDosing()
  }

  async function restockSupply(supplyId, newAmount) {
    await axios.post(`/api/supplies/${supplyId}/restock`, { new_amount: newAmount })
    await fetchDosing()
  }

  return { feedings, feedingHistory, dosingTasks, filterPausedSecs, fetchFeedings, fetchHistory, fetchDosing, feedNow, completeDose, restockSupply }
})
