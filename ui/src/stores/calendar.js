import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCalendarStore = defineStore('calendar', () => {
  const monthData = ref({}) // key: `${tankId}-${year}-${month}`
  const currentMonthByTank = ref({ 1: { year: new Date().getFullYear(), month: new Date().getMonth() + 1 } })
  const todayTasksByTank = ref({}) // { [tankId]: task[] }

  async function fetchMonth(year, month, tankId = 1) {
    const key = `${tankId}-${year}-${month}`
    const r = await axios.get(`/api/calendar/month/${year}/${month}`, { params: { tank_id: tankId } })
    monthData.value[key] = r.data
    currentMonthByTank.value = { ...currentMonthByTank.value, [tankId]: { year, month } }
  }

  async function fetchToday(tankId = 1) {
    const r = await axios.get('/api/calendar/today', { params: { tank_id: tankId } })
    todayTasksByTank.value = { ...todayTasksByTank.value, [tankId]: r.data.tasks }
  }

  async function toggleComplete(taskId, date) {
    const r = await axios.post('/api/calendar/complete', { task_id: taskId, date })
    const [y, m] = date.split('-').map(Number)
    // task_id alone doesn't say which tank's cache to update - check all
    // cached months for this year/month across tanks.
    for (const [key, data] of Object.entries(monthData.value)) {
      if (!key.endsWith(`-${y}-${m}`)) continue
      const day = data.days?.find(d => d.date === date)
      const task = day?.tasks.find(t => t.id === taskId)
      if (task) {
        task.completed = r.data.completed
        task.completed_at = r.data.completed ? new Date().toISOString() : null
      }
    }
    // also update whichever tank's today list has this task
    for (const tasks of Object.values(todayTasksByTank.value)) {
      const todayTask = tasks.find(t => t.id === taskId && t.date === date)
      if (todayTask) todayTask.completed = r.data.completed
    }
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
    await Promise.all(
      Object.entries(currentMonthByTank.value).map(([tid, { year, month }]) => fetchMonth(year, month, Number(tid)))
    )
  }

  return {
    monthData, currentMonthByTank, todayTasksByTank,
    fetchMonth, fetchToday, refetchCurrent,
    toggleComplete, createTask, updateTask, deleteTask,
  }
})

