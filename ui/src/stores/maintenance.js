import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useMaintenanceStore = defineStore('maintenance', () => {
  const tasks = ref([])

  async function fetchTasks() {
    const r = await axios.get('/api/maintenance')
    tasks.value = r.data
  }

  async function completeTask(taskId, partsReplaced, notes) {
    await axios.post(`/api/maintenance/${taskId}/complete`, { parts_replaced: partsReplaced, notes })
    await fetchTasks()
  }

  return { tasks, fetchTasks, completeTask }
})
