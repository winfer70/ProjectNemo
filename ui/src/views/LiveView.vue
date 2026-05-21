<template>
  <div>
    <!-- Supply warnings banner -->
    <div v-if="sensorsStore.supplyWarnings.length" class="banner banner-warn">
      {{ $t('live.supplyWarnings') }}:
      <span v-for="s in sensorsStore.supplyWarnings" :key="s.id" style="margin-left:4px;">
        {{ locale === 'pl' ? s.name_pl : s.name }} {{ s.current_amount }}{{ s.unit }} — {{ $t('live.orderSoon') }}
      </span>
    </div>

    <!-- Sensors row -->
    <div class="grid-2">
      <!-- Temperature -->
      <div class="card">
        <div class="card-title">{{ $t('live.temperature') }}</div>
        <div class="gauge-value">
          {{ sensorsStore.current.temperature?.toFixed(1) ?? '—' }}
          <span class="gauge-unit">°C</span>
        </div>
        <div class="gauge-range">24.5 – 27.5°C</div>
        <span class="badge" :class="tempBadge">{{ tempStatus }}</span>
      </div>

      <!-- pH -->
      <div class="card">
        <div class="card-title">{{ $t('live.ph') }}</div>
        <div v-if="!phReading">
          <div v-if="sensorsStore.current.ph !== null" class="gauge-value">
            {{ sensorsStore.current.ph?.toFixed(2) ?? '—' }}
          </div>
          <div v-else style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">
            No recent reading
          </div>
          <div class="gauge-range">6.0 – 6.8 (Amazon biotope)</div>
          <button class="btn btn-sm btn-secondary" style="margin-top:10px;" @click="startPhReading">
            {{ $t('live.phReadingBtn') }}
          </button>
        </div>
        <div v-else class="ph-timer">
          <div class="ph-timer-ring"></div>
          <div style="font-size:14px;">{{ $t('live.phStabilising', { secs: phSecsLeft }) }}</div>
        </div>
      </div>
    </div>

    <!-- Smart Plugs -->
    <div class="card">
      <div class="card-title">{{ $t('live.smartPlugs') }}</div>
      <div class="grid-4">
        <div v-for="device in sensorsStore.devices" :key="device.entity_id"
             class="card plug-card" style="margin-bottom:0;background:var(--bg-card2);"
             @click="sensorsStore.toggleDevice(device.entity_id)">
          <div style="font-size:12px;font-weight:600;">
            {{ locale === 'pl' ? device.name_pl : device.name }}
          </div>
          <div class="plug-state" :class="device.state">
            {{ device.state === 'on' ? $t('live.on') : device.state === 'off' ? $t('live.off') : $t('live.unavailable') }}
          </div>
          <div class="plug-watts" v-if="device.watts !== null">
            {{ device.watts?.toFixed(1) }} W
          </div>
          <div class="plug-kwh" v-if="device.kwh_today !== null">
            {{ device.kwh_today?.toFixed(3) }} kWh
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSensorsStore } from '../stores/sensors'

const { locale } = useI18n()
const sensorsStore = useSensorsStore()

const phReading = ref(false)
const phSecsLeft = ref(300)
let phTimer = null

const tempBadge = computed(() => {
  const t = sensorsStore.current.temperature
  if (t === null) return 'badge-warn'
  if (t < 24.5 || t > 27.5) return 'badge-danger'
  return 'badge-ok'
})
const tempStatus = computed(() => {
  const { t } = useI18n()
  const temp = sensorsStore.current.temperature
  if (temp === null) return t('live.unavailable')
  if (temp < 24.5 || temp > 27.5) return t('tests.outOfRange')
  return t('tests.ok')
})

function startPhReading() {
  phReading.value = true
  phSecsLeft.value = 300
  phTimer = setInterval(() => {
    phSecsLeft.value--
    if (phSecsLeft.value <= 0) {
      clearInterval(phTimer)
      phReading.value = false
      sensorsStore.fetchCurrent()
    }
  }, 1000)
}

onMounted(() => {
  sensorsStore.connectWs()
  sensorsStore.fetchDevices()
  sensorsStore.fetchSupplies()
})
onUnmounted(() => {
  sensorsStore.disconnectWs()
  if (phTimer) clearInterval(phTimer)
})
</script>
