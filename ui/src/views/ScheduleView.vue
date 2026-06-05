<template>
  <div>
    <!-- Filter paused banner -->
    <div v-if="scheduleStore.filterPausedSecs > 0" class="banner banner-warn">
      {{ $t('schedule.filterPaused', { secs: scheduleStore.filterPausedSecs }) }}
    </div>

    <!-- Feeding + Dosing + Lighting grid -->
    <div class="grid-3">
      <!-- FEEDING card -->
      <div class="card">
        <div class="card-title">{{ $t('schedule.feeding') }}</div>
        <div v-if="nextFeeding" style="margin-bottom:8px;font-size:13px;">
          {{ $t('schedule.nextFeed', { time: nextFeeding.time_of_day }) }}
        </div>
        <div v-if="lastFed" style="font-size:12px;color:var(--text-muted);margin-bottom:12px;">
          {{ $t('schedule.lastFed', { time: formatTime(lastFed.timestamp) }) }}
        </div>
        <button class="btn btn-primary btn-full" @click="handleFeedNow">
          {{ $t('schedule.feedNow') }}
        </button>
        <div style="margin-top:10px;">
          <div v-for="log in recentFeedings" :key="log.id"
               style="font-size:11px;color:var(--text-muted);padding:2px 0;">
            {{ formatTime(log.timestamp) }} ✓
          </div>
        </div>
      </div>

      <!-- DOSING card -->
      <div class="card">
        <div class="card-title">{{ $t('schedule.dosing') }}</div>
        <div v-for="task in scheduleStore.dosingTasks" :key="task.id" style="margin-bottom:12px;">
          <div style="font-size:13px;font-weight:600;">
            {{ locale === 'pl' ? task.supply_name_pl : task.supply_name }}
          </div>
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">
            {{ $t('schedule.doseIn', { amount: task.dose_amount, unit: task.dose_unit }) }}
            <span v-if="task.time_of_day"> · {{ task.time_of_day }}</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill"
                 :class="supplyClass(task.current_supply, task.supply_unit)"
                 :style="{ width: supplyPct(task.current_supply, task.dose_amount) + '%' }">
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:11px;color:var(--text-muted);">
              {{ $t('schedule.remaining', { amount: (task.current_supply?.toFixed(0) ?? '—'), unit: task.supply_unit }) }}
            </span>
            <button class="btn btn-sm btn-primary" @click="scheduleStore.completeDose(task.id)">
              {{ $t('schedule.complete') }}
            </button>
          </div>
        </div>
      </div>

      <!-- LIGHTING card -->
      <div class="card">
        <div class="card-title">{{ $t('schedule.lighting') }}</div>
        <div style="margin-bottom:10px;display:flex;align-items:center;justify-content:space-between;">
          <span style="font-size:13px;font-weight:700;"
                :style="{ color: lightOn ? 'var(--ok)' : 'var(--text-muted)' }">
            {{ lightOn ? $t('lighting.on') : $t('lighting.off') }}
          </span>
          <button class="btn btn-sm btn-secondary" @click="sensorsStore.toggleDevice(lightEntity)">
            {{ $t('lighting.toggle') }}
          </button>
        </div>
        <button
          class="btn btn-sm btn-full"
          :class="sensorsStore.bleConnected ? 'btn-secondary' : 'btn-primary'"
          style="margin-bottom:10px;"
          @click="handleBleConnect"
        >
          <span v-if="!sensorsStore.bleConnected">{{ $t('lighting.connect') }}</span>
          <span v-else>{{ $t('lighting.connected') }} <span style="color:var(--ok)">&#9679;</span></span>
        </button>
        <div class="channel-slider" v-for="(ch, key) in channels" :key="key">
          <span class="channel-label" :style="{ color: channelColors[key] }">
            {{ $t('lighting.' + key) }}
          </span>
          <input type="range" min="0" max="100" v-model.number="channels[key]" @change="pushChannels"
                 :disabled="!sensorsStore.bleConnected" />
          <span class="channel-value">{{ channels[key] }}%</span>
        </div>
      </div>
    </div>

    <!-- Maintenance tasks -->
    <div class="card">
      <div class="card-title">{{ $t('schedule.maintenance') }}</div>
      <div class="grid-3">
        <div v-for="task in maintenanceStore.tasks" :key="task.id"
             class="card" style="margin-bottom:0;background:var(--bg-card2);">
          <div style="font-size:13px;font-weight:600;margin-bottom:4px;">
            {{ locale === 'pl' ? task.name_pl : task.name }}
          </div>
          <div style="font-size:12px;margin-bottom:8px;" :style="{ color: dueBadgeColor(task.days_until) }">
            {{ dueLabel(task) }}
          </div>
          <div class="progress-bar">
            <div class="progress-fill"
                 :class="dueProgressClass(task.days_until, task.interval_days)"
                 :style="{ width: dueProgressPct(task.days_until, task.interval_days) + '%' }">
            </div>
          </div>
          <button class="btn btn-sm btn-secondary btn-full" style="margin-top:8px;"
                  @click="openMaintModal(task)">
            {{ $t('maintenance.start') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Maintenance Modal -->
    <MaintenanceModal
      v-if="maintModalTask"
      :task="maintModalTask"
      @close="maintModalTask = null"
      @done="onMaintDone"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useScheduleStore } from '../stores/schedule'
import { useSensorsStore } from '../stores/sensors'
import { useMaintenanceStore } from '../stores/maintenance'
import MaintenanceModal from '../components/MaintenanceModal.vue'
import * as bleService from '../services/bleService'

const { locale } = useI18n()
const scheduleStore = useScheduleStore()
const sensorsStore = useSensorsStore()
const maintenanceStore = useMaintenanceStore()

const channels = ref({ r: 60, g: 40, b: 100, w: 80 })
const channelColors = { r: '#ff4444', g: '#44ff88', b: '#4488ff', w: '#ffffaa' }
const maintModalTask = ref(null)

const lightEntity = computed(() => {
  const dev = sensorsStore.devices.find(d => d.role === 'light')
  return dev?.entity_id
})
const lightOn = computed(() => {
  const dev = sensorsStore.devices.find(d => d.role === 'light')
  return dev?.state === 'on'
})
const nextFeeding = computed(() => Array.isArray(scheduleStore.feedings) ? scheduleStore.feedings.find(f => f.active) : undefined)
const lastFed = computed(() => scheduleStore.feedingHistory[0])
const recentFeedings = computed(() => scheduleStore.feedingHistory.slice(0, 3))

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function supplyPct(current, dose) {
  // show % of a rough "bottle" (assume 500ml default)
  return Math.min(100, (current / 500) * 100)
}
function supplyClass(current, unit) {
  if (current <= 50 && unit === 'ml') return 'danger'
  if (current <= 100 && unit === 'ml') return 'warn'
  return ''
}

function dueLabel(task) {
  const { t } = useI18n()
  if (task.days_until === null) return t('common.never')
  if (task.days_until < 0) return t('maintenance.overdue', { days: Math.abs(task.days_until) })
  if (task.days_until === 0) return t('maintenance.dueToday')
  return t('maintenance.due', { days: task.days_until })
}
function dueBadgeColor(days) {
  if (days === null) return 'var(--text-muted)'
  if (days < 0) return 'var(--danger)'
  if (days <= 3) return 'var(--warn)'
  return 'var(--ok)'
}
function dueProgressClass(days, interval) {
  if (days === null) return ''
  const pct = days / interval
  if (pct < 0.2) return 'danger'
  if (pct < 0.4) return 'warn'
  return ''
}
function dueProgressPct(days, interval) {
  if (days === null || days < 0) return 100
  return Math.min(100, ((interval - days) / interval) * 100)
}

async function pushChannels() {
  await sensorsStore.setFluvalChannels(channels.value.r, channels.value.g, channels.value.b, channels.value.w)
}

async function handleBleConnect() {
  try {
    await bleService.connect()
    sensorsStore.bleConnected = true
  } catch (err) {
    console.error('[nemo] BLE connect failed:', err)
  }
}

function openMaintModal(task) { maintModalTask.value = task }
async function onMaintDone(taskId, partsReplaced, notes) {
  await maintenanceStore.completeTask(taskId, partsReplaced, notes)
  maintModalTask.value = null
}

async function handleFeedNow() {
  await scheduleStore.feedNow()
}

onMounted(async () => {
  await Promise.all([
    scheduleStore.fetchFeedings(),
    scheduleStore.fetchHistory(),
    scheduleStore.fetchDosing(),
    sensorsStore.fetchDevices(),
    maintenanceStore.fetchTasks(),
  ])
})
</script>
