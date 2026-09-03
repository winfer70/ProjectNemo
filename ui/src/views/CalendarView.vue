<template>
  <div :class="{ row2: tankIds.length > 1 }">
  <div v-for="tid in tankIds" :key="'calcol-' + tid" style="display:flex;flex-direction:column;gap:var(--gap);min-width:0">

  <!-- ── Calendar grid ──────────────────────────────────── -->
  <div class="tile" v-resizable="'calendar.grid.' + tid">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/>
        </svg>
        KALENDARZ
        <span v-if="tankIds.length > 1" class="muted" style="font-size:11px;font-weight:600;text-transform:none;margin-left:4px">· {{ tankName(tid) }}</span>
      </h2>
      <button class="btn btn-sm btn-accent" @click="openNew(tid)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14"/><path d="M5 12h14"/>
        </svg>
        {{ locale === 'pl' ? 'Zadanie' : 'Task' }}
      </button>
    </div>
    <hr class="divider">
    <div class="tile-body" style="padding-top:12px">
      <!-- Month navigation -->
      <div class="spread" style="margin-bottom:12px">
        <button class="btn icon-btn btn-ghost" @click="prevMonth(tid)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 5l-7 7 7 7"/>
          </svg>
        </button>
        <span style="font-weight:700;font-size:15px">{{ monthNameFor(tid) }} {{ calState[tid].viewYear }}</span>
        <button class="btn icon-btn btn-ghost" @click="nextMonth(tid)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>

      <!-- Day-of-week headers -->
      <div class="cal-grid" style="margin-bottom:4px">
        <div class="cal-dow" v-for="d in dows" :key="d">{{ d }}</div>
      </div>

      <!-- Calendar cells -->
      <div class="cal-grid">
        <template v-for="(cell, i) in calCellsFor(tid)" :key="i">
          <div v-if="cell === null" />
          <div v-else
            :class="['cal-cell', isToday(tid, cell) ? 'today' : '', cell === calState[tid].selectedDay ? 'sel' : '']"
            @click="calState[tid].selectedDay = cell"
          >
            {{ cell }}
            <span v-if="taskDaysFor(tid).has(cell)" class="cdot" />
          </div>
        </template>
      </div>
    </div>
  </div>

  <!-- ── Selected day tasks ─────────────────────────────── -->
  <div class="tile" v-resizable="'calendar.daytasks.' + tid">
    <div class="tile-hd">
      <h2>{{ formattedDayFor(tid) }}</h2>
    </div>
    <hr class="divider">
    <div class="tile-body" style="padding-top:6px">

      <!-- Empty state -->
      <div v-if="!dayTasksFor(tid).length" class="empty">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/>
        </svg>
        <span>{{ locale === 'pl' ? 'Wolny dzień' : 'Free day' }}</span>
      </div>

      <!-- Task rows with swipe-to-complete -->
      <template v-else>
        <div v-for="(task, i) in dayTasksFor(tid)" :key="task.id" style="position:relative;overflow:hidden">
          <!-- Swipe reveal background -->
          <div style="position:absolute;inset:0;display:flex;align-items:center;padding-left:16px;color:var(--success);background:var(--success-12)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 12.5l5 5 11-12"/>
            </svg>
          </div>
          <!-- Sliding content -->
          <div
            :style="{
              position: 'relative',
              background: 'var(--surface)',
              transform: swipeDx[task.id] ? `translateX(${swipeDx[task.id]}px)` : undefined,
              transition: swipeActiveId === task.id ? 'none' : 'transform .2s'
            }"
            @mousedown="swipeBegin($event, task.id)"
            @mousemove="swipeMove($event, task.id)"
            @mouseup="swipeEnd(task, tid)"
            @mouseleave="swipeLeave(task, tid)"
            @touchstart.passive="swipeBegin($event, task.id)"
            @touchmove.passive="swipeMove($event, task.id)"
            @touchend="swipeEnd(task, tid)"
          >
            <div
              class="spread"
              :style="{ padding: '12px 2px', borderTop: i ? '1px solid var(--border)' : 'none' }"
            >
              <!-- Task label -->
              <div class="row" style="gap:9px;min-width:0;flex:1;overflow:hidden">
                <span :style="{ color: task.completed ? 'var(--success)' : 'var(--accent)', display: 'flex', flexShrink: 0 }">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <template v-if="task.completed">
                      <circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.6 2.6L16 9"/>
                    </template>
                    <template v-else>
                      <circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/>
                    </template>
                  </svg>
                </span>
                <span :style="{
                  textDecoration: task.completed ? 'line-through' : 'none',
                  color: task.completed ? 'var(--text-muted)' : 'var(--text)',
                  whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'
                }">
                  {{ locale === 'pl' && task.name_pl ? task.name_pl : (task.name_en || task.name) }}
                </span>
              </div>

              <!-- Confirm-delete state -->
              <div v-if="confirmDelId === task.id" class="row" style="gap:6px;flex-shrink:0">
                <span class="muted" style="font-size:12px">{{ locale === 'pl' ? 'Usuń?' : 'Delete?' }}</span>
                <button class="btn icon-btn btn-danger-o" @click.stop="doDelete(task.id, tid)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 12.5l5 5 11-12"/>
                  </svg>
                </button>
                <button class="btn icon-btn btn-ghost" @click.stop="confirmDelId = null">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
                  </svg>
                </button>
              </div>

              <!-- Normal action buttons -->
              <div v-else class="row" style="gap:5px;flex-shrink:0">
                <button :class="['btn', 'icon-btn', task.completed ? 'btn-success' : '']" @click.stop="toggleTask(task, tid)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 12.5l5 5 11-12"/>
                  </svg>
                </button>
                <button class="btn icon-btn btn-ghost" @click.stop="editModal = { task, day: calState[tid].selectedDay, tankId: tid }">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M14 6l4 4"/>
                  </svg>
                </button>
                <button class="btn icon-btn btn-ghost" @click.stop="confirmDelId = task.id">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 7h16"/><path d="M9 7V5h6v2"/><path d="M6 7l1 13h10l1-13"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Add task button -->
      <button class="btn btn-block btn-ghost" style="margin-top:12px" @click="openNew(tid)">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14"/><path d="M5 12h14"/>
        </svg>
        {{ locale === 'pl' ? 'Dodaj zadanie' : 'Add task' }}
      </button>
    </div>
  </div>

  </div>
  </div>

  <!-- ── CalEditModal (full-screen) ────────────────────────────── -->
  <Teleport to="body">
    <div
      v-if="editModal"
      class="backdrop"
      style="position:fixed;align-items:stretch;justify-content:center"
      @click.self="editModal = null"
    >
      <div class="modal full" @click.stop>
        <!-- Modal header -->
        <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
          <button class="btn icon-btn btn-ghost" @click="editModal = null">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">
            {{ editModal.task ? (locale === 'pl' ? 'Edytuj zadanie' : 'Edit task') : (locale === 'pl' ? 'Nowe zadanie' : 'New task') }}
            <span v-if="tankIds.length > 1" class="muted" style="font-weight:400;font-size:12px"> · {{ tankName(editModal.tankId) }}</span>
          </span>
          <button class="btn btn-sm btn-accent" @click="saveTask">
            {{ locale === 'pl' ? 'Zapisz' : 'Save' }}
          </button>
        </div>

        <!-- Modal body -->
        <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
          <div class="field">
            <label>{{ locale === 'pl' ? 'Nazwa (PL)' : 'Title (PL)' }}</label>
            <input class="input" v-model="formPl" autofocus placeholder="Wymiana wody…">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Nazwa (EN)' : 'Title (EN)' }}</label>
            <input class="input" v-model="formEn" placeholder="Water change…">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Data' : 'Date' }}</label>
            <input class="input" type="date" v-model="formDate">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Powtarzanie' : 'Repeat' }}</label>
            <div class="seg" style="flex-wrap:wrap">
              <button
                v-for="[k, lab] in repeatOptions"
                :key="k"
                :class="{ on: formRepeat === k }"
                @click="formRepeat = k"
              >{{ lab }}</button>
            </div>
            <div v-if="formRepeat === 'every_n_days'" style="margin-top:8px;display:flex;align-items:center;gap:8px">
              <span class="muted" style="font-size:13px">{{ locale === 'pl' ? 'Co' : 'Every' }}</span>
              <input class="input" type="number" v-model="formInterval" min="2" style="width:80px">
              <span class="muted" style="font-size:13px">{{ locale === 'pl' ? 'dni' : 'days' }}</span>
            </div>
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Notatki' : 'Notes' }}</label>
            <textarea class="input" rows="3" v-model="formNotes" style="resize:none"></textarea>
          </div>
          <!-- Delete existing task -->
          <button
            v-if="editModal.task?.id"
            class="btn btn-block btn-danger-o"
            style="margin-top:16px"
            @click="deleteTask"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 7h16"/><path d="M9 7V5h6v2"/><path d="M6 7l1 13h10l1-13"/>
            </svg>
            {{ locale === 'pl' ? 'Usuń zadanie' : 'Delete task' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useCalendarStore } from '../stores/calendar'
import { useTankSelectorStore } from '../stores/tankSelector'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { ref, reactive, computed, onMounted, watch } from 'vue'

const { locale } = useI18n()
const calendarStore = useCalendarStore()
const tankStore = useTankSelectorStore()
const { monthData } = storeToRefs(calendarStore)

const tankIds = computed(() => tankStore.tanks.map(t => t.id).sort((a, b) => a - b))
function tankName(tid) {
  return tankStore.tanks.find(t => t.id === tid)?.name ?? `Tank ${tid}`
}

// ── Per-tank date state - each column navigates its own month/day ──────────
const today = new Date()
const calState = reactive({})
function ensureTankState(tid) {
  if (!calState[tid]) {
    calState[tid] = { viewYear: today.getFullYear(), viewMonth: today.getMonth() + 1, selectedDay: today.getDate() }
  }
}
watch(tankIds, (ids) => ids.forEach(ensureTankState), { immediate: true })

const confirmDelId = ref(null)
const editModal = ref(null)  // null | { task, day, tankId }

// ── Swipe-to-complete state ───────────────────────────────────
const swipeDx = reactive({})
const swipeActiveId = ref(null)
let _swipeStartX = null

function swipeBegin(e, taskId) {
  swipeActiveId.value = taskId
  _swipeStartX = e.touches ? e.touches[0].clientX : e.clientX
}

function swipeMove(e, taskId) {
  if (swipeActiveId.value !== taskId) return
  const x = e.touches ? e.touches[0].clientX : e.clientX
  const d = x - _swipeStartX
  if (d > 0) swipeDx[taskId] = Math.min(d, 120)
}

function swipeEnd(task, tid) {
  if (swipeActiveId.value !== task.id) return
  if ((swipeDx[task.id] || 0) > 70 && !task.completed) {
    calendarStore.toggleComplete(task.id, dayDateStrFor(tid))
  }
  swipeDx[task.id] = 0
  swipeActiveId.value = null
  _swipeStartX = null
}

function swipeLeave(task, tid) {
  if (swipeActiveId.value === task.id) swipeEnd(task, tid)
}

// ── Month navigation (per tank) ────────────────────────────────
function prevMonth(tid) {
  const s = calState[tid]
  if (s.viewMonth === 1) { s.viewMonth = 12; s.viewYear-- }
  else s.viewMonth--
}

function nextMonth(tid) {
  const s = calState[tid]
  if (s.viewMonth === 12) { s.viewMonth = 1; s.viewYear++ }
  else s.viewMonth++
}

watch(() => tankIds.value.map(tid => [tid, calState[tid]?.viewYear, calState[tid]?.viewMonth]), (entries) => {
  for (const [tid, y, m] of entries) {
    if (y && m) calendarStore.fetchMonth(y, m, tid)
  }
}, { deep: true })

onMounted(() => {
  tankIds.value.forEach(tid => {
    ensureTankState(tid)
    calendarStore.fetchMonth(calState[tid].viewYear, calState[tid].viewMonth, tid)
  })
})

// ── Locale helpers ────────────────────────────────────────────
const PL_MONTHS = ['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień']
const EN_MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
const PL_DOWS = ['Pn','Wt','Śr','Cz','Pt','Sb','Nd']
const EN_DOWS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

function monthNameFor(tid) {
  const m = calState[tid]?.viewMonth ?? 1
  return locale.value === 'pl' ? PL_MONTHS[m - 1] : EN_MONTHS[m - 1]
}
const dows = computed(() => locale.value === 'pl' ? PL_DOWS : EN_DOWS)

// ── Calendar grid (per tank) ────────────────────────────────────
function calCellsFor(tid) {
  const s = calState[tid]
  if (!s) return []
  const first = new Date(s.viewYear, s.viewMonth - 1, 1)
  const offset = (first.getDay() + 6) % 7  // Monday-first
  const daysInMonth = new Date(s.viewYear, s.viewMonth, 0).getDate()
  const cells = []
  for (let i = 0; i < offset; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)
  return cells
}

function isToday(tid, day) {
  const s = calState[tid]
  return (
    day === today.getDate() &&
    s.viewMonth === today.getMonth() + 1 &&
    s.viewYear === today.getFullYear()
  )
}

// ── Days that have tasks (for dots) ──────────────────────────
function taskDaysFor(tid) {
  const s = calState[tid]
  const key = `${tid}-${s.viewYear}-${s.viewMonth}`
  const data = monthData.value[key]
  const set = new Set()
  if (!data?.days) return set
  for (const d of data.days) {
    if (d.tasks?.length > 0) set.add(parseInt(d.date.slice(8), 10))
  }
  return set
}

// ── Selected day (per tank) ──────────────────────────────────
function dayDateStrFor(tid) {
  const s = calState[tid]
  const mm = String(s.viewMonth).padStart(2, '0')
  const dd = String(s.selectedDay).padStart(2, '0')
  return `${s.viewYear}-${mm}-${dd}`
}

function dayTasksFor(tid) {
  const s = calState[tid]
  const key = `${tid}-${s.viewYear}-${s.viewMonth}`
  const data = monthData.value[key]
  if (!data?.days) return []
  const dateStr = dayDateStrFor(tid)
  const dayData = data.days.find(d => (d.date || '').slice(0, 10) === dateStr)
  return dayData?.tasks || []
}

function formattedDayFor(tid) {
  const dateStr = dayDateStrFor(tid)
  const d = new Date(`${dateStr}T00:00:00`)
  const lcl = locale.value === 'pl' ? 'pl-PL' : 'en-US'
  const dayNum = d.getDate()
  const monthShort = d.toLocaleDateString(lcl, { month: 'short' })
    .replace(/^\w/, c => c.toUpperCase())
  const weekday = d.toLocaleDateString(lcl, { weekday: 'long' })
    .replace(/^\w/, c => c.toUpperCase())
  return `${dayNum} ${monthShort} — ${weekday}`
}

// ── Task actions ──────────────────────────────────────────────
function toggleTask(task, tid) {
  calendarStore.toggleComplete(task.id, dayDateStrFor(tid))
}

function doDelete(taskId, tid) {
  calendarStore.deleteTask(taskId, tid)
  confirmDelId.value = null
}

// ── Edit modal ────────────────────────────────────────────────
const formPl = ref('')
const formEn = ref('')
const formDate = ref('')
const formRepeat = ref('once')
const formInterval = ref(2)
const formNotes = ref('')

const repeatOptions = computed(() =>
  locale.value === 'pl'
    ? [['once','Raz'],['daily','Codziennie'],['every_n_days','Co N dni'],['weekdays','Dni robocze']]
    : [['once','Once'],['daily','Daily'],['every_n_days','Every N days'],['weekdays','Weekdays']]
)

function openNew(tid) {
  editModal.value = { task: null, day: calState[tid].selectedDay, tankId: tid }
}

watch(editModal, (val) => {
  if (!val) return
  const task = val.task
  formPl.value = task?.name_pl || ''
  formEn.value = task?.name_en || task?.name || ''
  formDate.value = task?.start_date || dayDateStrFor(val.tankId)
  formRepeat.value = task?.recurrence_type || 'once'
  formInterval.value = task?.interval_days || 2
  formNotes.value = task?.notes_pl || ''
})

async function saveTask() {
  if (!editModal.value) return
  const data = {
    tank_id: editModal.value.tankId,
    name: formPl.value || formEn.value,
    name_pl: formPl.value,
    name_en: formEn.value,
    start_date: formDate.value,
    recurrence_type: formRepeat.value,
    interval_days: formRepeat.value === 'every_n_days' ? (parseInt(formInterval.value) || 2) : undefined,
    notes_pl: formNotes.value,
  }
  if (editModal.value.task?.id) {
    await calendarStore.updateTask(editModal.value.task.id, data)
  } else {
    await calendarStore.createTask(data)
  }
  editModal.value = null
}

async function deleteTask() {
  if (!editModal.value?.task?.id) return
  await calendarStore.deleteTask(editModal.value.task.id, editModal.value.tankId)
  editModal.value = null
}
</script>

<style scoped>
.cal-cell { height: 48px; }
</style>
