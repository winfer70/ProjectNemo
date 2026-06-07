<template>
  <div>
    <!-- Connection header row -->
    <div class="spread" style="padding: 2px 4px">
      <h2 style="margin:0;font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted)">
        NA ŻYWO
      </h2>
      <span class="chip" :style="{ color: wsConnected ? 'var(--success)' : 'var(--warning)' }">
        <span v-if="wsConnected" class="dot on" />
        <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 4l20 20" />
          <path d="M5 9a11 11 0 0 1 4-2.5" />
          <path d="M16 9.5a11 11 0 0 1 3-0.5" />
          <path d="M8 12.5a6.5 6.5 0 0 1 3-1.8" />
          <circle cx="12" cy="18.5" r="0.7" fill="currentColor" stroke="none" />
        </svg>
        {{ wsConnected ? 'Połączono' : 'Rozłączono' }}
      </span>
    </div>

    <!-- Offline banner -->
    <div v-if="!wsConnected" class="banner stale">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M2 4l20 20" />
        <path d="M5 9a11 11 0 0 1 4-2.5" />
        <path d="M16 9.5a11 11 0 0 1 3-0.5" />
        <path d="M8 12.5a6.5 6.5 0 0 1 3-1.8" />
        <circle cx="12" cy="18.5" r="0.7" fill="currentColor" stroke="none" />
      </svg>
      Ostatnia synchronizacja: {{ minutesSinceSync }} min temu
    </div>

    <!-- Sensor grid -->
    <div class="sensor-grid">
      <!-- Temperature card -->
      <div class="sensor">
        <span class="lab">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13.5V5a2 2 0 0 1 4 0v8.5a4 4 0 1 1-4 0z" />
            <circle cx="12" cy="16" r="1.4" fill="currentColor" stroke="none" />
          </svg>
          Temperatura
        </span>
        <span class="val tnum">{{ tempDisplay }}<small>°C</small></span>
        <svg class="spark" viewBox="0 0 100 30" preserveAspectRatio="none">
          <polyline
            v-if="tempSparkPts"
            :points="tempSparkPts"
            fill="none"
            stroke="var(--accent-warm)"
            stroke-width="1.6"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <span class="range">
          <span>min {{ tempMin }}</span>
          <span>max {{ tempMax }}</span>
        </span>
      </div>

      <!-- pH card -->
      <div class="sensor">
        <span class="lab">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z" />
          </svg>
          pH
        </span>
        <span class="val tnum">{{ phDisplay }}</span>
        <svg class="spark" viewBox="0 0 100 30" preserveAspectRatio="none">
          <polyline
            v-if="phSparkPts"
            :points="phSparkPts"
            fill="none"
            stroke="var(--accent)"
            stroke-width="1.6"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <span class="range">
          <span class="tnum">{{ phMin }}–{{ phMax }}</span>
          <span style="color:var(--success)">optymalny</span>
        </span>
      </div>
    </div>

    <!-- Devices tile -->
    <div class="tile">
      <div class="tile-hd"><h2>URZĄDZENIA</h2></div>
      <hr class="divider" />
      <div class="tile-body" style="padding-top:4px">
        <div
          v-for="d in sensorsStore.devices"
          :key="d.entity_id"
          class="dev"
          style="padding:12px 2px"
        >
          <span class="dev-ico">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" />
            </svg>
          </span>
          <div class="dev-name">
            <div class="n" style="font-weight:600">{{ locale === 'pl' ? d.name_pl : d.name }}</div>
            <div class="row" style="gap:6px;margin-top:2px">
              <span :class="['dot', d.state === 'on' ? 'on' : 'off']" />
              <span class="muted" style="font-size:12px">{{ d.state === 'on' ? 'ON' : 'OFF' }}</span>
            </div>
          </div>
          <span class="muted tnum" style="font-size:13px;min-width:38px;text-align:right">
            {{ d.state === 'on' ? d.watts : 0 }}W
          </span>
          <button
            :class="['toggle', d.state === 'on' ? 'on accent' : '']"
            @click="sensorsStore.toggleDevice(d.entity_id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useSensorsStore } from '../stores/sensors'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const sensorsStore = useSensorsStore()

const HIST_MAX = 12
const tempHistory = ref([])
const phHistory = ref([])
const lastSyncAt = ref(Date.now())
const nowMs = ref(Date.now())
let clockInterval = null

// WS connection state — tracks BLE command socket exposed by the store
const wsConnected = computed(() => sensorsStore.wsConnection !== null)

const minutesSinceSync = computed(() =>
  Math.floor((nowMs.value - lastSyncAt.value) / 60000)
)

const tempDisplay = computed(() => {
  const t = sensorsStore.current.temperature
  return t !== null && t !== undefined ? t.toFixed(1) : '—'
})

const phDisplay = computed(() => {
  const p = sensorsStore.current.ph
  return p !== null && p !== undefined ? p.toFixed(1) : '—'
})

const tempMin = computed(() =>
  tempHistory.value.length ? Math.min(...tempHistory.value).toFixed(1) : '—'
)
const tempMax = computed(() =>
  tempHistory.value.length ? Math.max(...tempHistory.value).toFixed(1) : '—'
)
const phMin = computed(() =>
  phHistory.value.length ? Math.min(...phHistory.value).toFixed(1) : '—'
)
const phMax = computed(() =>
  phHistory.value.length ? Math.max(...phHistory.value).toFixed(1) : '—'
)

function computeSparkPts(history) {
  if (history.length < 2) return null
  const w = 100, h = 30, pad = 2
  const min = Math.min(...history)
  const max = Math.max(...history)
  const rng = max - min || 1
  return history
    .map((v, i) => {
      const x = pad + (i / (history.length - 1)) * (w - pad * 2)
      const y = h - pad - ((v - min) / rng) * (h - pad * 2)
      return `${x.toFixed(1)},${y.toFixed(1)}`
    })
    .join(' ')
}

const tempSparkPts = computed(() => computeSparkPts(tempHistory.value))
const phSparkPts = computed(() => computeSparkPts(phHistory.value))

watch(
  () => sensorsStore.current.temperature,
  (val) => {
    if (val === null || val === undefined) return
    lastSyncAt.value = Date.now()
    tempHistory.value.push(val)
    if (tempHistory.value.length > HIST_MAX) tempHistory.value.shift()
  }
)

watch(
  () => sensorsStore.current.ph,
  (val) => {
    if (val === null || val === undefined) return
    phHistory.value.push(val)
    if (phHistory.value.length > HIST_MAX) phHistory.value.shift()
  }
)

onMounted(() => {
  sensorsStore.connectWs()
  sensorsStore.fetchDevices()
  clockInterval = setInterval(() => { nowMs.value = Date.now() }, 30000)
})

onUnmounted(() => {
  sensorsStore.disconnectWs()
  clearInterval(clockInterval)
})
</script>
