<template>
  <div style="display:flex;gap:12px;align-items:flex-start">
  <!-- ── Tile 1: Calendar grid ──────────────────────────────────── -->
  <div class="tile" style="zoom:0.8;flex:3;min-width:0">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/>
        </svg>
        KALENDARZ
      </h2>
      <button class="btn btn-sm btn-accent" @click="openNew">
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
        <button class="btn icon-btn btn-ghost" @click="prevMonth">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 5l-7 7 7 7"/>
          </svg>
        </button>
        <span style="font-weight:700;font-size:15px">{{ monthName }} {{ viewYear }}</span>
        <button class="btn icon-btn btn-ghost" @click="nextMonth">
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
        <template v-for="(cell, i) in calCells" :key="i">
          <div v-if="cell === null" />
          <div v-else
            :class="['cal-cell', isToday(cell) ? 'today' : '', cell === selectedDay ? 'sel' : '']"
            @click="selectedDay = cell"
          >
            {{ cell }}
            <span v-if="taskDays.has(cell)" class="cdot" />
          </div>
        </template>
      </div>
    </div>
  </div>

  <!-- ── Tile 2: Selected day tasks ─────────────────────────────── -->
  <div class="tile" style="flex:2;min-width:0">
    <div class="tile-hd">
      <h2>{{ formattedDay }}</h2>
    </div>
    <hr class="divider">
    <div class="tile-body" style="padding-top:6px">

      <!-- Empty state -->
      <div v-if="!dayTasks.length" class="empty">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/>
        </svg>
        <span>{{ locale === 'pl' ? 'Wolny dzień' : 'Free day' }}</span>
      </div>

      <!-- Task rows with swipe-to-complete -->
      <template v-else>
        <div v-for="(task, i) in dayTasks" :key="task.id" style="position:relative;overflow:hidden">
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
            @mouseup="swipeEnd(task)"
            @mouseleave="swipeLeave(task)"
            @touchstart.passive="swipeBegin($event, task.id)"
            @touchmove.passive="swipeMove($event, task.id)"
            @touchend="swipeEnd(task)"
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
                <button class="btn icon-btn btn-danger-o" @click.stop="doDelete(task.id)">
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
                <button :class="['btn', 'icon-btn', task.completed ? 'btn-success' : '']" @click.stop="toggleTask(task)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 12.5l5 5 11-12"/>
                  </svg>
                </button>
                <button class="btn icon-btn btn-ghost" @click.stop="editModal = { task, day: selectedDay }">
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
      <button class="btn btn-block btn-ghost" style="margin-top:12px" @click="openNew">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14"/><path d="M5 12h14"/>
        </svg>
        {{ locale === 'pl' ? 'Dodaj zadanie' : 'Add task' }}
      </button>
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
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { ref, computed, reactive, onMounted, watch } from 'vue'

const { locale } = useI18n()
const calendarStore = useCalendarStore()
const { monthData } = storeToRefs(calendarStore)

// ── Date state ────────────────────────────────────────────────
const today = new Date()
const viewYear = ref(today.getFullYear())
const viewMonth = ref(today.getMonth() + 1)  // 1-based
const selectedDay = ref(today.getDate())
const confirmDelId = ref(null)
const editModal = ref(null)  // null | { task, day }

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

function swipeEnd(task) {
  if (swipeActiveId.value !== task.id) return
  if ((swipeDx[task.id] || 0) > 70 && !task.completed) {
    calendarStore.toggleComplete(task.id, dayDateStr.value)
  }
  swipeDx[task.id] = 0
  swipeActiveId.value = null
  _swipeStartX = null
}

function swipeLeave(task) {
  if (swipeActiveId.value === task.id) swipeEnd(task)
}

// ── Month navigation ──────────────────────────────────────────
function prevMonth() {
  if (viewMonth.value === 1) { viewMonth.value = 12; viewYear.value-- }
  else viewMonth.value--
}

function nextMonth() {
  if (viewMonth.value === 12) { viewMonth.value = 1; viewYear.value++ }
  else viewMonth.value++
}

watch([viewYear, viewMonth], ([y, m]) => calendarStore.fetchMonth(y, m))
onMounted(() => calendarStore.fetchMonth(viewYear.value, viewMonth.value))

// ── Locale helpers ────────────────────────────────────────────
const PL_MONTHS = ['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień']
const EN_MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
const PL_DOWS = ['Pn','Wt','Śr','Cz','Pt','Sb','Nd']
const EN_DOWS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

const monthName = computed(() =>
  locale.value === 'pl' ? PL_MONTHS[viewMonth.value - 1] : EN_MONTHS[viewMonth.value - 1]
)
const dows = computed(() => locale.value === 'pl' ? PL_DOWS : EN_DOWS)

// ── Calendar grid ─────────────────────────────────────────────
const calCells = computed(() => {
  const first = new Date(viewYear.value, viewMonth.value - 1, 1)
  const offset = (first.getDay() + 6) % 7  // Monday-first
  const daysInMonth = new Date(viewYear.value, viewMonth.value, 0).getDate()
  const cells = []
  for (let i = 0; i < offset; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)
  return cells
})

function isToday(day) {
  return (
    day === today.getDate() &&
    viewMonth.value === today.getMonth() + 1 &&
    viewYear.value === today.getFullYear()
  )
}

// ── Days that have tasks (for dots) ──────────────────────────
const taskDays = computed(() => {
  const key = `${viewYear.value}-${viewMonth.value}`
  const data = monthData.value[key]
  const s = new Set()
  if (!data?.days) return s
  for (const d of data.days) {
    if (d.tasks?.length > 0) s.add(parseInt(d.date.slice(8), 10))
  }
  return s
})

// ── Selected day ──────────────────────────────────────────────
const dayDateStr = computed(() => {
  const mm = String(viewMonth.value).padStart(2, '0')
  const dd = String(selectedDay.value).padStart(2, '0')
  return `${viewYear.value}-${mm}-${dd}`
})

const dayTasks = computed(() => {
  const key = `${viewYear.value}-${viewMonth.value}`
  const data = monthData.value[key]
  if (!data?.days) return []
  const dayData = data.days.find(d => (d.date || '').slice(0, 10) === dayDateStr.value)
  return dayData?.tasks || []
})

const formattedDay = computed(() => {
  const d = new Date(`${dayDateStr.value}T00:00:00`)
  const lcl = locale.value === 'pl' ? 'pl-PL' : 'en-US'
  const dayNum = d.getDate()
  const monthShort = d.toLocaleDateString(lcl, { month: 'short' })
    .replace(/^\w/, c => c.toUpperCase())
  const weekday = d.toLocaleDateString(lcl, { weekday: 'long' })
    .replace(/^\w/, c => c.toUpperCase())
  return `${dayNum} ${monthShort} — ${weekday}`
})

// ── Task actions ──────────────────────────────────────────────
function toggleTask(task) {
  calendarStore.toggleComplete(task.id, dayDateStr.value)
}

function doDelete(taskId) {
  calendarStore.deleteTask(taskId)
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

function openNew() {
  editModal.value = { task: null, day: selectedDay.value }
}

watch(editModal, (val) => {
  if (!val) return
  const task = val.task
  formPl.value = task?.name_pl || ''
  formEn.value = task?.name_en || task?.name || ''
  formDate.value = task?.start_date || dayDateStr.value
  formRepeat.value = task?.recurrence_type || 'once'
  formInterval.value = task?.interval_days || 2
  formNotes.value = task?.notes_pl || ''
})

async function saveTask() {
  if (!editModal.value) return
  const data = {
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
  await calendarStore.deleteTask(editModal.value.task.id)
  editModal.value = null
}
</script>
