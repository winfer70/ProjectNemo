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
          <div style="font-size:10px;color:var(--text-muted);margin-top:2px;">({{ readTime(param.key) }})</div>
          <details v-if="latestReading(param.key)?.out_of_range"
                   style="margin-top:6px;border:1px solid #f59e0b;border-radius:6px;padding:6px 8px;">
            <summary style="font-size:11px;cursor:pointer;color:#f59e0b;font-weight:600;">
              {{ $t('tests.advice') }}
            </summary>
            <div style="font-size:12px;margin-top:6px;line-height:1.5;color:var(--text);">
              {{ getRemediation(param, latestReading(param.key)) }}
            </div>
          </details>
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

        <!-- Strip scan buttons -->
        <div style="margin-bottom:14px;">
          <input ref="fileInput" type="file" accept="image/*"
                 style="display:none" @change="handleFileSelected" />
          <input ref="fileInputAmmonia" type="file" accept="image/*"
                 style="display:none" @change="handleAmmoniaFileSelected" />
          <button class="btn btn-secondary" style="width:100%;position:relative;"
                  :disabled="scanning" @click="fileInput.click()">
            <span v-if="scanning">⏳ {{ $t('tests.scanning') }}</span>
            <span v-else>📷 {{ $t('tests.scanStrip') }}</span>
          </button>
          <button class="btn btn-secondary" style="width:100%;position:relative;margin-top:6px;"
                  :disabled="scanningAmmonia" @click="fileInputAmmonia.click()">
            <span v-if="scanningAmmonia">⏳ {{ $t('tests.scanningAmmonia') }}</span>
            <span v-else>🟢 {{ $t('tests.scanAmmonia') }}</span>
          </button>
          <div v-if="scanError" style="font-size:11px;color:var(--danger);margin-top:4px;">{{ scanError }}</div>
          <div v-if="scannedKeys.size" style="font-size:11px;color:var(--ok);margin-top:4px;">
            ✓ {{ $t('tests.scanFilled', { n: scannedKeys.size }) }}
          </div>
          <div v-if="ammoniaScanned" style="font-size:11px;color:var(--ok);margin-top:2px;">
            ✓ {{ $t('tests.scanAmmoniaFilled') }}
          </div>
        </div>

        <div v-for="param in manualParams" :key="param.key" style="margin-bottom:12px;">
          <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:4px;">
            {{ locale === 'pl' ? param.name_pl : param.name_en }} ({{ param.unit }})
            <span v-if="scannedKeys.has(param.id) && scanOutOfRange[param.id]"
                  style="color:var(--danger);font-size:10px;margin-left:4px;">⚠ high</span>
            <span v-else-if="scannedKeys.has(param.id)"
                  style="color:var(--ok);font-size:10px;margin-left:4px;">✓ scanned</span>
          </label>
          <input
            type="number"
            step="0.01"
            v-model.number="formValues[param.id]"
            :style="`width:100%;background:var(--bg);border:1px solid ${scanOutOfRange[param.id] ? 'var(--danger)' : scannedKeys.has(param.id) ? 'var(--ok)' : 'var(--border)'};border-radius:6px;color:var(--text);padding:8px;font-size:14px;`"
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

const REMEDIATION = {
  ph: {
    high: 'pH > 7.8: Do 30% water change. Add driftwood or peat to filter for natural tannins. Reduce aeration temporarily.',
    low: 'pH < 7.2: Do 30% water change with tap water (Meath pH ~7.6). Check KH — low KH causes pH swings.',
    high_pl: 'pH > 7.8: Podmień 30% wody. Dodaj korzeń lub torf do filtra. Ogranicz napowietrzanie.',
    low_pl: 'pH < 7.2: Podmień 30% wody kranową (Meath pH ~7.6). Sprawdź KH — niski KH powoduje wahania pH.',
  },
  nitrate: {
    high: 'NO3 > 30 ppm: Do 30–50% water change. Reduce feeding. More plants absorb nitrates. Vacuum substrate.',
    high_pl: 'NO3 > 30 ppm: Podmień 30–50% wody. Zmniejsz karmienie. Więcej roślin pochłania azotany. Wysyfonuj dno.',
  },
  nitrite: {
    high: 'NO2 > 0: URGENT — add 5 ml Seachem Prime directly to tank (neutralises NO2 for 24–48h). Dose 25 ml Stability. Do 30% water change. Increase aeration to max.',
    high_pl: 'NO2 > 0: PILNE — dodaj 5 ml Seachem Prime bezpośrednio do akwarium. Dodaj 25 ml Stability. Podmień 30% wody. Napowietrzanie na max.',
  },
  ammonia: {
    high: 'NH3 > 0: URGENT — add 5 ml Seachem Prime. Do 30% water change immediately. Stop feeding for 48h. Dose 25 ml Stability daily until ammonia = 0.',
    high_pl: 'NH3 > 0: PILNE — dodaj 5 ml Seachem Prime. Natychmiast podmień 30% wody. Nie karm przez 48h. Dodawaj 25 ml Stability codziennie aż amoniak = 0.',
  },
  free_chlorine: {
    high: 'Chlorine > 0: Always add Seachem Prime to new water before adding to tank. If already in tank, add 5 ml Prime now.',
    high_pl: 'Chlor > 0: Zawsze dodawaj Seachem Prime do nowej wody przed wlaniem do akwarium. Jeśli już w zbiorniku, dodaj 5 ml Prime.',
  },
  copper: {
    high: 'Cu > 0.2 ppm: Dangerous for shrimp and invertebrates. Do 50% water change immediately. Check for copper pipes or copper-containing products.',
    high_pl: 'Cu > 0.2 ppm: Niebezpieczne dla krewetek. Natychmiast podmień 50% wody. Sprawdź miedziane rury lub produkty zawierające miedź.',
  },
  kh: {
    low: 'KH < 40 ppm: pH will be unstable. Add crushed coral to filter or use KH buffer. Do not change drastically.',
    high: 'KH > 180 ppm: Partial water change with softer water. For Meath tap water this is normal — County Meath KH is 120–180 ppm.',
    low_pl: 'KH < 40 ppm: pH będzie niestabilne. Dodaj pokruszony koral do filtra lub bufor KH.',
    high_pl: 'KH > 180 ppm: Podmień część wody miękkiejszą wodą. Dla wody z Meath to normalne — KH 120–180 ppm.',
  },
  gh: {
    low: 'GH < 125 ppm: Add mineral supplements (GH booster). Fish may show stress.',
    high: 'GH > 250 ppm: Partial water change with RO or rainwater to dilute.',
    low_pl: 'GH < 125 ppm: Dodaj minerały (GH booster). Ryby mogą być zestresowane.',
    high_pl: 'GH > 250 ppm: Podmień część wody z wodą RO lub deszczówką.',
  },
  total_alkalinity: {
    low: 'TAL < 80 ppm: pH buffering capacity is low. Add alkalinity buffer or crushed coral.',
    high: 'TAL > 180 ppm: Partial water change. Add peat to filter.',
    low_pl: 'TAL < 80 ppm: Niska zdolność buforowania pH. Dodaj bufor zasadowości lub koral.',
    high_pl: 'TAL > 180 ppm: Podmień część wody. Dodaj torf do filtra.',
  },
}

const READ_TIME = { ammonia: '3 min' }

function readTime(key) {
  return READ_TIME[key] || '30s'
}

function getRemediation(param, reading) {
  if (!reading?.out_of_range) return null
  const rem = REMEDIATION[param.key]
  if (!rem) return null
  const isHigh = param.max_safe !== null && reading.value > param.max_safe
  const isLow = param.min_safe !== null && reading.value < param.min_safe
  const lang = locale.value === 'pl' ? '_pl' : ''
  if (isHigh) return rem[`high${lang}`] ?? rem.high ?? null
  if (isLow) return rem[`low${lang}`] ?? rem.low ?? null
  return null
}

const showForm = ref(false)
const formValues = ref({})
const formNotes = ref('')
const fileInput = ref(null)
const fileInputAmmonia = ref(null)
const scanning = ref(false)
const scanningAmmonia = ref(false)
const scanError = ref('')
const scannedKeys = ref(new Set())
const ammoniaScanned = ref(false)
const scanCacheId = ref(null)
const scanOutOfRange = ref({})

async function handleFileSelected(event) {
  const file = event.target.files?.[0]
  if (!file) return
  scanning.value = true
  scanError.value = ''
  scannedKeys.value = new Set()
  scanCacheId.value = null
  scanOutOfRange.value = {}
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch('/api/water-tests/analyze_strip', { method: 'POST', body: fd })
    if (!res.ok) {
      let detail = res.status
      try { detail = (await res.json()).detail ?? res.status } catch {}
      throw new Error(String(detail))
    }
    const { prefill, cache_id, out_of_range, cache_hit } = await res.json()
    scanCacheId.value = cache_id
    if (cache_hit) scanError.value = ''
    scanOutOfRange.value = out_of_range || {}
    const ammoniaId = manualParams.value.find(p => p.key === 'ammonia')?.id
    for (const [id, value] of Object.entries(prefill)) {
      const numId = parseInt(id)
      if (numId === ammoniaId) continue  // ammonia needs 3-min scan
      formValues.value[numId] = value
      scannedKeys.value.add(numId)
    }
  } catch (e) {
    scanError.value = `Scan failed: ${e.message}`
  } finally {
    scanning.value = false
    event.target.value = ''
  }
}

async function handleAmmoniaFileSelected(event) {
  const file = event.target.files?.[0]
  if (!file) return
  scanningAmmonia.value = true
  scanError.value = ''
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch('/api/water-tests/analyze_strip', { method: 'POST', body: fd })
    if (!res.ok) {
      let detail = res.status
      try { detail = (await res.json()).detail ?? res.status } catch {}
      throw new Error(String(detail))
    }
    const { prefill, out_of_range } = await res.json()
    const ammoniaId = manualParams.value.find(p => p.key === 'ammonia')?.id
    if (ammoniaId !== undefined && prefill[ammoniaId] !== undefined) {
      formValues.value[ammoniaId] = prefill[ammoniaId]
      scannedKeys.value = new Set([...scannedKeys.value, ammoniaId])
      if (out_of_range?.[ammoniaId] !== undefined) {
        scanOutOfRange.value = { ...scanOutOfRange.value, [ammoniaId]: out_of_range[ammoniaId] }
      }
      ammoniaScanned.value = true
    } else {
      scanError.value = 'Ammonia not detected in photo'
    }
  } catch (e) {
    scanError.value = `Ammonia scan failed: ${e.message}`
  } finally {
    scanningAmmonia.value = false
    event.target.value = ''
  }
}

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

  await waterTestsStore.createSession(null, formNotes.value || null, readings, scanCacheId.value)
  formValues.value = {}
  formNotes.value = ''
  scannedKeys.value = new Set()
  scanError.value = ''
  scanCacheId.value = null
  scanOutOfRange.value = {}
  ammoniaScanned.value = false
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
