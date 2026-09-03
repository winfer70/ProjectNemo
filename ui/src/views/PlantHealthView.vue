<template>
  <div class="tile" v-resizable="'planthealth.main'">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
          <path d="M5 19c2-6 6-9 10-10"/>
        </svg>
        {{ locale === 'pl' ? 'ZDROWIE ROŚLIN' : 'PLANT HEALTH' }}
      </h2>
      <label class="btn btn-sm btn-accent" style="cursor:pointer">
        {{ phStore.scanning ? (locale === 'pl' ? 'Skanuję…' : 'Scanning…') : (locale === 'pl' ? 'Skanuj' : 'Scan') }}
        <input type="file" accept="image/*" capture="environment" style="display:none" :disabled="phStore.scanning" @change="startScan">
      </label>
    </div>
    <hr class="divider">
    <div class="tile-body" style="padding-top:8px">
      <!-- Diagram: matches the Aquathusiast nutrient-deficiency chart -
           click a leaf to see its details, then log it against a plant. -->
      <div class="sec-lab">{{ locale === 'pl' ? 'Diagram niedoborów' : 'Deficiency diagram' }}</div>
      <svg viewBox="0 0 320 460" class="ph-svg" @click.self="selectedKey = null">
        <defs>
          <!-- nitrogen: old growth yellow fading to light green new growth -->
          <linearGradient id="nitrogenGrad" x1="0" y1="0" x2="78" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0" stop-color="#e8d94a"/>
            <stop offset="1" stop-color="#7fae52"/>
          </linearGradient>
        </defs>
        <path d="M140,438 L180,438 L172,458 L148,458 Z" fill="#2a2a2a"/>
        <line x1="160" y1="438" x2="160" y2="70" stroke="#3a6b2f" stroke-width="4" stroke-linecap="round"/>
        <line x1="20" y1="240" x2="300" y2="240" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="5,4"/>
        <text x="300" y="230" text-anchor="end" font-size="10" fill="var(--text-muted)" font-style="italic">{{ locale === 'pl' ? 'Nowe przyrosty' : 'New Growth' }}</text>
        <text x="300" y="253" text-anchor="end" font-size="10" fill="var(--text-muted)" font-style="italic">{{ locale === 'pl' ? 'Stare liście' : 'Old Growth' }}</text>

        <g
          v-for="leaf in DIAGRAM_LEAVES"
          :key="leaf.key"
          :transform="`translate(160,${leaf.y}) scale(${(leaf.side === 'left' ? -1 : 1) * (leaf.scale || 1)},${leaf.scale || 1})`"
          class="ph-leaf"
          :class="{ on: selectedKey === leaf.key }"
          @click="selectedKey = leaf.key"
        >
          <!-- base leaf shape, colored/textured per symptom so it's visible at a glance -->
          <path d="M0,0 Q18,-22 42,-19 Q68,-16 78,0 Q68,16 42,19 Q18,22 0,0 Z" :fill="leaf.color"/>
          <line x1="8" y1="0" x2="70" y2="0" stroke="rgba(0,0,0,0.25)" stroke-width="1"/>

          <template v-if="leaf.key === 'manganese'">
            <circle cx="30" cy="-8" r="3" fill="#274d29"/>
            <circle cx="50" cy="6" r="2.5" fill="#274d29"/>
            <circle cx="20" cy="10" r="2.5" fill="var(--bg)" stroke="#274d29" stroke-width="0.5"/>
            <circle cx="45" cy="-12" r="2" fill="var(--bg)" stroke="#274d29" stroke-width="0.5"/>
          </template>

          <template v-if="leaf.key === 'potassium'">
            <path d="M0,0 Q18,-22 42,-19 Q68,-16 78,0 Q68,16 42,19 Q18,22 0,0 Z" fill="none" stroke="#e0c94a" stroke-width="3"/>
            <circle cx="35" cy="-4" r="2" fill="var(--bg)" stroke="#e0c94a" stroke-width="0.5"/>
            <circle cx="55" cy="8" r="1.8" fill="var(--bg)" stroke="#e0c94a" stroke-width="0.5"/>
            <circle cx="25" cy="10" r="1.8" fill="var(--bg)" stroke="#e0c94a" stroke-width="0.5"/>
          </template>

          <template v-if="leaf.key === 'magnesium'">
            <line x1="20" y1="0" x2="10" y2="-10" stroke="#3f6b3a" stroke-width="1"/>
            <line x1="35" y1="0" x2="25" y2="-13" stroke="#3f6b3a" stroke-width="1"/>
            <line x1="50" y1="0" x2="42" y2="-12" stroke="#3f6b3a" stroke-width="1"/>
            <line x1="20" y1="0" x2="12" y2="10" stroke="#3f6b3a" stroke-width="1"/>
            <line x1="35" y1="0" x2="27" y2="13" stroke="#3f6b3a" stroke-width="1"/>
            <line x1="50" y1="0" x2="43" y2="12" stroke="#3f6b3a" stroke-width="1"/>
          </template>

          <template v-if="leaf.key === 'phosphate'">
            <ellipse cx="28" cy="-6" rx="7" ry="5" fill="#1f2a17" opacity="0.6"/>
            <ellipse cx="48" cy="8" rx="6" ry="4" fill="#1f2a17" opacity="0.6"/>
            <circle cx="18" cy="8" r="2.5" fill="var(--bg)" stroke="#1f2a17" stroke-width="0.5"/>
            <circle cx="60" cy="-6" r="2" fill="var(--bg)" stroke="#1f2a17" stroke-width="0.5"/>
          </template>
        </g>

        <text
          v-for="leaf in DIAGRAM_LEAVES"
          :key="'lbl-' + leaf.key"
          :x="leaf.side === 'left' ? 62 : 258"
          :y="leaf.y"
          text-anchor="middle"
          font-size="12"
          font-weight="600"
          :fill="selectedKey === leaf.key ? 'var(--accent)' : 'var(--text)'"
          style="cursor:pointer"
          @click="selectedKey = leaf.key"
        >{{ deficiencyName(leaf.key) }}</text>
      </svg>

      <!-- Active issues across both tanks -->
      <div class="sec-lab" style="padding-top:16px">{{ locale === 'pl' ? 'Aktywne problemy' : 'Active issues' }}</div>
      <div v-if="!pendingEvents.length" class="muted" style="font-size:12px;padding:8px 0">
        {{ locale === 'pl' ? 'Brak' : 'None' }}
      </div>
      <div v-for="e in pendingEvents" :key="e.id" class="ls-card" style="flex-direction:column;align-items:stretch;gap:6px;padding:10px 12px">
        <div class="spread">
          <span style="font-weight:600;font-size:13px">{{ deficiencyName(e.deficiency_key) }}</span>
          <span class="pill" style="cursor:default">
            {{ e.source === 'ai_scan' ? (locale === 'pl' ? 'Skan AI' : 'AI scan') : (locale === 'pl' ? 'Ręcznie' : 'Manual') }}
          </span>
        </div>
        <span class="muted" style="font-size:12px">{{ plantLabel(e.plant_id) }}</span>
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

  <!-- ── Leaf detail popup ───────────────────────────────────────
       Shown when a leaf on the diagram is clicked; easier to read than
       an inline card, especially on mobile. -->
  <Teleport to="body">
    <div
      v-if="selectedKey"
      class="backdrop"
      @click.self="selectedKey = null"
    >
      <div class="modal" style="max-width:440px;width:92vw;padding:24px;display:flex;flex-direction:column;gap:12px" @click.stop>
        <div class="spread">
          <span style="font-weight:700;font-size:20px;color:#fff">{{ deficiencyName(selectedKey) }}</span>
          <button class="btn icon-btn btn-ghost" @click="selectedKey = null">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
        </div>
        <span class="muted" style="font-size:15px">{{ deficiencySymptom(selectedKey) }}</span>
        <span class="muted" style="font-size:15px">{{ deficiencyTreatment(selectedKey) }}</span>
        <button class="btn btn-accent" style="margin-top:8px" @click="logSelected">
          {{ locale === 'pl' ? 'Zapisz dla rośliny' : 'Log for a plant' }}
        </button>
      </div>
    </div>
  </Teleport>

  <!-- ── Plant picker (full-screen) ──────────────────────────────
       Shown after either a manual diagram pick or a photo scan needs to
       know which plant it's for. -->
  <Teleport to="body">
    <div
      v-if="pendingAction"
      class="backdrop"
      style="position:fixed;align-items:stretch;justify-content:center"
      @click.self="pendingAction = null"
    >
      <div class="modal full" @click.stop>
        <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
          <button class="btn icon-btn btn-ghost" @click="pendingAction = null">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">{{ locale === 'pl' ? 'Która roślina?' : 'Which plant?' }}</span>
          <span style="width:34px"></span>
        </div>
        <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
          <div v-for="tid in sortedTankIds" :key="tid">
            <div class="sec-lab">{{ tankName(tid) }}</div>
            <div v-if="plantsFor(tid).length === 0" class="muted" style="font-size:12px;padding:8px 0">
              {{ locale === 'pl' ? 'Brak roślin' : 'No plants' }}
            </div>
            <div
              v-for="p in plantsFor(tid)"
              :key="p.id"
              class="ls-card"
              @click="choosePlantForAction(p)"
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
                </div>
                <span class="sp">{{ p.latin }}</span>
              </div>
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

function plantLabel(plantId) {
  const p = obsadaStore.plants.find(p => p.id === plantId)
  if (!p) return ''
  const name = locale.value === 'pl' && p.name_pl ? p.name_pl : p.name_en
  return `${name} · ${tankName(p.tank_id ?? 1)}`
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

// ── Diagram ────────────────────────────────────────────────────
// Matches the Aquathusiast "5 Min Guide: Freshwater Nutrient Deficiencies"
// chart - 4 new-growth leaves above the dashed line, 4 old-growth below.
// Each leaf's color/texture depicts its own symptom (spots, holes, veins,
// gradient, rim) rather than a flat swatch, so the problem reads at a glance.
const DIAGRAM_LEAVES = [
  { key: 'iron', side: 'left', y: 110, color: '#e8d94a' },
  { key: 'calcium', side: 'right', y: 110, color: '#dce9ba', scale: 0.72 },
  { key: 'manganese', side: 'left', y: 195, color: '#4f9153' },
  { key: 'nitrogen', side: 'right', y: 195, color: 'url(#nitrogenGrad)' },
  { key: 'potassium', side: 'left', y: 285, color: '#5a9c4a' },
  { key: 'magnesium', side: 'right', y: 285, color: '#a9c97a' },
  { key: 'phosphate', side: 'left', y: 365, color: '#4a4a2a' },
  { key: 'co2', side: 'right', y: 365, color: '#cfcac0', scale: 0.65 },
]

const selectedKey = ref(null)
const correctingEventId = ref(null)

function deficiencyName(key) {
  const d = phStore.deficiencies.find(d => d.key === key)
  if (!d) return key
  return locale.value === 'pl' ? d.name_pl : d.name_en
}

function deficiencySymptom(key) {
  const d = phStore.deficiencies.find(d => d.key === key)
  if (!d) return ''
  return locale.value === 'pl' ? d.symptom_pl : d.symptom_en
}

function deficiencyTreatment(key) {
  const d = phStore.deficiencies.find(d => d.key === key)
  if (!d) return ''
  return locale.value === 'pl' ? d.treatment_pl : d.treatment_en
}

// ── Pending action -> plant picker ────────────────────────────
// null | { type: 'manual', deficiencyKey } | { type: 'scan', file }
const pendingAction = ref(null)

function logSelected() {
  if (!selectedKey.value) return
  pendingAction.value = { type: 'manual', deficiencyKey: selectedKey.value }
  selectedKey.value = null
}

function startScan(ev) {
  const file = ev.target.files?.[0]
  ev.target.value = ''
  if (!file) return
  pendingAction.value = { type: 'scan', file }
}

async function choosePlantForAction(plant) {
  const action = pendingAction.value
  if (!action) return
  pendingAction.value = null
  if (action.type === 'manual') {
    await phStore.logEvent(plant.id, action.deficiencyKey)
  } else {
    await phStore.scanLeaf(plant.id, action.file)
  }
}

function openCorrect(e) {
  correctingEventId.value = correctingEventId.value === e.id ? null : e.id
}

async function correctWith(e, d) {
  await phStore.correctEvent(e.id, d.key)
  correctingEventId.value = null
}

const pendingEvents = computed(() => phStore.events.filter(e => e.status === 'pending'))
</script>

<style scoped>
.ph-svg {
  width: 100%;
  max-width: 360px;
  height: auto;
  display: block;
  margin: 8px auto 0;
}
.ph-leaf {
  cursor: pointer;
}
.ph-leaf path {
  stroke: var(--border);
  stroke-width: 1;
  transition: stroke 0.15s, stroke-width 0.15s;
}
.ph-leaf.on path {
  stroke: var(--accent);
  stroke-width: 2.5;
}
</style>
