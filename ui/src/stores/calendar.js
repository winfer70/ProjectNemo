/**
 * Calendar store — manages monthly task schedule and completion state.
 * Fetches task/completion data from the API and provides toggle actions.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCalendarStore = defineStore('calendar', () => {
  // monthData keyed by "YYYY-M" → { year, month, days: [...] }
  const monthData = ref({})

  /**
   * Fetch all days for a given month from the API.
   * @param {number} year
   * @param {number} month  1-based
   */
  async function fetchMonth(year, month) {
    const key = `${year}-${month}`
    const r = await axios.get(`/api/calendar/month/${year}/${month}`)
    monthData.value[key] = r.data
  }

  /**
   * Toggle completion of a task on a date.
   * Updates local state optimistically after API confirms.
   * @param {number} taskId
   * @param {string} date  YYYY-MM-DD
   */
  async function toggleComplete(taskId, date) {
    const r = await axios.post('/api/calendar/complete', { task_id: taskId, date })
    const [y, m] = date.split('-').map(Number)
    const key = `${y}-${m}`
    const data = monthData.value[key]
    if (!data) return
    const day = data.days.find(d => d.date === date)
    if (!day) return
    const task = day.tasks.find(t => t.id === taskId)
    if (!task) return
    task.completed = r.data.completed
    task.completed_at = r.data.completed ? new Date().toISOString() : null
  }

  return { monthData, fetchMonth, toggleComplete }
})
