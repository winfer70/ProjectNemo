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
          {{ effectiveTemp?.toFixed(1) ?? '—' }}
          <span class="gauge-unit">°C</span>
        </div>
        <div class="gauge-range">24.5 – 27.5°C</div>
        <span class="badge" :class="tempBadge">{{ tempStatus }}</span>

        <!-- Manual temperature override -->
        <div v-if="useManual" style="margin-top:10px;">
          <span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;background:#f59e0b;color:#000;margin-bottom:6px;">
            {{ $t('live.manualTempBadge') }}
          </span>
          <input
            type="number"
            step="0.1"
            v-model.number="manualTemp"
            style="width:100%;background:var(--bg);border:1px solid #f59e0b;border-radius:6px;color:var(--text);padding:8px;font-size:14px;box-sizing:border-box;"
            :placeholder="$t('live.manualTempPlaceholder')"
          />
          <button v-if="sensorsStore.current.temperature !== null"
                  class="btn btn-sm btn-secondary"
                  style="margin-top:6px;font-size:11px;"
                  @click="useManual = false">
            {{ $t('live.useSensor') }}
          </button>
        </div>
        <div v-else style="margin-top:8px;">
          <button class="btn btn-sm btn-secondary" style="font-size:11px;" @click="useManual = true">
            🌡️ {{ $t('live.manualTempToggle') }}
          </button>
        </div>
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
             :style="device.role === 'light' ? { borderTop: '2px solid #aa44ff' } : {}"
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
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSensorsStore } from '../stores/sensors'

const { locale } = useI18n()
const sensorsStore = useSensorsStore()

const manualTemp = ref(
  localStorage.getItem('nemo_manual_temp')
    ? parseFloat(localStorage.getItem('nemo_manual_temp'))
    : null
)
const useManual = ref(sensorsStore.current.temperature === null)

const effectiveTemp = computed(() =>
  useManual.value ? manualTemp.value : sensorsStore.current.temperature
)

const phReading = ref(false)
const phSecsLeft = ref(300)
let phTimer = null

const tempBadge = computed(() => {
  const t = effectiveTemp.value
  if (t === null || t === undefined) return 'badge-warn'
  if (t < 24.5 || t > 27.5) return 'badge-danger'
  return 'badge-ok'
})
const tempStatus = computed(() => {
  const { t } = useI18n()
  const temp = effectiveTemp.value
  if (temp === null || temp === undefined) return t('live.unavailable')
  if (temp < 24.5 || temp > 27.5) return t('tests.outOfRange')
  return t('tests.ok')
})

watch(() => sensorsStore.current.temperature, (val) => {
  if (val === null) useManual.value = true
})
watch(manualTemp, (val) => {
  if (val !== null && val !== undefined) {
    localStorage.setItem('nemo_manual_temp', String(val))
  }
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
