<template>
  <div class="tile">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
          <path d="M5 19c2-6 6-9 10-10"/>
        </svg>
        {{ locale === 'pl' ? 'ZDROWIE ROŚLIN' : 'PLANT HEALTH' }}
      </h2>
    </div>
    <hr class="divider">
    <div class="tile-body" style="padding-top:8px">
      <!-- Tank 1 left / Tank 2 right, consistent with the Oba combined view -->
      <div class="row2">
        <div v-for="tid in sortedTankIds" :key="tid">
          <div class="sec-lab">{{ tankName(tid) }}</div>
          <div v-if="plantsFor(tid).length === 0" class="empty" style="padding:20px 8px">
            <span class="muted" style="font-size:12px">{{ locale === 'pl' ? 'Brak roślin' : 'No plants' }}</span>
          </div>
          <div
            v-for="p in plantsFor(tid)"
            :key="p.id"
            class="ls-card"
            @click="openHealthModal(p)"
          >
            <div class="ls-thumb">
              <img v-if="p.img" :src="p.img" style="width:100%;height:100%;object-fit:cover">
              <div v-else class="ph">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
                  <path d="M5 19c2-6 6-9 10-10"/>
                </svg>
              </div>
            </div>
            <div class="ls-meta">
              <div class="name">
                <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                  {{ locale === 'pl' && p.name_pl ? p.name_pl : p.name_en }}
                </span>
                <span v-if="pendingCountFor(p.id) > 0" class="task-badge b-overdue">{{ pendingCountFor(p.id) }}</span>
                <span v-else class="pill in_tank" style="cursor:default">{{ locale === 'pl' ? 'OK' : 'OK' }}</span>
              </div>
              <span class="sp">{{ p.latin }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Plant health modal (full-screen) ───────────────────────── -->
  <Teleport to="body">
    <div
      v-if="healthModal"
      class="backdrop"
      style="position:fixed;align-items:stretch;justify-content:center"
      @click.self="closeHealthModal"
    >
      <div class="modal full" @click.stop>
        <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
          <button class="btn icon-btn btn-ghost" @click="closeHealthModal">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">
            {{ locale === 'pl' ? 'Zdrowie' : 'Health' }} · {{ healthModal ? (locale === 'pl' && healthModal.plant.name_pl ? healthModal.plant.name_pl : healthModal.plant.name_en) : '' }}
          </span>
          <label class="btn btn-sm btn-accent" style="cursor:pointer">
            {{ phStore.scanning ? (locale === 'pl' ? 'Skanuję…' : 'Scanning…') : (locale === 'pl' ? 'Skanuj' : 'Scan') }}
            <input type="file" accept="image/*" capture="environment" style="display:none" :disabled="phStore.scanning" @change="onScanFile">
          </label>
        </div>

        <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
          <!-- Diagram: two clickable growth zones -->
          <div class="sec-lab">{{ locale === 'pl' ? 'Zaznacz objaw' : 'Log a symptom' }}</div>
          <div class="ph-diagram">
            <div class="ph-zone" :class="{ on: pickerStage === 'new_growth' }" @click="togglePickerStage('new_growth')">
              {{ locale === 'pl' ? 'Nowe przyrosty' : 'New growth' }}
            </div>
            <div class="ph-stem"/>
            <div class="ph-zone" :class="{ on: pickerStage === 'old_growth' }" @click="togglePickerStage('old_growth')">
              {{ locale === 'pl' ? 'Stare liście' : 'Old leaves' }}
            </div>
          </div>

          <div v-if="pickerStage" style="margin-top:12px;display:flex;flex-direction:column;gap:8px">
            <button
              v-for="d in deficienciesForStage(pickerStage)"
              :key="d.key"
              class="ls-card"
              style="flex-direction:column;align-items:flex-start;gap:2px;padding:10px 12px;width:100%"
              @click="pickDeficiency(d)"
            >
              <span style="font-weight:600;font-size:13px">{{ locale === 'pl' ? d.name_pl : d.name_en }}</span>
              <span class="muted" style="font-size:11px">{{ locale === 'pl' ? d.symptom_pl : d.symptom_en }}</span>
            </button>
          </div>

          <!-- Active issues -->
          <div class="sec-lab" style="padding-top:16px">{{ locale === 'pl' ? 'Aktywne problemy' : 'Active issues' }}</div>
          <div v-if="!pendingEventsForPlant.length" class="muted" style="font-size:12px;padding:8px 0">
            {{ locale === 'pl' ? 'Brak' : 'None' }}
          </div>
          <div v-for="e in pendingEventsForPlant" :key="e.id" class="ls-card" style="flex-direction:column;align-items:stretch;gap:6px;padding:10px 12px">
            <div class="spread">
              <span style="font-weight:600;font-size:13px">{{ deficiencyName(e.deficiency_key) }}</span>
              <span class="pill" style="cursor:default">
                {{ e.source === 'ai_scan' ? (locale === 'pl' ? 'Skan AI' : 'AI scan') : (locale === 'pl' ? 'Ręcznie' : 'Manual') }}
              </span>
            </div>
            <span v-if="e.confidence != null" class="muted" style="font-size:11px">
              {{ locale === 'pl' ? 'Pewność' : 'Confidence' }}: {{ Math.round(e.confidence * 100) }}%
            </span>
            <span class="muted" style="font-size:11px">{{ formatDate(e.detected_at) }}</span>
            <div class="row" style="gap:8px;margin-top:4px">
              <button class="btn btn-sm btn-accent" @click="phStore.treatEvent(e.id)">
                {{ locale === 'pl' ? 'Oznacz jako leczone' : 'Mark treated' }}
              </button>
              <button class="btn btn-sm btn-ghost" @click="openCorrect(e)">
                {{ locale === 'pl' ? 'Popraw' : 'Correct' }}
              </button>
            </div>
            <div v-if="correctingEventId === e.id" style="display:flex;flex-direction:column;gap:4px;margin-top:4px">
              <button
                v-for="d in phStore.deficiencies"
                :key="d.key"
                class="btn btn-ghost"
                style="justify-content:flex-start;font-size:12px"
                @click="correctWith(e, d)"
              >
                {{ locale === 'pl' ? d.name_pl : d.name_en }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useObsadaStore } from '../stores/obsada'
import { usePlantHealthStore } from '../stores/plantHealth'
import { useTankSelectorStore } from '../stores/tankSelector'

const { locale } = useI18n()
const obsadaStore = useObsadaStore()
const phStore = usePlantHealthStore()
const tankStore = useTankSelectorStore()

const sortedTankIds = computed(() => tankStore.tanks.map(t => t.id).sort((a, b) => a - b))

function tankName(tid) {
  return tankStore.tanks.find(t => t.id === tid)?.name ?? ''
}

function plantsFor(tid) {
  return obsadaStore.plants.filter(p => (p.tank_id ?? 1) === tid)
}

function pendingCountFor(plantId) {
  return phStore.events.filter(e => e.plant_id === plantId && e.status === 'pending').length
}

function formatDate(s) {
  if (!s) return '—'
  return new Date(s).toLocaleDateString('pl-PL', {
    year: 'numeric', month: '2-digit', day: '2-digit',
  })
}

onMounted(() => {
  obsadaStore.fetchPlants()
  phStore.fetchDeficiencies()
  phStore.fetchEvents()
})

// ── Plant health modal ────────────────────────────────────────
const healthModal = ref(null)        // null | { plant }
const pickerStage = ref(null)        // null | 'new_growth' | 'old_growth'
const correctingEventId = ref(null)

function openHealthModal(plant) {
  healthModal.value = { plant }
  pickerStage.value = null
  correctingEventId.value = null
}

function closeHealthModal() {
  healthModal.value = null
}

function togglePickerStage(stage) {
  pickerStage.value = pickerStage.value === stage ? null : stage
  correctingEventId.value = null
}

function deficienciesForStage(stage) {
  return phStore.deficiencies.filter(d => d.growth_stage === stage)
}

function deficiencyName(key) {
  const d = phStore.deficiencies.find(d => d.key === key)
  if (!d) return key
  return locale.value === 'pl' ? d.name_pl : d.name_en
}

async function pickDeficiency(d) {
  if (!healthModal.value) return
  await phStore.logEvent(healthModal.value.plant.id, d.key)
  pickerStage.value = null
}

function openCorrect(e) {
  correctingEventId.value = correctingEventId.value === e.id ? null : e.id
  pickerStage.value = null
}

async function correctWith(e, d) {
  await phStore.correctEvent(e.id, d.key)
  correctingEventId.value = null
}

// pendingEvents used to be global (single-plant modal already implied it) -
// now scoped explicitly to the open plant since the list view shows all tanks.
const pendingEventsForPlant = computed(() =>
  phStore.events.filter(e => e.status === 'pending' && e.plant_id === healthModal.value?.plant.id)
)

async function onScanFile(ev) {
  const file = ev.target.files?.[0]
  if (!file || !healthModal.value) return
  await phStore.scanLeaf(healthModal.value.plant.id, file)
  ev.target.value = ''
}
</script>

<style scoped>
.ph-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 0;
}
.ph-zone {
  width: 100%;
  text-align: center;
  padding: 14px 12px;
  border-radius: 10px;
  border: 1.5px solid var(--border);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.ph-zone.on {
  border-color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
}
.ph-stem {
  width: 3px;
  height: 20px;
  background: var(--border);
}
</style>
