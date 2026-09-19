import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useMaintenanceStore = defineStore('maintenance', () => {
  const tasks = ref([])

  async function fetchTasks() {
    const r = await axios.get('/api/maintenance')
    tasks.value = r.data
  }

  async function startTask(taskId, affectsEntity = null) {
    await axios.post(`/api/maintenance/${taskId}/start`, { affects_entity: affectsEntity })
    await fetchTasks()
  }

  async function completeTask(taskId, partsReplaced = [], notes = null) {
    await axios.post(`/api/maintenance/${taskId}/complete`, {
      parts_replaced: partsReplaced,
      notes,
    })
    await fetchTasks()
  }

  // Defers the on-screen due-reminder but keeps the hourly Telegram nudge
  // going (mirrors the water-test reminders' snooze) until the task is
  // actually completed, which clears the snooze server-side.
  async function snoozeTask(taskId) {
    await axios.post(`/api/maintenance/${taskId}/snooze`)
    await fetchTasks()
  }

  return { tasks, fetchTasks, startTask, completeTask, snoozeTask }
})
