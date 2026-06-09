<template>
  <div class="nemo" :class="{ tablet: isTablet }" ref="rootRef">
    <template v-if="!isTablet">
      <header class="hdr">
        <div class="hdr-dt">
          <div class="hdr-dt-day">{{ shortDay }}</div>
          <div class="hdr-dt-bottom">
            <span class="hdr-dt-date">{{ shortDate }}</span>
            <span class="hdr-dt-sep">·</span>
            <span class="hdr-dt-clock">{{ clock }}</span>
          </div>
        </div>
        <div class="hdr-locale">
          <button :class="{ on: locale === 'en' }" @click="setLocale('en')">EN</button>
          <button :class="{ on: locale === 'pl' }" @click="setLocale('pl')">PL</button>
        </div>
      </header>
      <main class="scroll" ref="scrollRef" @scroll="onScroll">
        <ScheduleView v-if="activeTab === 'schedule'" />
        <LiveView v-if="activeTab === 'live'" />
        <WaterTestsView v-if="activeTab === 'tests'" />
        <CalendarView v-if="activeTab === 'calendar'" />
        <LivestockView v-if="activeTab === 'livestock'" />
      </main>
      <div v-if="toast" class="toast-msg">{{ toast }}</div>
      <nav class="nav" :class="{ hidden: navHidden }">
        <button :class="{ on: activeTab === 'schedule' }" @click="goTab('schedule')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4.5" width="18" height="16" rx="2.5"/>
            <path d="M3 9h18"/>
            <path d="M8 2.5v4"/>
            <path d="M16 2.5v4"/>
            <path d="M8.5 14.5l2.2 2.2 4-4.4"/>
          </svg>
          <span class="nlab">{{ $t('nav.schedule') }}</span>
        </button>
        <button :class="{ on: activeTab === 'live' }" @click="goTab('live')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 12h3.5l2-6 4 12 2.5-6H21"/>
          </svg>
          <span class="nlab">{{ $t('nav.live') }}</span>
        </button>
        <button :class="{ on: activeTab === 'tests' }" @click="goTab('tests')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
          </svg>
          <span class="nlab">{{ $t('nav.tests') }}</span>
        </button>
        <button :class="{ on: activeTab === 'calendar' }" @click="goTab('calendar')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4.5" width="18" height="16" rx="2.5"/>
            <path d="M3 9.5h18"/>
            <path d="M8 2.5v4"/>
            <path d="M16 2.5v4"/>
          </svg>
          <span class="nlab">{{ $t('nav.calendar') }}</span>
        </button>
        <button :class="{ on: activeTab === 'livestock' }" @click="goTab('livestock')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
            <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
            <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
          </svg>
          <span class="nlab">{{ $t('nav.livestock') }}</span>
        </button>
      </nav>
    </template>

    <template v-else>
      <aside class="side">
        <div class="s-brand">
          <span class="fish">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
              <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
              <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
          </span>
          PROJECT NEMO
        </div>
        <div class="s-clock">
          <div class="c">{{ clock }}</div>
          <div class="s-date">{{ fullDate }}</div>
        </div>
        <div class="s-nav">
          <button class="s-item" :class="{ on: activeTab === 'schedule' }" @click="goTab('schedule')">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4.5" width="18" height="16" rx="2.5"/>
              <path d="M3 9h18"/>
              <path d="M8 2.5v4"/>
              <path d="M16 2.5v4"/>
              <path d="M8.5 14.5l2.2 2.2 4-4.4"/>
            </svg>
            <span>{{ $t('nav.schedule') }}</span>
          </button>
          <button class="s-item" :class="{ on: activeTab === 'live' }" @click="goTab('live')">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12h3.5l2-6 4 12 2.5-6H21"/>
            </svg>
            <span>{{ $t('nav.live') }}</span>
          </button>
          <button class="s-item" :class="{ on: activeTab === 'tests' }" @click="goTab('tests')">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
            </svg>
            <span>{{ $t('nav.tests') }}</span>
          </button>
          <button class="s-item" :class="{ on: activeTab === 'calendar' }" @click="goTab('calendar')">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4.5" width="18" height="16" rx="2.5"/>
              <path d="M3 9.5h18"/>
              <path d="M8 2.5v4"/>
              <path d="M16 2.5v4"/>
            </svg>
            <span>{{ $t('nav.calendar') }}</span>
          </button>
          <button class="s-item" :class="{ on: activeTab === 'livestock' }" @click="goTab('livestock')">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
              <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
              <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
            <span>{{ $t('nav.livestock') }}</span>
          </button>
        </div>
        <div class="s-foot">
          <div class="s-foot-info">
            <span class="lab">{{ locale === 'pl' ? 'Serwer' : 'Server' }}</span>
            <span class="chip" style="color: var(--success)">
              <span class="dot on"></span>
              REDACTED-HOST · {{ locale === 'pl' ? 'połączony' : 'connected' }}
            </span>
          </div>
          <div class="s-foot-locale">
            <div class="hdr-locale">
              <button :class="{ on: locale === 'en' }" @click="setLocale('en')">EN</button>
              <button :class="{ on: locale === 'pl' }" @click="setLocale('pl')">PL</button>
            </div>
          </div>
        </div>
      </aside>
      <div class="main-pane">
        <main class="scroll" ref="scrollRef" @scroll="onScroll">
          <ScheduleView v-if="activeTab === 'schedule'" />
          <LiveView v-if="activeTab === 'live'" />
          <WaterTestsView v-if="activeTab === 'tests'" />
          <CalendarView v-if="activeTab === 'calendar'" />
          <LivestockView v-if="activeTab === 'livestock'" />
        </main>
        <div v-if="toast" class="toast-msg">{{ toast }}</div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, provide } from 'vue'
import { useI18n } from 'vue-i18n'
import ScheduleView from './views/ScheduleView.vue'
import LiveView from './views/LiveView.vue'
import WaterTestsView from './views/WaterTestsView.vue'
import CalendarView from './views/CalendarView.vue'
import LivestockView from './views/LivestockView.vue'
import { useSensorsStore } from './stores/sensors'
import { useWaterTestsStore } from './stores/waterTests'
import { useMaintenanceStore } from './stores/maintenance'
import { useScheduleStore } from './stores/schedule'
import { useCalendarStore } from './stores/calendar'

const { locale } = useI18n()

const sensorsStore = useSensorsStore()
const waterTestsStore = useWaterTestsStore()
const maintenanceStore = useMaintenanceStore()
const scheduleStore = useScheduleStore()
const calendarStore = useCalendarStore()

const rootRef = ref(null)
const scrollRef = ref(null)
const activeTab = ref('schedule')
const navHidden = ref(false)
const isTablet = ref(false)
const toast = ref(null)
const now = ref(new Date())
const lastScroll = ref(0)

let clockTimer = null
let toastTimer = null
let ro = null

function showToast(msg) {
  toast.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value = null }, 1700)
}

provide('showToast', showToast)

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('nemo_locale', lang)
}

const clock = computed(() => {
  const h = String(now.value.getHours()).padStart(2, '0')
  const m = String(now.value.getMinutes()).padStart(2, '0')
  return `${h}:${m}`
})

const shortDay = computed(() => {
  const d = now.value
  if (locale.value === 'pl') {
    return ['Ndz', 'Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob'][d.getDay()]
  }
  return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getDay()]
})

const shortDate = computed(() => {
  const d = now.value
  if (locale.value === 'pl') {
    const months = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru']
    return `${d.getDate()} ${months[d.getMonth()]}`
  }
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[d.getMonth()]} ${d.getDate()}`
})

const fullDate = computed(() => {
  const d = now.value
  if (locale.value === 'pl') {
    const days = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota']
    const months = ['Stycznia', 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca', 'Lipca', 'Sierpnia', 'Września', 'Października', 'Listopada', 'Grudnia']
    return `${days[d.getDay()]}, ${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
  }
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  return `${days[d.getDay()]}, ${months[d.getMonth()]} ${d.getDate()} ${d.getFullYear()}`
})

function onScroll(e) {
  const y = e.target.scrollTop
  if (y > lastScroll.value + 6 && y > 40) navHidden.value = true
  else if (y < lastScroll.value - 6) navHidden.value = false
  lastScroll.value = y
}

function goTab(id) {
  activeTab.value = id
  if (scrollRef.value) scrollRef.value.scrollTop = 0
  navHidden.value = false
}

const _refreshMap = {
  water_tests: () => { waterTestsStore.fetchLatest(); waterTestsStore.fetchSessions() },
  maintenance: () => maintenanceStore.fetchTasks(),
  schedule: () => { scheduleStore.fetchFeedings(); scheduleStore.fetchHistory(); scheduleStore.fetchDosing() },
  supplies: () => { sensorsStore.fetchSupplies(); scheduleStore.fetchDosing() },
  dosing: () => { scheduleStore.fetchDosing(); sensorsStore.fetchSupplies() },
  calendar: () => { calendarStore.refetchCurrent(); calendarStore.fetchToday() },
}

function _handleInvalidate(evt) {
  const fn = _refreshMap[evt.detail?.domain]
  if (fn) fn()
}

onMounted(() => {
  clockTimer = setInterval(() => { now.value = new Date() }, 1000)
  sensorsStore.connectWs()
  window.addEventListener('nemo:invalidate', _handleInvalidate)
  if (rootRef.value) {
    const measure = () => {
      if (rootRef.value) isTablet.value = rootRef.value.offsetWidth >= 720
    }
    measure()
    ro = new ResizeObserver(measure)
    ro.observe(rootRef.value)
  }
})

onUnmounted(() => {
  clearInterval(clockTimer)
  clearTimeout(toastTimer)
  sensorsStore.disconnectWs()
  window.removeEventListener('nemo:invalidate', _handleInvalidate)
  if (ro) ro.disconnect()
})
</script>
