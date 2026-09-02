import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCalendarStore = defineStore('calendar', () => {
  const monthData = ref({})
  const currentMonth = ref({ year: new Date().getFullYear(), month: new Date().getMonth() + 1 })
  const todayTasks = ref([])

  async function fetchMonth(year, month) {
    const key = `${year}-${month}`
    const r = await axios.get(`/api/calendar/month/${year}/${month}`)
    monthData.value[key] = r.data
    currentMonth.value = { year, month }
  }

  async function fetchToday(tankId = 1) {
    const r = await axios.get('/api/calendar/today', { params: { tank_id: tankId } })
    todayTasks.value = r.data.tasks
  }

  async function toggleComplete(taskId, date) {
    const r = await axios.post('/api/calendar/complete', { task_id: taskId, date })
    const [y, m] = date.split('-').map(Number)
    const key = `${y}-${m}`
    const data = monthData.value[key]
    if (data) {
      const day = data.days.find(d => d.date === date)
      if (day) {
        const task = day.tasks.find(t => t.id === taskId)
        if (task) {
          task.completed = r.data.completed
          task.completed_at = r.data.completed ? new Date().toISOString() : null
        }
      }
    }
    // also update todayTasks
    const todayTask = todayTasks.value.find(t => t.id === taskId && t.date === date)
    if (todayTask) todayTask.completed = r.data.completed
    return r.data.completed
  }

  async function createTask(data) {
    await axios.post('/api/calendar/tasks', data)
    await fetchToday(data.tank_id ?? 1)
    await refetchCurrent()
  }

  async function updateTask(taskId, data) {
    await axios.put(`/api/calendar/tasks/${taskId}`, data)
    await fetchToday(data.tank_id ?? 1)
    await refetchCurrent()
  }

  async function deleteTask(taskId, tankId = 1) {
    await axios.delete(`/api/calendar/tasks/${taskId}`)
    await fetchToday(tankId)
    await refetchCurrent()
  }

  async function refetchCurrent() {
    await fetchMonth(currentMonth.value.year, currentMonth.value.month)
  }

  return {
    monthData, currentMonth, todayTasks,
    fetchMonth, fetchToday, refetchCurrent,
    toggleComplete, createTask, updateTask, deleteTask,
  }
})
