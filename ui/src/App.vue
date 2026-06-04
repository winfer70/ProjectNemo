<template>
  <div class="app-shell">
    <!-- Header -->
    <header class="app-header">
      <span style="font-weight:700;font-size:15px;">🐟 PROJECT NEMO</span>
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:12px;color:var(--text-muted);">{{ currentTime }}</span>
        <div class="lang-toggle" @click="toggleLocale">
          <span :class="{ active: locale === 'en' }">EN</span>
          <span style="color:var(--border)"> | </span>
          <span :class="{ active: locale === 'pl' }">PL</span>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="app-content">
      <ScheduleView v-if="activeTab === 'schedule'" />
      <LiveView v-if="activeTab === 'live'" />
      <WaterTestsView v-if="activeTab === 'tests'" />
      <CalendarView v-if="activeTab === 'calendar'" />
      <LivestockView v-if="activeTab === 'livestock'" />
    </main>

    <!-- Bottom tab bar -->
    <nav class="tab-bar">
      <button class="tab-btn" :class="{ active: activeTab === 'schedule' }" @click="activeTab = 'schedule'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        {{ $t('nav.schedule') }}
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'live' }" @click="activeTab = 'live'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
        {{ $t('nav.live') }}
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'tests' }" @click="activeTab = 'tests'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>
        </svg>
        {{ $t('nav.tests') }}
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'calendar' }" @click="activeTab = 'calendar'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
          <line x1="8" y1="14" x2="8" y2="14"/>
          <line x1="12" y1="14" x2="12" y2="14"/>
          <line x1="16" y1="14" x2="16" y2="14"/>
        </svg>
        {{ $t('nav.calendar') }}
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'livestock' }" @click="activeTab = 'livestock'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M2 8L7 12L2 16"/>
          <path d="M7 12C7 12 11 6 17 6C20 6 22 9 22 12C22 15 20 18 17 18C11 18 7 12 7 12Z"/>
          <circle cx="17" cy="11" r="1" fill="currentColor" stroke="none"/>
        </svg>
        {{ $t('nav.livestock') }}
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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
const activeTab = ref('calendar')

const now = ref(new Date())
let clockTimer

const _refreshMap = {
  water_tests: () => { waterTestsStore.fetchLatest(); waterTestsStore.fetchSessions() },
  maintenance: () => maintenanceStore.fetchTasks(),
  schedule:    () => { scheduleStore.fetchFeedings(); scheduleStore.fetchHistory(); scheduleStore.fetchDosing() },
  supplies:    () => { sensorsStore.fetchSupplies(); scheduleStore.fetchDosing() },
  dosing:      () => { scheduleStore.fetchDosing(); sensorsStore.fetchSupplies() },
  calendar:    () => calendarStore.refetchCurrent(),
}
function _handleInvalidate(evt) {
  const fn = _refreshMap[evt.detail?.domain]
  if (fn) fn()
}

onMounted(() => {
  clockTimer = setInterval(() => { now.value = new Date() }, 1000)
  sensorsStore.connectWs()
  window.addEventListener('nemo:invalidate', _handleInvalidate)
})
onUnmounted(() => {
  clearInterval(clockTimer)
  sensorsStore.disconnectWs()
  window.removeEventListener('nemo:invalidate', _handleInvalidate)
})

const currentTime = computed(() => {
  return now.value.toLocaleTimeString(locale.value === 'pl' ? 'pl-PL' : 'en-IE', {
    hour: '2-digit', minute: '2-digit',
  })
})

function toggleLocale() {
  locale.value = locale.value === 'en' ? 'pl' : 'en'
  localStorage.setItem('nemo_locale', locale.value)
}
</script>
