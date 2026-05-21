<template>
  <!-- Capture all interactions to reset the inactivity timer -->
  <div class="cal-container" @click="resetTimer" @touchstart.passive="resetTimer">

    <!-- Month navigation header -->
    <div class="cal-header">
      <button class="cal-nav-btn" @click.stop="prevMonth">&#8249;</button>
      <span class="cal-month-title">{{ monthName }} {{ year }}</span>
      <button class="cal-nav-btn" @click.stop="nextMonth">&#8250;</button>
    </div>

    <!-- Weekday column headers (Mon–Sun) -->
    <div class="cal-grid">
      <div class="cal-weekday" v-for="wd in weekdayLabels" :key="wd">{{ wd }}</div>

      <!-- Calendar day cells -->
      <div
        v-for="cell in calendarCells"
        :key="cell.key"
        class="cal-day"
        :class="{
          'other-month': !cell.currentMonth,
          'today': cell.isToday,
          'selected': selectedDate === cell.dateStr && cell.currentMonth,
        }"
        @click.stop="cell.currentMonth && selectDay(cell)"
      >
        <div class="cal-day-header">
          <span class="cal-day-num">{{ cell.day }}</span>
          <span v-if="cell.tasks.length && cell.tasks.every(t => t.completed)" class="cal-all-done">&#10003;</span>
        </div>
        <div class="cal-day-rows">
          <div
            v-for="task in cell.tasks"
            :key="task.id"
            class="cal-day-row"
            :class="{ done: task.completed }"
          >
            <span class="cal-row-bar" :style="{ background: task.color }"></span>
            <span class="cal-row-text">{{ locale === 'pl' ? task.name_pl : task.name }}</span>
            <span v-if="task.amount" class="cal-row-amt">{{ task.amount }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Day detail bottom-sheet (Teleported to body to avoid overflow clipping) -->
    <Teleport to="body">
      <div v-if="selectedDate && selectedDayData" class="modal-overlay" @click.self="closePanel">
        <div class="modal-sheet">
          <div class="modal-title">{{ formatSelectedDate }}</div>

          <div v-if="!selectedDayData.tasks.length" class="cal-no-tasks">
            {{ $t('calendar.noTasks') }}
          </div>

          <ul v-else class="cal-detail-list">
            <li v-for="task in selectedDayData.tasks" :key="task.id" class="cal-task-item">
              <span class="cal-task-color" :style="{ background: task.color }" />
              <div class="cal-task-info">
                <div class="cal-task-name">{{ locale === 'pl' ? task.name_pl : task.name }}</div>
                <div v-if="task.amount" class="cal-task-amount">{{ task.amount }}</div>
              </div>
              <button
                class="cal-task-done-btn"
                :class="{ done: task.completed }"
                @click.stop="toggleTask(task)"
                :title="task.completed ? $t('calendar.markUndone') : $t('calendar.markDone')"
              >
                {{ task.completed ? '✓' : '○' }}
              </button>
            </li>
          </ul>

          <div class="modal-footer">
            <button class="btn btn-secondary btn-full" @click="closePanel">
              {{ $t('common.close') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCalendarStore } from '../stores/calendar.js'

const { t, tm, locale } = useI18n()
const calStore = useCalendarStore()

// ── Current month state ───────────────────────────────────────
const today = new Date()
const year = ref(today.getFullYear())
const month = ref(today.getMonth() + 1)   // 1-based

// ── Selected day ──────────────────────────────────────────────
const selectedDate = ref(null)   // "YYYY-MM-DD" or null

// ── 5-minute inactivity timer — closes day panel ──────────────
const INACTIVITY_MS = 5 * 60 * 1000
let inactivityTimer = null

function resetTimer() {
  if (!selectedDate.value) return
  clearTimeout(inactivityTimer)
  inactivityTimer = setTimeout(closePanel, INACTIVITY_MS)
}

function closePanel() {
  selectedDate.value = null
  clearTimeout(inactivityTimer)
}

onUnmounted(() => clearTimeout(inactivityTimer))

// ── Fetch month data when year/month changes ──────────────────
watch([year, month], () => calStore.fetchMonth(year.value, month.value), { immediate: true })

function prevMonth() {
  if (month.value === 1) { month.value = 12; year.value-- }
  else month.value--
}
function nextMonth() {
  if (month.value === 12) { month.value = 1; year.value++ }
  else month.value++
}

// ── i18n helpers ──────────────────────────────────────────────
const weekdayLabels = computed(() => {
  // tm() returns the raw translation value (array) without coercing to string
  const labels = tm('calendar.weekdays')
  return Array.isArray(labels) ? labels : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
})

const monthName = computed(() => {
  const months = tm('calendar.months')
  return Array.isArray(months) ? months[month.value - 1] : ''
})

// ── Calendar grid cells ───────────────────────────────────────
const calendarCells = computed(() => {
  const data = calStore.monthData[`${year.value}-${month.value}`] || { days: [] }
  const dayMap = {}
  for (const d of (data.days ?? [])) dayMap[d.date] = d

  // First day of month: getDay() returns 0=Sun — convert to Mon-first (0=Mon)
  const firstDay = new Date(year.value, month.value - 1, 1)
  const startOffset = (firstDay.getDay() + 6) % 7
  const daysInMonth = new Date(year.value, month.value, 0).getDate()
  const prevMonthDays = new Date(year.value, month.value - 1, 0).getDate()
  const todayStr = today.toISOString().slice(0, 10)

  const cells = []

  // Leading days from previous month (greyed out)
  for (let i = startOffset - 1; i >= 0; i--) {
    const d = prevMonthDays - i
    cells.push({ key: `prev-${d}`, day: d, currentMonth: false, isToday: false, dateStr: null, tasks: [] })
  }

  // Current month days
  for (let d = 1; d <= daysInMonth; d++) {
    const mm = String(month.value).padStart(2, '0')
    const dd = String(d).padStart(2, '0')
    const dateStr = `${year.value}-${mm}-${dd}`
    const dayData = dayMap[dateStr] || { tasks: [] }
    cells.push({
      key: dateStr,
      day: d,
      currentMonth: true,
      isToday: dateStr === todayStr,
      dateStr,
      tasks: dayData.tasks || [],
    })
  }

  // Trailing days to complete the last week row
  const remaining = (7 - (cells.length % 7)) % 7
  for (let d = 1; d <= remaining; d++) {
    cells.push({ key: `next-${d}`, day: d, currentMonth: false, isToday: false, dateStr: null, tasks: [] })
  }

  return cells
})

// ── Selected day data ─────────────────────────────────────────
const selectedDayData = computed(() => {
  if (!selectedDate.value) return null
  const data = calStore.monthData[`${year.value}-${month.value}`] || { days: [] }
  return (data.days ?? []).find(d => d.date === selectedDate.value) || { tasks: [] }
})

// Format date for panel title
const formatSelectedDate = computed(() => {
  if (!selectedDate.value) return ''
  const d = new Date(selectedDate.value + 'T00:00:00')
  return d.toLocaleDateString(locale.value === 'pl' ? 'pl-PL' : 'en-IE', {
    weekday: 'long', day: 'numeric', month: 'long',
  })
})

function selectDay(cell) {
  if (selectedDate.value === cell.dateStr) {
    closePanel()
  } else {
    selectedDate.value = cell.dateStr
    resetTimer()
  }
}

async function toggleTask(task) {
  await calStore.toggleComplete(task.id, selectedDate.value)
  resetTimer()
}
</script>
