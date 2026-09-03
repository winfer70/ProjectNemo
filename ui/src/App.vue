<template>
  <div class="nemo" :class="{ tablet: isTablet }" ref="rootRef" :style="{ zoom: appZoom }">
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
      </header>
      <main class="scroll" ref="scrollRef" @scroll="onScroll">
        <ScheduleView v-if="activeTab === 'schedule'" />
        <LiveView v-if="activeTab === 'live'" />
        <WaterTestsView v-if="activeTab === 'tests'" />
        <CalendarView v-if="activeTab === 'calendar'" />
        <LivestockView v-if="activeTab === 'livestock'" />
        <PlantHealthView v-if="activeTab === 'planthealth'" />
        <SettingsView v-if="activeTab === 'settings'" />
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
        <button :class="{ on: activeTab === 'planthealth' }" @click="goTab('planthealth')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
            <path d="M5 19c2-6 6-9 10-10"/>
          </svg>
          <span class="nlab">{{ $t('nav.planthealth') }}</span>
        </button>
        <button :class="{ on: activeTab === 'settings' }" @click="goTab('settings')">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
          <span class="nlab">{{ $t('nav.settings') }}</span>
        </button>
      </nav>
    </template>

    <template v-else>
      <header class="t-hdr">
        <div class="t-hdr-brand">
          <span class="fish">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
              <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
              <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
          </span>
          PROJECT NEMO
        </div>
        <div class="t-hdr-center">
          <div class="t-clock">{{ clock }}</div>
          <div class="t-date">{{ fullDate }}</div>
        </div>
        <div class="t-hdr-right">
          <div v-if="weather" class="t-weather">
            <span style="font-size:75px;line-height:1;flex-shrink:0">{{ wxEmoji(weather.code) }}</span>
            <div class="wx-main">
              <div class="wx-temp">{{ Math.round(weather.temp) }}°C</div>
              <div class="wx-cond">{{ wxLabel(weather.code) }}</div>
              <div class="wx-city">Ballivor, Meath</div>
            </div>
            <div class="wx-hl">
              <div>↑ {{ Math.round(weather.high) }}°</div>
              <div>↓ {{ Math.round(weather.low) }}°</div>
            </div>
          </div>
        </div>
      </header>
      <div class="t-body">
        <aside class="side">
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
            <button class="s-item" :class="{ on: activeTab === 'planthealth' }" @click="goTab('planthealth')">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
                <path d="M5 19c2-6 6-9 10-10"/>
              </svg>
              <span>{{ $t('nav.planthealth') }}</span>
            </button>
            <button class="s-item s-settings-btn" :class="{ on: activeTab === 'settings' }" @click="goTab('settings')">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
              <span>{{ $t('nav.settings') }}</span>
            </button>
          </div>
        </aside>
        <div class="main-pane">
          <main class="scroll" ref="scrollRef" @scroll="onScroll">
            <ScheduleView v-if="activeTab === 'schedule'" />
            <LiveView v-if="activeTab === 'live'" />
            <WaterTestsView v-if="activeTab === 'tests'" />
            <CalendarView v-if="activeTab === 'calendar'" />
            <LivestockView v-if="activeTab === 'livestock'" />
            <PlantHealthView v-if="activeTab === 'planthealth'" />
            <SettingsView v-if="activeTab === 'settings'" />
          </main>
          <div v-if="toast" class="toast-msg">{{ toast }}</div>
        </div>
      </div>
    </template>

    <!-- Kamilo assistant - floating shortcut on every tab, talk or type to
         update anything without hunting through the UI. -->
    <button class="kamilo-fab" @click="kamiloOpen = true" :title="$t('kamilo.title') || 'Kamilo'">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2a3 3 0 0 1 3 3v4a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z"/>
        <path d="M19 10v1a7 7 0 0 1-14 0v-1"/>
        <path d="M12 18v4"/>
        <path d="M9 22h6"/>
      </svg>
    </button>

    <Teleport to="body">
      <div v-if="kamiloOpen" class="backdrop" @click.self="kamiloOpen = false">
        <div class="modal" style="max-width:420px;width:92vw;padding:20px;display:flex;flex-direction:column;gap:12px;max-height:80vh" @click.stop>
          <div class="spread">
            <span style="font-weight:700;font-size:18px">Kamilo</span>
            <button class="btn icon-btn btn-ghost" @click="kamiloOpen = false">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
              </svg>
            </button>
          </div>

          <div style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:8px;min-height:120px">
            <div v-if="!kamiloLog.length" class="muted" style="font-size:12.5px;text-align:center;padding:16px 0">
              {{ locale === 'pl' ? 'Zapytaj lub powiedz Kamilo, co zaktualizować.' : 'Ask or tell Kamilo what to update.' }}
            </div>
            <div v-for="(m, i) in kamiloLog" :key="i" :style="{ alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }">
              <div style="padding:8px 12px;border-radius:12px;font-size:13.5px" :style="{ background: m.role === 'user' ? 'var(--accent)' : 'var(--surface-2,rgba(255,255,255,0.06))', color: m.role === 'user' ? '#fff' : 'var(--text)' }">
                {{ m.text }}
              </div>
            </div>
            <div v-if="kamiloBusy" class="muted" style="font-size:12.5px">{{ locale === 'pl' ? 'Kamilo myśli…' : 'Kamilo is thinking…' }}</div>
          </div>

          <div class="row" style="gap:8px">
            <button
              v-if="speechSupported"
              class="btn icon-btn"
              :class="kamiloListening ? 'btn-danger-o' : 'btn-ghost'"
              @click="toggleListening"
              :title="locale === 'pl' ? 'Mów' : 'Speak'"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a3 3 0 0 1 3 3v4a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z"/>
                <path d="M19 10v1a7 7 0 0 1-14 0v-1"/>
                <path d="M12 18v4"/><path d="M9 22h6"/>
              </svg>
            </button>
            <input
              class="input"
              v-model="kamiloInput"
              :placeholder="kamiloListening ? (locale === 'pl' ? 'Słucham…' : 'Listening…') : (locale === 'pl' ? 'Napisz do Kamilo…' : 'Type to Kamilo…')"
              style="flex:1"
              @keyup.enter="sendKamilo"
            >
            <button class="btn btn-accent" :disabled="kamiloBusy || !kamiloInput.trim()" @click="sendKamilo">
              {{ locale === 'pl' ? 'Wyślij' : 'Send' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, provide, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import ScheduleView from './views/ScheduleView.vue'
import LiveView from './views/LiveView.vue'
import WaterTestsView from './views/WaterTestsView.vue'
import CalendarView from './views/CalendarView.vue'
import LivestockView from './views/LivestockView.vue'
import PlantHealthView from './views/PlantHealthView.vue'
import SettingsView from './views/SettingsView.vue'
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
const weather = ref(null)
const fontScale = ref(parseInt(localStorage.getItem('nemo_fontscale') || '0'))
const appZoom = computed(() => Math.max(0.25, Math.min(3, 1 + fontScale.value / 100)))

function setFontScale(val) {
  fontScale.value = val
  localStorage.setItem('nemo_fontscale', String(val))
}

let clockTimer = null
let toastTimer = null
let wxTimer = null
let ro = null

function showToast(msg) {
  toast.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value = null }, 1700)
}

provide('showToast', showToast)
provide('fontScale', { fontScale, setFontScale })

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

const WX_LABELS = {
  0:  ['Clear sky',      'Bezchmurnie'],
  1:  ['Mainly clear',   'Małe zachmurzenie'],
  2:  ['Partly cloudy',  'Częściowe chmury'],
  3:  ['Overcast',       'Zachmurzenie'],
  45: ['Fog',            'Mgła'],
  48: ['Icy fog',        'Mgła z szronem'],
  51: ['Light drizzle',  'Lekka mżawka'],
  53: ['Drizzle',        'Mżawka'],
  55: ['Heavy drizzle',  'Silna mżawka'],
  61: ['Light rain',     'Lekki deszcz'],
  63: ['Rain',           'Deszcz'],
  65: ['Heavy rain',     'Silny deszcz'],
  71: ['Light snow',     'Lekki śnieg'],
  73: ['Snow',           'Śnieg'],
  75: ['Heavy snow',     'Silny śnieg'],
  77: ['Snow grains',    'Ziarna śniegu'],
  80: ['Showers',        'Przelotne opady'],
  81: ['Showers',        'Przelotne opady'],
  82: ['Heavy showers',  'Silne opady'],
  95: ['Thunderstorm',   'Burza'],
  96: ['Storm + hail',   'Burza z gradem'],
  99: ['Storm + hail',   'Burza z gradem'],
}

function wxLabel(code) {
  const entry = WX_LABELS[code]
  if (!entry) return ''
  return locale.value === 'pl' ? entry[1] : entry[0]
}

function wxEmoji(code) {
  if (code === 0) return '☀️'
  if (code <= 2) return '🌤️'
  if (code === 3) return '☁️'
  if (code <= 48) return '🌫️'
  if (code <= 57) return '🌦️'
  if (code <= 67) return '🌧️'
  if (code <= 77) return '❄️'
  if (code <= 82) return '🌧️'
  return '⛈️'
}

async function fetchWeather() {
  try {
    const r = await fetch(
      'https://api.open-meteo.com/v1/forecast?latitude=53.5563&longitude=-6.8847' +
      '&current=temperature_2m,weather_code,wind_speed_10m' +
      '&daily=temperature_2m_max,temperature_2m_min' +
      '&timezone=Europe%2FDublin&forecast_days=1'
    )
    const d = await r.json()
    weather.value = {
      temp: d.current.temperature_2m,
      code: d.current.weather_code,
      high: d.daily.temperature_2m_max[0],
      low:  d.daily.temperature_2m_min[0],
    }
  } catch {}
}

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
  water_tests: () => {
    waterTestsStore.fetchLatest()
    waterTestsStore.fetchSessions()
    waterTestsStore.fetchCurrent(1)
    waterTestsStore.fetchCurrent(2)
  },
  maintenance: () => maintenanceStore.fetchTasks(),
  schedule: () => { scheduleStore.fetchFeedings(); scheduleStore.fetchHistory(); scheduleStore.fetchDosing() },
  supplies: () => { sensorsStore.fetchSupplies(); scheduleStore.fetchDosing() },
  dosing: () => { scheduleStore.fetchDosing(); sensorsStore.fetchSupplies() },
  calendar: () => { calendarStore.refetchCurrent(); calendarStore.fetchToday() },
}

const _lastDate = ref(new Date().toDateString())

function _handleInvalidate(evt) {
  const fn = _refreshMap[evt.detail?.domain]
  if (fn) fn()
}

onMounted(() => {
  clockTimer = setInterval(() => { now.value = new Date() }, 1000)
  watch(now, () => {
    const d = now.value.toDateString()
    if (d !== _lastDate.value) {
      _lastDate.value = d
      _refreshMap.calendar?.()
      _refreshMap.schedule?.()
    }
  })
  fetchWeather()
  wxTimer = setInterval(fetchWeather, 30 * 60 * 1000)
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
  setFontScale(fontScale.value)
})

onUnmounted(() => {
  clearInterval(clockTimer)
  clearInterval(wxTimer)
  clearTimeout(toastTimer)
  sensorsStore.disconnectWs()
  window.removeEventListener('nemo:invalidate', _handleInvalidate)
  if (ro) ro.disconnect()
  if (recognition) recognition.stop()
})

// ─── Kamilo assistant popup ────────────────────────────────────────────────────
const kamiloOpen = ref(false)
const kamiloLog = ref([])
const kamiloInput = ref('')
const kamiloBusy = ref(false)
const kamiloListening = ref(false)
const kamiloConversationId = ref(null)

const SpeechRecognitionImpl = window.SpeechRecognition || window.webkitSpeechRecognition
const speechSupported = !!SpeechRecognitionImpl
let recognition = null
if (speechSupported) {
  recognition = new SpeechRecognitionImpl()
  recognition.continuous = false
  recognition.interimResults = false
  recognition.onresult = (e) => {
    kamiloInput.value = e.results[0][0].transcript
    sendKamilo()
  }
  recognition.onerror = () => { kamiloListening.value = false }
  recognition.onend = () => { kamiloListening.value = false }
}

function toggleListening() {
  if (!recognition) return
  if (kamiloListening.value) {
    recognition.stop()
    return
  }
  recognition.lang = locale.value === 'pl' ? 'pl-PL' : 'en-US'
  kamiloListening.value = true
  recognition.start()
}

async function sendKamilo() {
  const text = kamiloInput.value.trim()
  if (!text || kamiloBusy.value) return
  kamiloLog.value.push({ role: 'user', text })
  kamiloInput.value = ''
  kamiloBusy.value = true
  try {
    const r = await axios.post('/api/assistant/ask', {
      text,
      language: locale.value === 'pl' ? 'pl' : 'en',
      conversation_id: kamiloConversationId.value,
    })
    kamiloConversationId.value = r.data.conversation_id || kamiloConversationId.value
    kamiloLog.value.push({ role: 'assistant', text: r.data.reply })
  } catch (err) {
    kamiloLog.value.push({ role: 'assistant', text: locale.value === 'pl' ? 'Błąd połączenia z Kamilo.' : 'Could not reach Kamilo.' })
  } finally {
    kamiloBusy.value = false
  }
}
</script>
