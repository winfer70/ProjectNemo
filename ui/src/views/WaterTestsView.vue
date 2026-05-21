<template>
  <div>
    <!-- Cycling banners -->
    <div v-if="waterTestsStore.isCycled()" class="banner banner-ok">
      🐟 {{ $t('tests.cycled') }}
    </div>
    <div v-if="nh3High" class="banner banner-danger">
      ⚠️ {{ $t('tests.waterChangeRecommended') }}
    </div>

    <!-- Header row -->
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
      <div style="font-size:12px;color:var(--text-muted);">
        <span v-if="waterTestsStore.latestSession">
          {{ $t('tests.lastTest', { days: daysSinceLastTest }) }}
        </span>
        <span v-else>{{ $t('tests.noTests') }}</span>
      </div>
      <button class="btn btn-primary btn-sm" @click="showForm = true">
        + {{ $t('tests.newSession') }}
      </button>
    </div>

    <!-- Latest values grid -->
    <div class="card">
      <div class="card-title">{{ $t('tests.title') }}</div>
      <div class="test-grid">
        <div v-for="param in manualParams" :key="param.key"
             class="test-param"
             :class="{ 'out-of-range': latestReading(param.key)?.out_of_range }">
          <div class="test-param-name">
            {{ locale === 'pl' ? param.name_pl : param.name_en }}
          </div>
          <div class="test-param-value">
            {{ latestReading(param.key)?.value ?? '—' }}
          </div>
          <div class="test-param-unit">{{ param.unit }}</div>
          <div class="test-param-age" v-if="waterTestsStore.latestSession">
            {{ daysSinceLastTest }}d
          </div>
          <span class="badge" :class="latestReading(param.key)?.out_of_range ? 'badge-danger' : 'badge-ok'"
                style="margin-top:4px;">
            {{ latestReading(param.key)?.out_of_range ? $t('tests.outOfRange') : $t('tests.ok') }}
          </span>
        </div>
      </div>
    </div>

    <!-- Session history -->
    <div class="card" v-if="waterTestsStore.sessions.length">
      <div class="card-title">{{ $t('tests.history') }}</div>
      <div v-for="session in waterTestsStore.sessions.slice(0,5)" :key="session.id"
           style="border-bottom:1px solid var(--border);padding:8px 0;font-size:12px;">
        <div style="display:flex;justify-content:space-between;">
          <span>{{ formatDate(session.tested_at) }}</span>
          <span v-if="session.readings.some(r => r.out_of_range)"
                class="badge badge-danger">{{ $t('tests.outOfRange') }}</span>
          <span v-else class="badge badge-ok">{{ $t('tests.ok') }}</span>
        </div>
        <div v-if="session.notes" style="color:var(--text-muted);margin-top:2px;">
          {{ session.notes }}
        </div>
      </div>
    </div>

    <!-- New test session modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal-sheet">
        <div class="modal-title">{{ $t('tests.newSession') }}</div>
        <div v-for="param in manualParams" :key="param.key" style="margin-bottom:12px;">
          <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:4px;">
            {{ locale === 'pl' ? param.name_pl : param.name_en }} ({{ param.unit }})
          </label>
          <input
            type="number"
            step="0.01"
            v-model.number="formValues[param.id]"
            style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);padding:8px;font-size:14px;"
            :placeholder="paramRange(param)"
          />
        </div>
        <div style="margin-bottom:12px;">
          <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:4px;">
            {{ $t('tests.sessionNotes') }}
          </label>
          <textarea v-model="formNotes"
            style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);padding:8px;font-size:13px;height:60px;resize:none;">
          </textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" style="flex:1" @click="showForm = false">
            {{ $t('tests.cancel') }}
          </button>
          <button class="btn btn-primary" style="flex:1" @click="submitSession">
            {{ $t('tests.save') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWaterTestsStore } from '../stores/waterTests'

const { locale } = useI18n()
const waterTestsStore = useWaterTestsStore()

const showForm = ref(false)
const formValues = ref({})
const formNotes = ref('')

const manualParams = computed(() =>
  waterTestsStore.parameters.filter(p => p.category === 'manual')
)

const daysSinceLastTest = computed(() => {
  if (!waterTestsStore.latestSession) return null
  const diff = Date.now() - new Date(waterTestsStore.latestSession.tested_at).getTime()
  return Math.floor(diff / 86400000)
})

const nh3High = computed(() => {
  const r = latestReading('ammonia')
  return r && r.value > 0.25
})

function latestReading(paramKey) {
  if (!waterTestsStore.latestSession) return null
  return waterTestsStore.latestSession.readings.find(r => r.parameter_key === paramKey)
}

function paramRange(param) {
  const parts = []
  if (param.min_safe !== null) parts.push(`min ${param.min_safe}`)
  if (param.max_safe !== null) parts.push(`max ${param.max_safe}`)
  return parts.join(' / ') || ''
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString(locale.value === 'pl' ? 'pl-PL' : 'en-IE')
}

async function submitSession() {
  const readings = Object.entries(formValues.value)
    .filter(([, v]) => v !== null && v !== undefined && v !== '')
    .map(([id, value]) => ({ parameter_id: parseInt(id), value }))

  if (readings.length === 0) return

  await waterTestsStore.createSession(null, formNotes.value || null, readings)
  formValues.value = {}
  formNotes.value = ''
  showForm.value = false
}

onMounted(async () => {
  await Promise.all([
    waterTestsStore.fetchParameters(),
    waterTestsStore.fetchLatest(),
    waterTestsStore.fetchSessions(),
  ])
})
</script>
