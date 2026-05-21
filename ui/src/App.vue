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

const { locale } = useI18n()
const activeTab = ref('calendar')

const now = ref(new Date())
let clockTimer
onMounted(() => { clockTimer = setInterval(() => { now.value = new Date() }, 1000) })
onUnmounted(() => clearInterval(clockTimer))

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
