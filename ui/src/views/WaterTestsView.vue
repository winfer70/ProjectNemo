<template>
  <div>
    <!-- Main tile -->
    <div class="tile">
      <div class="tile-hd">
        <h2>TESTY WODY</h2>
        <button class="btn btn-sm btn-accent" @click="openScanModal">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 8.5a2 2 0 0 1 2-2h2l1.5-2h7L17 6.5h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-9z" />
            <circle cx="12" cy="12.5" r="3.5" />
          </svg>
          Skanuj
        </button>
      </div>
      <hr class="divider" />

      <!-- Empty state -->
      <div v-if="latestReadings.length === 0" class="empty" style="padding:34px 16px">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 3h6" />
          <path d="M10 3v6L5 18a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3" />
          <path d="M7.5 14h9" />
        </svg>
        <span>Brak testów — dodaj pierwszy wynik</span>
        <button class="btn btn-sm btn-accent" @click="openScanModal">Skanuj</button>
      </div>

      <!-- Test table -->
      <template v-else>
        <div class="tile-body" style="padding-top:12px;padding-bottom:8px">
          <span class="muted" style="font-size:13px">
            Ostatni test: <b style="color:var(--text)">{{ lastTestDays }} dni temu</b>
          </span>
        </div>

        <div class="tile-body ptable" style="padding-top:0">
          <!-- Header row -->
          <div class="prow" style="padding-bottom:6px">
            <span class="sec-lab" style="padding:0">Parametr</span>
            <span class="sec-lab" style="padding:0;text-align:right">Wartość</span>
            <span class="sec-lab" style="padding:0;text-align:center">Status</span>
            <span class="sec-lab" style="padding:0;text-align:center">Trend</span>
          </div>

          <!-- Data rows -->
          <div v-for="p in latestReadings" :key="p.parameter_key" class="prow">
            <span class="pp">{{ p.name_pl }}</span>
            <span class="pv">{{ p.value }}{{ p.unit ? ' ' + p.unit : '' }}</span>
            <span class="ps" :style="{ color: statusColor(p), justifyContent: 'center' }">
              <svg v-if="!p.out_of_range" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 12.5l5 5 11-12" />
              </svg>
              <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 4l9 15H3l9-15z" />
                <path d="M12 10v4" />
                <circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none" />
              </svg>
              {{ statusText(p) }}
            </span>
            <span class="pt">
              <span
                :style="{
                  color: p.trend === 'up' ? 'var(--warning)' : p.trend === 'down' ? 'var(--accent)' : 'var(--text-muted)',
                  display: 'inline-flex'
                }"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <template v-if="p.trend === 'up'">
                    <path d="M6 18L18 6" />
                    <path d="M9 6h9v9" />
                  </template>
                  <template v-else-if="p.trend === 'down'">
                    <path d="M6 6l12 12" />
                    <path d="M18 9v9H9" />
                  </template>
                  <template v-else>
                    <path d="M5 12h13" />
                    <path d="M13 6l6 6-6 6" />
                  </template>
                </svg>
              </span>
            </span>
          </div>
        </div>

        <hr class="divider" />

        <div class="tile-body" style="padding-top:14px">
          <div class="row" style="gap:10px">
            <button class="btn btn-block">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 3-6.7" />
                <path d="M3 4v4h4" />
                <path d="M12 8v4l3 2" />
              </svg>
              Historia
            </button>
            <button class="btn btn-block">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12h3.5l2-6 4 12 2.5-6H21" />
              </svg>
              Cykl zbiornika
            </button>
          </div>
        </div>
      </template>
    </div>

    <!-- Scan modal -->
    <div
      v-if="scanModal"
      class="backdrop"
      style="align-items:stretch;justify-content:center"
      @click.self="closeScanModal"
    >
      <div class="modal full" @click.stop>
        <!-- Modal header -->
        <div
          class="spread"
          style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0"
        >
          <button class="btn icon-btn btn-ghost" @click="closeScanModal">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12" />
              <path d="M18 6L6 18" />
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">Skanuj</span>
          <span style="width:32px" />
        </div>

        <!-- Modal body -->
        <div style="padding:16px;overflow-y:auto;flex:1">

          <!-- Camera + detecting phase -->
          <template v-if="scanPhase !== 'confirm'">
            <input type="file" accept="image/*" capture="environment" ref="fileInputRef" style="display:none" @change="handleFile">
            <div
              style="aspect-ratio:3/4;border-radius:14px;overflow:hidden;position:relative;border:1px solid var(--border);cursor:pointer"
              @click="fileInputRef?.click()"
            >
              <div class="ph" style="position:absolute;inset:0">podgląd kamery</div>
              <div
                style="position:absolute;inset:18% 12%;border:2px dashed rgba(255,255,255,0.4);border-radius:10px"
              />
              <div
                v-if="scanPhase === 'detecting'"
                style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(0,0,0,0.45)"
              >
                <span style="color:var(--accent)" class="spin">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 12a8 8 0 1 1-2.3-5.6" />
                    <path d="M20 4v4h-4" />
                  </svg>
                </span>
                <span style="font-size:13px;font-weight:600">Wykrywanie pasków…</span>
              </div>
            </div>

            <p class="muted" style="font-size:12.5px;text-align:center;margin:14px 0 18px">
              Umieść pasek testowy w ramce. CV dopasuje kolory, AI uzupełni braki.
            </p>

            <button
              class="btn btn-block btn-ghost"
              style="margin-bottom:10px"
              @click="() => { const vals = {}; manualParams.forEach(p => { vals[p.id] = '' }); detectedValues.value = vals; scanPhase.value = 'confirm' }"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 6h20v12H2z"/><path d="M6 10h.01"/><path d="M10 10h.01"/><path d="M14 10h.01"/><path d="M18 10h.01"/><path d="M8 14h8"/>
              </svg>
              Wpisz ręcznie
            </button>

            <button
              class="btn btn-accent btn-block btn-lg"
              :disabled="scanPhase === 'detecting'"
              @click="startCapture"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 8.5a2 2 0 0 1 2-2h2l1.5-2h7L17 6.5h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-9z" />
                <circle cx="12" cy="12.5" r="3.5" />
              </svg>
              {{ scanPhase === 'detecting' ? 'Analizowanie…' : 'Zrób zdjęcie' }}
            </button>
          </template>

          <!-- Confirm phase -->
          <template v-else>
            <div
              class="banner"
              style="background:var(--success-12);color:var(--success);margin-bottom:16px;border:1px solid rgba(63,185,80,0.3)"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="9" />
                <path d="M8 12.2l2.6 2.6L16 9" />
              </svg>
              <span>Wykryto parametry — potwierdź wartości</span>
            </div>

            <div v-for="p in manualParams" :key="p.id" class="kv">
              <span class="k" style="color:var(--text);font-weight:600">{{ p.name_pl }}</span>
              <span class="v row" style="gap:8px">
                <input
                  class="input"
                  v-model="detectedValues[p.id]"
                  type="number"
                  step="0.01"
                  style="width:76px;padding:6px 10px;text-align:right"
                />
                <span class="muted" style="min-width:30px;font-size:12px">{{ p.unit }}</span>
              </span>
            </div>

            <button
              class="btn btn-success btn-block btn-lg"
              style="margin-top:18px"
              :disabled="saving"
              @click="saveScan"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 12.5l5 5 11-12" />
              </svg>
              {{ saving ? 'Zapisywanie…' : 'Zapisz' }}
            </button>
          </template>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const sessions = ref([])
const parameters = ref([])

onMounted(async () => {
  const [sessR, paramR] = await Promise.all([
    axios.get('/api/water-tests/sessions'),
    axios.get('/api/water-tests/parameters'),
  ])
  sessions.value = sessR.data
  parameters.value = paramR.data
})

const latestSession = computed(() => sessions.value[0] ?? null)

const latestReadings = computed(() => {
  if (!latestSession.value) return []
  return latestSession.value.readings.map((r) => {
    const param = parameters.value.find((p) => p.id === r.parameter_id)
    return {
      ...r,
      name_pl: param?.name_pl ?? param?.name_en ?? r.parameter_id,
      name_en: param?.name_en,
      unit: param?.unit ?? '',
      trend: 'flat',
      parameter_key: param?.key,
    }
  })
})

const lastTestDays = computed(() => {
  if (!latestSession.value) return 0
  return Math.floor((Date.now() - new Date(latestSession.value.tested_at)) / 86400000)
})

const manualParams = computed(() =>
  parameters.value.filter((p) => p.category === 'manual')
)

const statusColor = (p) => {
  if (p.out_of_range) return 'var(--warning)'
  return 'var(--success)'
}

const statusText = (p) => (p.out_of_range ? 'Wysoko' : 'OK')

// Scan modal state
const scanModal = ref(false)
const scanPhase = ref('camera')
const detectedValues = ref({})
const saving = ref(false)
const fileInputRef = ref(null)
let scanTimeout = null

function openScanModal() {
  scanPhase.value = 'camera'
  detectedValues.value = {}
  scanModal.value = true
}

function closeScanModal() {
  clearTimeout(scanTimeout)
  scanModal.value = false
  scanPhase.value = 'camera'
  detectedValues.value = {}
}

function startCapture() {
  scanPhase.value = 'detecting'
  scanTimeout = setTimeout(() => {
    const vals = {}
    manualParams.value.forEach((p) => {
      vals[p.id] = ''
    })
    detectedValues.value = vals
    scanPhase.value = 'confirm'
  }, 1600)
}

async function saveScan() {
  const readings = Object.entries(detectedValues.value)
    .filter(([, v]) => v !== '' && v !== null && v !== undefined)
    .map(([id, value]) => ({ parameter_id: parseInt(id), value: parseFloat(value) }))
    .filter((r) => !isNaN(r.value))

  if (readings.length === 0) {
    closeScanModal()
    return
  }

  saving.value = true
  try {
    await axios.post('/api/water-tests/sessions', { readings })
    const sessR = await axios.get('/api/water-tests/sessions')
    sessions.value = sessR.data
  } finally {
    saving.value = false
    closeScanModal()
  }
}
</script>
