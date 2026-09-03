<template>
  <div>
    <!-- Main tile -->
    <div class="tile">
      <div class="tile-hd">
        <h2>TESTY WODY</h2>
        <div class="row" style="gap:8px">
          <button class="btn btn-sm btn-ghost icon-btn" @click="openNormsModal" :title="locale === 'pl' ? 'Normy' : 'Norms'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
          </button>
          <button class="btn btn-sm btn-accent" @click="openScanModal">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 8.5a2 2 0 0 1 2-2h2l1.5-2h7L17 6.5h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-9z" />
              <circle cx="12" cy="12.5" r="3.5" />
            </svg>
            Skanuj
          </button>
        </div>
      </div>
      <hr class="divider" />
      <TankSwitcher />

      <!-- Overdue test reminders - log a value or snooze until later -->
      <div v-if="reminders.length" class="tile-body" style="padding-top:12px;padding-bottom:4px;display:flex;flex-direction:column;gap:8px">
        <div v-for="r in reminders" :key="'rem-' + r.parameter_id" class="ls-card" style="flex-direction:column;align-items:stretch;gap:6px;padding:10px 12px;border-left:3px solid var(--warning)">
          <div class="spread">
            <span style="font-weight:600;font-size:13px">🧪 {{ r.name_pl }}</span>
            <span class="muted" style="font-size:11px">{{ formatUpdatedAt(r.last_tested_at) }}</span>
          </div>
          <div class="row" style="gap:8px">
            <input class="input" type="number" step="0.01" v-model="reminderValues[r.parameter_id]" :placeholder="locale === 'pl' ? 'Wynik' : 'Result'" style="flex:1;text-align:right">
            <span class="muted" style="min-width:30px;font-size:12px">{{ r.unit }}</span>
            <button class="btn btn-sm btn-accent" :disabled="!reminderValues[r.parameter_id]" @click="logReminder(r)">
              {{ locale === 'pl' ? 'Zapisz' : 'Log' }}
            </button>
            <button class="btn btn-sm btn-ghost" @click="snoozeReminder(r)">
              {{ r.snoozed_at ? (locale === 'pl' ? 'Odłożone' : 'Snoozed') : (locale === 'pl' ? 'Później' : 'Snooze') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="currentReadings.length === 0" class="empty" style="padding:34px 16px">
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
        <div class="tile-body ptable" style="padding-top:12px">
          <!-- Header row -->
          <div class="prow" style="padding-bottom:6px">
            <span class="sec-lab" style="padding:0">Parametr</span>
            <span class="sec-lab" style="padding:0;text-align:right">Wartość</span>
            <span class="sec-lab" style="padding:0;text-align:center">Status</span>
            <span class="sec-lab" style="padding:0;text-align:center">Trend</span>
          </div>

          <!-- Data rows - tap a row to edit that parameter's value -->
          <div v-for="p in currentReadings" :key="p.parameter_key" class="prow" style="cursor:pointer" @click="openEditParam(p)">
            <span class="pp">
              {{ p.name_pl }}
              <span class="pp-time">{{ formatUpdatedAt(p.updated_at) }}</span>
            </span>
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

          <!-- Manual params with no reading yet in this test - tap to add -->
          <div
            v-for="p in missingManualParams"
            :key="'missing-' + p.id"
            class="prow"
            style="cursor:pointer"
            @click="openAddParam(p)"
          >
            <span class="pp muted">+ {{ p.name_pl }}</span>
            <span class="pv muted" style="grid-column:span 3;text-align:right">{{ locale === 'pl' ? 'Dodaj wartość' : 'Add value' }}</span>
          </div>
        </div>

        <hr class="divider" />

        <div class="tile-body" style="padding-top:14px">
          <div class="row" style="gap:10px">
            <button class="btn btn-block" @click="openHistoryModal">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 3-6.7" />
                <path d="M3 4v4h4" />
                <path d="M12 8v4l3 2" />
              </svg>
              Historia
            </button>
            <button class="btn btn-block" @click="openCycleModal">
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
        <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">

        <!-- Upload + manual phase -->
          <template v-if="scanPhase !== 'confirm'">
            <input type="file" accept="image/*" ref="fileInputRef" style="display:none" @change="handleFile">
            <div
              style="aspect-ratio:3/4;border-radius:14px;overflow:hidden;position:relative;border:2px dashed var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center"
              @click="fileInputRef?.click()"
            >
              <img v-if="scannedImageUrl" :src="scannedImageUrl" style="width:100%;height:100%;object-fit:cover;display:block">
              <div v-else style="display:flex;flex-direction:column;align-items:center;gap:10px;color:var(--text-muted)">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <span style="font-size:14px;font-weight:600">Wgraj zdjęcie</span>
                <span style="font-size:12px">Dotknij aby wybrać</span>
              </div>
            </div>

            <p class="muted" style="font-size:12.5px;text-align:center;margin:14px 0 18px">
              Wgraj zdjęcie paska testowego — data zostanie pobrana z EXIF.
            </p>

            <button
              class="btn btn-block btn-ghost"
              style="margin-bottom:10px"
              @click="enterManual"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 6h20v12H2z"/><path d="M6 10h.01"/><path d="M10 10h.01"/><path d="M14 10h.01"/><path d="M18 10h.01"/><path d="M8 14h8"/>
              </svg>
              Wpisz ręcznie
            </button>

            <button
              class="btn btn-accent btn-block btn-lg"
              @click="fileInputRef?.click()"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Wgraj zdjęcie
            </button>
          </template>

          <!-- Confirm phase -->
          <template v-else>
            <div v-if="scannedImageUrl" style="margin-bottom:16px;border-radius:10px;overflow:hidden;max-height:180px">
              <img :src="scannedImageUrl" style="width:100%;object-fit:cover;display:block">
            </div>

            <div class="field" style="margin-bottom:16px">
              <label style="font-size:12px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:6px">Data testu</label>
              <input
                class="input"
                type="datetime-local"
                v-model="testDate"
                style="font-size:14px"
              />
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

    <!-- Edit/add single parameter popup -->
    <Teleport to="body">
      <div v-if="editParam" class="backdrop" @click.self="editParam = null">
        <div class="modal" style="max-width:360px;padding:20px;display:flex;flex-direction:column;gap:12px" @click.stop>
          <div class="spread">
            <span style="font-weight:700;font-size:17px">{{ editParam.name_pl }}</span>
            <button class="btn icon-btn btn-ghost" @click="editParam = null">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
              </svg>
            </button>
          </div>
          <div class="row" style="gap:8px">
            <input class="input" type="number" step="0.01" v-model="editParam.value" autofocus style="flex:1;font-size:16px;text-align:right" @keyup.enter="saveEditParam">
            <span class="muted" style="min-width:30px">{{ editParam.unit }}</span>
          </div>
          <button class="btn btn-accent btn-block" :disabled="savingParam" @click="saveEditParam">
            {{ savingParam ? (locale === 'pl' ? 'Zapisywanie…' : 'Saving…') : (locale === 'pl' ? 'Zapisz' : 'Save') }}
          </button>
        </div>
      </div>
    </Teleport>

    <!-- Norms (safe range) settings - per-tank, since two differently
         stocked tanks want different min/max for the same test. -->
    <Teleport to="body">
      <div v-if="normsModal" class="backdrop" style="align-items:stretch;justify-content:center" @click.self="normsModal = false">
        <div class="modal full" @click.stop>
          <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
            <button class="btn icon-btn btn-ghost" @click="normsModal = false">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
              </svg>
            </button>
            <span style="font-weight:700;font-size:16px">{{ locale === 'pl' ? 'Normy' : 'Norms' }} · {{ tankStore.tanks.find(t => t.id === tankStore.activeTankId)?.name }}</span>
            <span style="width:34px"></span>
          </div>
          <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
            <p class="muted" style="font-size:12.5px;margin:0 0 14px">
              {{ locale === 'pl' ? 'Zakres bezpieczny dla tego zbiornika. Puste pole = brak limitu.' : 'Safe range for this tank. Empty = no limit.' }}
            </p>
            <div v-for="p in parameters" :key="p.id" class="field" style="margin-bottom:14px">
              <label style="font-size:13px;font-weight:600;display:block;margin-bottom:6px">{{ p.name_pl }} <span class="muted" style="font-weight:400">({{ p.unit }})</span></label>
              <div class="row" style="gap:8px">
                <input class="input" type="number" step="0.01" v-model="normDrafts[p.id].min_safe" :placeholder="locale === 'pl' ? 'Min' : 'Min'" style="flex:1;text-align:right">
                <span class="muted">–</span>
                <input class="input" type="number" step="0.01" v-model="normDrafts[p.id].max_safe" :placeholder="locale === 'pl' ? 'Maks' : 'Max'" style="flex:1;text-align:right">
              </div>
              <div v-if="p.category === 'manual'" class="row" style="gap:8px;margin-top:6px">
                <span class="muted" style="font-size:12px;white-space:nowrap">{{ locale === 'pl' ? 'Co (dni)' : 'Every (days)' }}</span>
                <input class="input" type="number" step="1" v-model="normDrafts[p.id].test_frequency_days" placeholder="—" style="width:70px;text-align:right">
                <button class="btn btn-sm btn-accent" style="margin-left:auto" :disabled="savingNorm === p.id" @click="saveNorm(p)">
                  {{ savingNorm === p.id ? '…' : (locale === 'pl' ? 'Zapisz' : 'Save') }}
                </button>
              </div>
              <button v-else class="btn btn-sm btn-accent" style="margin-top:6px" :disabled="savingNorm === p.id" @click="saveNorm(p)">
                {{ savingNorm === p.id ? '…' : (locale === 'pl' ? 'Zapisz' : 'Save') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Historia - past test sessions for this tank -->
    <Teleport to="body">
      <div v-if="historyModal" class="backdrop" style="align-items:stretch;justify-content:center" @click.self="historyModal = false">
        <div class="modal full" @click.stop>
          <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
            <button class="btn icon-btn btn-ghost" @click="historyModal = false">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
              </svg>
            </button>
            <span style="font-weight:700;font-size:16px">{{ locale === 'pl' ? 'Historia' : 'History' }} · {{ tankStore.tanks.find(t => t.id === tankStore.activeTankId)?.name }}</span>
            <span style="width:34px"></span>
          </div>
          <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
            <div v-if="!historySessions.length" class="muted" style="font-size:13px;text-align:center;padding:24px 0">
              {{ locale === 'pl' ? 'Brak testów' : 'No tests yet' }}
            </div>
            <div v-for="s in historySessions" :key="s.id" class="ls-card" style="flex-direction:column;align-items:stretch;gap:8px;padding:12px;margin-bottom:10px">
              <div class="spread">
                <span style="font-weight:700;font-size:13px">{{ formatSessionDate(s.tested_at) }}</span>
              </div>
              <div v-if="s.notes" class="muted" style="font-size:12px">{{ s.notes }}</div>
              <div style="display:flex;flex-wrap:wrap;gap:6px">
                <span
                  v-for="r in s.readings"
                  :key="r.id"
                  class="pill"
                  style="cursor:default"
                  :style="{ color: r.out_of_range ? 'var(--warning)' : 'var(--success)' }"
                >
                  {{ r.parameter_name_pl }}: {{ r.value }}{{ r.unit ? ' ' + r.unit : '' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Cykl zbiornika - nitrogen cycle status from current ammonia/nitrite/nitrate -->
    <Teleport to="body">
      <div v-if="cycleModal" class="backdrop" @click.self="cycleModal = false">
        <div class="modal" style="max-width:400px;padding:20px;display:flex;flex-direction:column;gap:12px" @click.stop>
          <div class="spread">
            <span style="font-weight:700;font-size:17px">{{ locale === 'pl' ? 'Cykl zbiornika' : 'Tank Cycle' }}</span>
            <button class="btn icon-btn btn-ghost" @click="cycleModal = false">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
              </svg>
            </button>
          </div>
          <div class="spread" style="padding:10px 12px;border-radius:10px;background:var(--surface-2,rgba(255,255,255,0.04))">
            <span style="font-weight:700" :style="{ color: cycleStatus.cycled ? 'var(--success)' : 'var(--warning)' }">
              {{ cycleStatus.cycled ? (locale === 'pl' ? '✓ Zacyklowany' : '✓ Cycled') : (locale === 'pl' ? 'Wciąż się cykluje' : 'Still cycling') }}
            </span>
          </div>
          <div v-for="row in cycleStatus.rows" :key="row.key" class="spread" style="font-size:13px">
            <span>{{ row.label }}</span>
            <span :style="{ fontWeight: 700, color: row.ok ? 'var(--success)' : 'var(--warning)' }">
              {{ row.value != null ? row.value + ' ' + row.unit : (locale === 'pl' ? 'brak danych' : 'no data') }}
            </span>
          </div>
          <p class="muted" style="font-size:12px;margin:4px 0 0">
            {{ locale === 'pl'
              ? 'Zacyklowany: amoniak i azotyny = 0, azotany obecne (bakterie nitryfikacyjne w pełni ustanowione).'
              : 'Cycled means ammonia and nitrite are both 0 while nitrate is present (nitrifying bacteria fully established).' }}
          </p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useTankSelectorStore } from '../stores/tankSelector'
import { useWaterTestsStore } from '../stores/waterTests'
import TankSwitcher from '../components/TankSwitcher.vue'

const { locale } = useI18n()
const tankStore = useTankSelectorStore()
const waterStore = useWaterTestsStore()
const currentReadingsRaw = computed(() => waterStore.currentByTank[Number(tankStore.activeTankId)] || [])
const parameters = ref([])

async function fetchParameters() {
  const paramR = await axios.get('/api/water-tests/parameters', { params: { tank_id: tankStore.activeTankId } })
  parameters.value = paramR.data
}

async function fetchCurrent() {
  await waterStore.fetchCurrent(tankStore.activeTankId)
}

const reminders = ref([])
const reminderValues = ref({})

async function fetchReminders() {
  const r = await axios.get('/api/water-tests/reminders', { params: { tank_id: tankStore.activeTankId } })
  reminders.value = r.data
}

onMounted(async () => {
  await Promise.all([fetchCurrent(), fetchParameters(), fetchReminders()])
})

watch(() => tankStore.activeTankId, async () => {
  await Promise.all([fetchCurrent(), fetchParameters(), fetchReminders()])
})

const currentReadings = computed(() => {
  return currentReadingsRaw.value.map((r) => {
    const param = parameters.value.find((p) => p.id === r.parameter_id)
    return {
      ...r,
      name_pl: param?.name_pl ?? r.parameter_name_pl ?? r.parameter_id,
      name_en: param?.name_en ?? r.parameter_name_en,
      unit: param?.unit ?? r.unit ?? '',
      trend: 'flat',
      parameter_key: param?.key ?? r.parameter_key,
    }
  })
})

function formatUpdatedAt(iso) {
  if (!iso) return locale.value === 'pl' ? 'brak daty' : 'no date'
  const d = new Date(iso)
  if (isNaN(d.getTime())) return locale.value === 'pl' ? 'brak daty' : 'no date'
  const ms = Date.now() - d.getTime()
  const mins = Math.floor(ms / 60000)
  const hours = Math.floor(ms / 3600000)
  const days = Math.floor(ms / 86400000)
  if (mins < 1) return locale.value === 'pl' ? 'przed chwilą' : 'just now'
  if (mins < 60) return locale.value === 'pl' ? `${mins} min temu` : `${mins}m ago`
  if (hours < 24) return locale.value === 'pl' ? `${hours} godz. temu` : `${hours}h ago`
  if (days === 1) return locale.value === 'pl' ? 'wczoraj' : 'yesterday'
  const when = d.toLocaleString(locale.value === 'pl' ? 'pl-PL' : 'en-GB', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
  })
  return `${days} dni · ${when}`
}

const manualParams = computed(() =>
  parameters.value.filter((p) => p.category === 'manual')
)

// Manual params not present in the latest test - offered as quick "+ add" rows.
const missingManualParams = computed(() => {
  const have = new Set(currentReadings.value.map((r) => r.parameter_id))
  return manualParams.value.filter((p) => !have.has(p.id))
})

const statusColor = (p) => {
  if (p.out_of_range) return 'var(--warning)'
  return 'var(--success)'
}

const statusText = (p) => (p.out_of_range ? 'Wysoko' : 'OK')

// ─── Helpers ──────────────────────────────────────────────────────────────────
function toLocalDatetimeInput(d) {
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

function extractExifDate(file) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const bytes = new Uint8Array(e.target.result)
        let str = ''
        for (let i = 0; i < bytes.length; i++) str += String.fromCharCode(bytes[i])
        // EXIF DateTimeOriginal format: "YYYY:MM:DD HH:MM:SS"
        const m = str.match(/(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})/)
        if (m) {
          const dt = new Date(`${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:${m[6]}`)
          if (!isNaN(dt.getTime())) { resolve(dt); return }
        }
      } catch {}
      resolve(new Date(file.lastModified || Date.now()))
    }
    reader.onerror = () => resolve(new Date(file.lastModified || Date.now()))
    reader.readAsArrayBuffer(file.slice(0, 65536))
  })
}

// ─── Scan modal state ─────────────────────────────────────────────────────────
const scanModal = ref(false)
const scanPhase = ref('upload')
const detectedValues = ref({})
const saving = ref(false)
const fileInputRef = ref(null)
const scannedImageUrl = ref(null)
const testDate = ref('')
const cacheId = ref(null)

function openScanModal() {
  scanPhase.value = 'upload'
  detectedValues.value = {}
  scannedImageUrl.value = null
  testDate.value = toLocalDatetimeInput(new Date())
  cacheId.value = null
  scanModal.value = true
}

function closeScanModal() {
  scanModal.value = false
  scanPhase.value = 'upload'
  detectedValues.value = {}
  scannedImageUrl.value = null
  testDate.value = ''
  cacheId.value = null
}

function enterManual() {
  const vals = {}
  manualParams.value.forEach((p) => { vals[p.id] = '' })
  detectedValues.value = vals
  testDate.value = toLocalDatetimeInput(new Date())
  cacheId.value = null
  scanError.value = null
  scanPhase.value = 'confirm'
}

async function handleFile(event) {
  const file = event.target.files?.[0]
  if (!file) return

  scannedImageUrl.value = URL.createObjectURL(file)
  scanError.value = null

  const dt = await extractExifDate(file)
  testDate.value = toLocalDatetimeInput(dt)

  const vals = {}
  manualParams.value.forEach((p) => { vals[p.id] = '' })
  detectedValues.value = vals
  cacheId.value = null
  scanPhase.value = 'confirm'

  if (fileInputRef.value) fileInputRef.value.value = ''
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
    const payload = { readings, tank_id: tankStore.activeTankId }
    if (cacheId.value != null) payload.scan_cache_id = cacheId.value
    if (testDate.value) payload.tested_at = new Date(testDate.value).toISOString()

    await axios.post('/api/water-tests/sessions', payload)
    await fetchCurrent()
  } finally {
    saving.value = false
    closeScanModal()
  }
}

// ─── Log a single parameter reading ───────────────────────────────────────────
// Always creates a new dated entry (never overwrites history) so trend /
// water-change-frequency analysis stays accurate.
const editParam = ref(null)
const savingParam = ref(false)

function openEditParam(reading) {
  editParam.value = {
    parameterId: reading.parameter_id,
    name_pl: reading.name_pl,
    unit: reading.unit,
    value: reading.value,
  }
}

function openAddParam(param) {
  editParam.value = {
    parameterId: param.id,
    name_pl: param.name_pl,
    unit: param.unit,
    value: '',
  }
}

async function saveEditParam() {
  const value = parseFloat(editParam.value.value)
  if (isNaN(value)) return

  savingParam.value = true
  try {
    await axios.post('/api/water-tests/sessions', {
      tank_id: tankStore.activeTankId,
      readings: [{ parameter_id: editParam.value.parameterId, value }],
    })
    await fetchCurrent()
    editParam.value = null
  } finally {
    savingParam.value = false
  }
}

async function logReminder(reminder) {
  const value = parseFloat(reminderValues.value[reminder.parameter_id])
  if (isNaN(value)) return
  await axios.post('/api/water-tests/sessions', {
    tank_id: tankStore.activeTankId,
    readings: [{ parameter_id: reminder.parameter_id, value }],
  })
  reminderValues.value[reminder.parameter_id] = ''
  await Promise.all([fetchCurrent(), fetchReminders()])
}

async function snoozeReminder(reminder) {
  await axios.post(`/api/water-tests/reminders/${reminder.parameter_id}/snooze`, {
    tank_id: tankStore.activeTankId,
  })
  await fetchReminders()
}

// ─── Norms (per-tank safe range) settings ─────────────────────────────────────
const normsModal = ref(false)
const normDrafts = ref({})
const savingNorm = ref(null)

function openNormsModal() {
  const drafts = {}
  parameters.value.forEach((p) => {
    drafts[p.id] = {
      min_safe: p.min_safe ?? '',
      max_safe: p.max_safe ?? '',
      test_frequency_days: p.test_frequency_days ?? '',
    }
  })
  normDrafts.value = drafts
  normsModal.value = true
}

async function saveNorm(param) {
  const draft = normDrafts.value[param.id]
  savingNorm.value = param.id
  try {
    await axios.put(`/api/water-tests/parameters/${param.id}/norms`, {
      tank_id: tankStore.activeTankId,
      min_safe: draft.min_safe === '' ? null : parseFloat(draft.min_safe),
      max_safe: draft.max_safe === '' ? null : parseFloat(draft.max_safe),
      test_frequency_days: draft.test_frequency_days === '' ? null : parseInt(draft.test_frequency_days),
    })
    await Promise.all([fetchParameters(), fetchReminders()])
  } finally {
    savingNorm.value = null
  }
}

// ─── Historia (past sessions) ─────────────────────────────────────────────────
const historyModal = ref(false)
const historySessions = ref([])

async function openHistoryModal() {
  const r = await axios.get('/api/water-tests/sessions', { params: { tank_id: tankStore.activeTankId, limit: 50 } })
  historySessions.value = r.data
  historyModal.value = true
}

function formatSessionDate(iso) {
  const d = new Date(iso)
  return d.toLocaleString(locale.value === 'pl' ? 'pl-PL' : 'en-GB', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
  })
}

// ─── Cykl zbiornika (nitrogen cycle status) ───────────────────────────────────
const cycleModal = ref(false)

const cycleStatus = computed(() => {
  const find = (key) => currentReadings.value.find((r) => r.parameter_key === key)
  const ammonia = find('ammonia')
  const nitrite = find('nitrite')
  const nitrate = find('nitrate')
  const cycled = ammonia?.value === 0 && nitrite?.value === 0 && (nitrate?.value ?? 0) > 0
  return {
    cycled,
    rows: [
      { key: 'ammonia', label: locale.value === 'pl' ? 'Amoniak (NH3/NH4)' : 'Ammonia (NH3/NH4)', value: ammonia?.value ?? null, unit: ammonia?.unit ?? 'mg/L', ok: (ammonia?.value ?? 0) === 0 },
      { key: 'nitrite', label: locale.value === 'pl' ? 'Azotyny (NO2)' : 'Nitrite (NO2)', value: nitrite?.value ?? null, unit: nitrite?.unit ?? 'mg/L', ok: (nitrite?.value ?? 0) === 0 },
      { key: 'nitrate', label: locale.value === 'pl' ? 'Azotany (NO3)' : 'Nitrate (NO3)', value: nitrate?.value ?? null, unit: nitrate?.unit ?? 'mg/L', ok: (nitrate?.value ?? 0) > 0 },
    ],
  }
})

function openCycleModal() {
  cycleModal.value = true
}
</script>
