<template>
  <!-- ── Main livestock tile ────────────────────────────────────── -->
  <div class="tile ls-tile">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
          <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
          <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
        </svg>
        OBSADA
      </h2>
      <button class="btn btn-sm btn-accent" @click="editModal = { item: null, kind: 'fish' }">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14"/><path d="M5 12h14"/>
        </svg>
        {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
      </button>
    </div>
    <hr class="divider">
    <TankSwitcher />

    <!-- Empty state -->
    <div v-if="!fish.length && !plants.length" class="empty" style="padding:40px 16px">
      <span class="em">🐠</span>
      <span>{{ locale === 'pl' ? 'Dodaj pierwsze ryby' : 'Add your first fish' }}</span>
    </div>

    <!-- Content -->
    <div v-else class="tile-body" style="padding-top:4px">
      <!-- Fish section -->
      <div class="sec-lab">{{ locale === 'pl' ? 'Ryby' : 'Fish' }} ({{ fish.length }})</div>
      <div
        v-for="x in fish"
        :key="x.id"
        class="ls-card"
        @click="editModal = { item: x, kind: 'fish' }"
      >
        <div class="ls-thumb">
          <img v-if="x.img" :src="x.img" style="width:100%;height:100%;object-fit:cover">
          <div v-else class="ph">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/>
              <path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/>
              <circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
          </div>
        </div>
        <div class="ls-meta">
          <div class="name">
            <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
              {{ locale === 'pl' && x.name_pl ? x.name_pl : x.name_en }}
            </span>
            <span
              :class="['pill', x.status]"
              @click.stop="togglePicker(x.id)"
            >
              {{ statusLabel(x.status) }}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 9l7 7 7-7"/>
              </svg>
            </span>
          </div>
          <span class="sp">{{ x.latin }}</span>
          <span class="sub">
            {{ x.status === 'planned' ? (locale === 'pl' ? 'Planowane' : 'Planned') : (locale === 'pl' ? 'Dodano' : 'Added') }}:
            {{ formatDate(x.added_at) }} · ×{{ x.qty }}
          </span>
          <!-- Inline status picker -->
          <div
            v-if="statusPicker === x.id"
            class="row"
            style="gap:6px;margin-top:8px;flex-wrap:wrap"
            @click.stop
          >
            <span
              v-for="s in statuses"
              :key="s"
              :class="['pill', s]"
              :style="{ opacity: s === x.status ? 1 : 0.6, cursor: 'pointer' }"
              @click="setStatus(x, s)"
            >
              {{ statusLabel(s) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Plants section -->
      <div v-if="plants.length > 0" class="sec-lab" style="padding-top:14px">
        {{ locale === 'pl' ? 'Rośliny' : 'Plants' }} ({{ plants.length }})
      </div>
      <div
        v-for="x in plants"
        :key="x.id"
        class="ls-card"
        @click="editModal = { item: x, kind: 'plant' }"
      >
        <div class="ls-thumb">
          <img v-if="x.img" :src="x.img" style="width:100%;height:100%;object-fit:cover">
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
              {{ locale === 'pl' && x.name_pl ? x.name_pl : x.name_en }}
            </span>
            <span class="pill in_tank" style="cursor:default">
              {{ locale === 'pl' ? 'W zbiorniku' : 'In tank' }}
            </span>
          </div>
          <span class="sp">{{ x.latin }}</span>
          <span class="sub">
            {{ locale === 'pl' ? 'Dodano' : 'Added' }}: {{ formatDate(x.added_at) }}
          </span>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════ PLANT HEALTH ENTRY POINT ═══════════════════════════ -->
  <div class="tile" style="cursor:pointer" @click="showPlantHealth = true">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 4S8 4 6 12c-1 4 1 7 1 7s9-1 11-9c1-4 2-6 2-6z"/>
          <path d="M5 19c2-6 6-9 10-10"/>
        </svg>
        {{ locale === 'pl' ? 'ZDROWIE ROŚLIN' : 'PLANT HEALTH' }}
      </h2>
      <span v-if="pendingPlantHealthCount > 0" class="task-badge b-overdue">{{ pendingPlantHealthCount }}</span>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 6l6 6-6 6"/>
      </svg>
    </div>
  </div>

  <!-- ═══════════════════════════ DOSING TILE ═══════════════════════════ -->
  <div class="tile">
    <div class="tile-hd">
      <h2>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
        </svg>
        {{ locale === 'pl' ? 'DAWKOWANIE' : 'DOSING' }}
      </h2>
      <button class="btn btn-sm btn-ghost" @click="openDoseEdit(null)">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14"/><path d="M5 12h14"/>
        </svg>
        {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
      </button>
    </div>
    <hr class="divider">
    <div class="tile-body">
      <div v-if="filteredDosingTasks.length === 0" class="empty">
        <span>{{ locale === 'pl' ? 'Brak dawkowań' : 'No doses configured' }}</span>
        <button class="btn btn-sm btn-accent" @click="openDoseEdit(null)">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 5v14"/><path d="M5 12h14"/>
          </svg>
          {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
        </button>
      </div>
      <div
        v-for="(task, i) in filteredDosingTasks"
        :key="task.id"
        :style="{ paddingTop: '12px', paddingBottom: '12px', borderTop: i > 0 ? '1px solid var(--border)' : 'none' }"
      >
        <div class="row" style="justify-content:space-between;margin-bottom:0">
          <div class="row" style="gap:9px;min-width:0;flex:1">
            <span style="color:var(--accent);display:flex;flex-shrink:0">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
              </svg>
            </span>
            <span style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ locale === 'pl' ? task.supply_name_pl : task.supply_name }}</span>
            <span class="muted tnum" style="font-size:13px;white-space:nowrap">{{ task.dose_amount }}{{ task.dose_unit }}<span v-if="task.time_of_day"> · {{ task.time_of_day }}</span></span>
          </div>
          <div class="row" style="gap:6px;flex-shrink:0">
            <button class="btn icon-btn" :class="{ 'btn-success': task.done_today }" @click="scheduleStore.completeDose(task.id)">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 12.5l5 5 11-12"/>
              </svg>
            </button>
            <button class="btn icon-btn btn-ghost" @click="openDoseEdit(task)">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M14 6l4 4"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="spread" style="margin:9px 0 6px;font-size:12px">
          <span class="muted">
            {{ locale === 'pl' ? 'Pozostało:' : 'Left:' }}
            <b class="tnum" style="color:var(--text)">{{ task.supply_current_amount ?? '—' }}{{ task.supply_unit }}</b>
          </span>
          <span class="muted tnum">{{ supplyPct(task) }}%</span>
        </div>
        <div class="bar" :class="supplyBarClass(supplyPct(task))">
          <i :style="{ width: Math.max(0, Math.min(100, supplyPct(task))) + '%' }"></i>
        </div>
        <button class="btn btn-sm btn-ghost" style="margin-top:10px" @click="openRestock(task)">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 5v9"/><path d="M8 10l4 4 4-4"/><path d="M5 19h14"/>
          </svg>
          {{ locale === 'pl' ? 'Uzupełnij' : 'Restock' }}
        </button>
      </div>
    </div>
  </div>

  <!-- ── LsEditModal (full-screen) ──────────────────────────────── -->
  <Teleport to="body">
    <div
      v-if="editModal"
      class="backdrop"
      style="position:fixed;align-items:stretch;justify-content:center"
      @click.self="editModal = null"
    >
      <div class="modal full" @click.stop>
        <!-- Modal header -->
        <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
          <button class="btn icon-btn btn-ghost" @click="editModal = null">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">
            {{ editModal.item ? (locale === 'pl' ? 'Edytuj' : 'Edit') : (locale === 'pl' ? 'Dodaj' : 'Add') }}
          </span>
          <button class="btn btn-sm btn-accent" @click="saveLs">
            {{ locale === 'pl' ? 'Zapisz' : 'Save' }}
          </button>
        </div>

        <!-- Modal body -->
        <div style="padding:16px;overflow-y:scroll;-webkit-overflow-scrolling:touch;overscroll-behavior:contain">
          <!-- Thumb + kind segmented + image search -->
          <div class="row" style="gap:14px;margin-bottom:16px;align-items:flex-start">
            <div class="ls-thumb" style="width:72px;height:72px;flex-shrink:0">
              <img v-if="lsFormImg" :src="lsFormImg" style="width:100%;height:100%;object-fit:cover">
              <div v-else class="ph" style="font-size:9px">{{ locale === 'pl' ? 'zdjęcie' : 'image' }}</div>
            </div>
            <div style="flex:1;display:flex;flex-direction:column;gap:8px">
              <div class="seg">
                <button :class="{ on: lsFormKind === 'fish' }" @click="lsFormKind = 'fish'">
                  {{ locale === 'pl' ? 'Ryba' : 'Fish' }}
                </button>
                <button :class="{ on: lsFormKind === 'plant' }" @click="lsFormKind = 'plant'">
                  {{ locale === 'pl' ? 'Roślina' : 'Plant' }}
                </button>
              </div>
              <div v-if="tankStore.tanks.length > 1" class="seg">
                <button
                  v-for="t in tankStore.tanks"
                  :key="t.id"
                  :class="{ on: lsFormTankId === t.id }"
                  @click="lsFormTankId = t.id"
                >
                  {{ t.name }}
                </button>
              </div>
              <button class="btn btn-ghost" style="font-size:12px" @click="searchImg" :disabled="obsadaStore.searching">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
                </svg>
                {{ obsadaStore.searching ? (locale === 'pl' ? 'Szukam…' : 'Searching…') : (locale === 'pl' ? 'Szukaj zdjęcia' : 'Search image') }}
              </button>
            </div>
          </div>

          <!-- Image search results -->
          <div v-if="obsadaStore.searchResults?.images?.length" style="margin-bottom:16px">
            <div class="sec-lab" style="padding-bottom:6px">{{ locale === 'pl' ? 'Wyniki' : 'Results' }}</div>
            <div v-if="obsadaStore.searchResults.is_genus_fallback" class="muted" style="font-size:11px;margin-bottom:6px;text-align:center">
              {{ locale === 'pl' ? 'Brak zdjęć gatunku — pokazuję podobne z rodzaju' : 'No species photos — showing similar from genus' }}
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px">
              <div
                v-for="img in obsadaStore.searchResults.images"
                :key="img.url"
                style="aspect-ratio:1;border-radius:6px;overflow:hidden;cursor:pointer;border:2px solid transparent"
                :style="{ borderColor: lsFormImg === img.url ? 'var(--accent)' : 'transparent' }"
                @click="lsFormImg = img.url"
              >
                <img :src="img.thumb || img.url" style="width:100%;height:100%;object-fit:cover">
              </div>
            </div>
          </div>
          <div v-else-if="obsadaStore.searchResults && !obsadaStore.searching" class="muted" style="font-size:12px;margin-bottom:12px;text-align:center">
            {{ locale === 'pl' ? 'Brak zdjęć dla tego gatunku' : 'No images found for this species' }}
          </div>

          <div class="field">
            <label>{{ locale === 'pl' ? 'Nazwa' : 'Name' }}</label>
            <input class="input" v-model="lsFormName" autofocus :placeholder="lsFormKind === 'fish' ? 'Pyszczak mozambicki…' : 'Elodea…'">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Gatunek (łac.)' : 'Species (latin)' }}</label>
            <input class="input" v-model="lsFormLatin" style="font-style:italic" placeholder="Oreochromis mossambicus…">
          </div>
          <div class="row" style="gap:12px">
            <div class="field" style="width:100px">
              <label>{{ locale === 'pl' ? 'Ilość' : 'Count' }}</label>
              <input class="input" type="number" v-model="lsFormQty" min="1">
            </div>
            <div class="field" style="flex:1">
              <label>{{ locale === 'pl' ? 'Data' : 'Date' }}</label>
              <input class="input" type="date" v-model="lsFormDate">
            </div>
          </div>

          <!-- Status picker — fish only -->
          <div v-if="lsFormKind === 'fish'" class="field">
            <label>{{ locale === 'pl' ? 'Status' : 'Status' }}</label>
            <div class="seg" style="flex-wrap:wrap">
              <button
                v-for="s in statuses"
                :key="s"
                :class="{ on: lsFormStatus === s }"
                @click="lsFormStatus = s"
              >
                {{ statusLabel(s) }}
              </button>
            </div>
          </div>

          <!-- Delete -->
          <div v-if="editModal.item?.id" style="margin-top:16px">
            <div v-if="lsConfirmDelete" class="row" style="gap:10px">
              <span class="muted" style="font-size:13px;flex:1">
                {{ locale === 'pl' ? 'Usunąć?' : 'Delete?' }}
              </span>
              <button class="btn btn-danger-o" @click="deleteLs">
                {{ locale === 'pl' ? 'Tak, usuń' : 'Yes, delete' }}
              </button>
              <button class="btn btn-ghost" @click="lsConfirmDelete = false">
                {{ locale === 'pl' ? 'Anuluj' : 'Cancel' }}
              </button>
            </div>
            <button v-else class="btn btn-block btn-danger-o" @click="lsConfirmDelete = true">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 7h16"/><path d="M9 7V5h6v2"/><path d="M6 7l1 13h10l1-13"/>
              </svg>
              {{ locale === 'pl' ? 'Usuń' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>

  <!-- ═══════════════════════════ RESTOCK MODAL ═══════════════════════════ -->
  <div v-if="restockDose" class="backdrop" @click.self="restockDose = null">
    <div class="modal">
      <h3 class="modal-title">{{ locale === 'pl' ? 'Uzupełnij zapas' : 'Restock supply' }}</h3>
      <p class="modal-sub">{{ locale === 'pl' ? restockDose.supply_name_pl : restockDose.supply_name }}</p>
      <div class="field">
        <label>{{ locale === 'pl' ? 'Ile dodajesz?' : 'How much to add?' }}</label>
        <div class="input-row">
          <input class="input" type="number" inputmode="decimal" v-model="restockAmount" autofocus>
          <span class="unit">{{ restockDose.supply_unit }}</span>
        </div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-block" @click="restockDose = null">{{ locale === 'pl' ? 'Anuluj' : 'Cancel' }}</button>
        <button class="btn btn-accent btn-block" @click="handleRestock">{{ locale === 'pl' ? 'Potwierdź' : 'Confirm' }}</button>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════ DOSE EDIT MODAL ═══════════════════════════ -->
  <div v-if="doseEditOpen" class="backdrop" @click.self="doseEditOpen = false">
    <div class="modal">
      <h3 class="modal-title">{{ doseEditTask ? (locale === 'pl' ? 'Edytuj dawkę' : 'Edit dose') : (locale === 'pl' ? 'Nowa dawka' : 'Add dose') }}</h3>
      <div class="field">
        <label>{{ locale === 'pl' ? 'Nazwa (PL)' : 'Name (PL)' }}</label>
        <input class="input" v-model="doseForm.name_pl" placeholder="Nawóz…">
      </div>
      <div class="field">
        <label>Name (EN)</label>
        <input class="input" v-model="doseForm.name" placeholder="Fertilizer…">
      </div>
      <div class="row" style="gap:12px;align-items:flex-start">
        <div class="field" style="flex:1;margin-bottom:0">
          <label>{{ locale === 'pl' ? 'Dawka' : 'Amount' }}</label>
          <div class="input-row">
            <input class="input" type="number" inputmode="decimal" v-model="doseForm.amount">
            <span class="unit">{{ doseForm.unit }}</span>
          </div>
        </div>
        <div class="field" style="width:110px;margin-bottom:0">
          <label>{{ locale === 'pl' ? 'Godzina' : 'Time' }}</label>
          <input class="input" type="time" v-model="doseForm.time">
        </div>
      </div>
      <div class="field" style="margin-top:14px">
        <label>{{ locale === 'pl' ? 'Jednostka' : 'Unit' }}</label>
        <select class="select" v-model="doseForm.unit">
          <option value="ml">ml</option>
          <option value="g">g</option>
          <option value="drops">{{ locale === 'pl' ? 'krople' : 'drops' }}</option>
        </select>
      </div>
      <div v-if="tankStore.tanks.length > 1" class="field">
        <label>{{ locale === 'pl' ? 'Zbiornik' : 'Tank' }}</label>
        <div class="seg">
          <button
            v-for="t in tankStore.tanks"
            :key="t.id"
            :class="{ on: doseForm.tankId === t.id }"
            @click="doseForm.tankId = t.id"
          >
            {{ t.name }}
          </button>
        </div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-block" @click="doseEditOpen = false">{{ locale === 'pl' ? 'Anuluj' : 'Cancel' }}</button>
        <button class="btn btn-accent btn-block" @click="saveDose">{{ locale === 'pl' ? 'Zapisz' : 'Save' }}</button>
      </div>
    </div>
  </div>

  <PlantHealthView v-if="showPlantHealth" @close="showPlantHealth = false" />
</template>

<script setup>
import { useObsadaStore } from '../stores/obsada'
import { usePlantHealthStore } from '../stores/plantHealth'
import { useTankSelectorStore } from '../stores/tankSelector'
import { useScheduleStore } from '../stores/schedule'
import TankSwitcher from '../components/TankSwitcher.vue'
import PlantHealthView from './PlantHealthView.vue'
import { useI18n } from 'vue-i18n'
import { ref, reactive, computed, onMounted, watch, inject } from 'vue'

const { locale } = useI18n()
const obsadaStore = useObsadaStore()
const phStore = usePlantHealthStore()
const tankStore = useTankSelectorStore()
const scheduleStore = useScheduleStore()
const showToast = inject('showToast', () => {})

// ── UI state ──────────────────────────────────────────────────
const statusPicker = ref(null)   // id of item showing status picker
const editModal = ref(null)      // null | { item: fish|plant|null, kind: 'fish'|'plant' }
const showPlantHealth = ref(false)
const pendingPlantHealthCount = computed(() => phStore.events.filter(e => e.status === 'pending').length)

// ── Status helpers ────────────────────────────────────────────
const statuses = ['planned', 'in_tank', 'sold', 'deceased']

const STATUS_LABELS_PL = {
  planned: 'Planowany',
  in_tank: 'W zbiorniku',
  sold: 'Sprzedany',
  deceased: 'Obumarły',
}
const STATUS_LABELS_EN = {
  planned: 'Planned',
  in_tank: 'In tank',
  sold: 'Sold',
  deceased: 'Deceased',
}

function statusLabel(s) {
  const map = locale.value === 'pl' ? STATUS_LABELS_PL : STATUS_LABELS_EN
  return map[s] || s
}

function togglePicker(id) {
  statusPicker.value = statusPicker.value === id ? null : id
}

async function setStatus(x, s) {
  if (x.kind === 'fish') {
    await obsadaStore.updateFish(x.id, { status: s })
  }
  statusPicker.value = null
}

// ── Data ──────────────────────────────────────────────────────
const fish = computed(() =>
  obsadaStore.fish.filter(tankStore.matchesActiveTank).map(f => ({ ...f, kind: 'fish' }))
)
const plants = computed(() =>
  obsadaStore.plants.filter(tankStore.matchesActiveTank).map(p => ({ ...p, kind: 'plant' }))
)
const filteredDosingTasks = computed(() => scheduleStore.dosingTasks.filter(tankStore.matchesActiveTank))

onMounted(() => {
  obsadaStore.fetchFish()
  obsadaStore.fetchPlants()
  scheduleStore.fetchDosing()
  phStore.fetchEvents()
})

// ── Dosing ──────────────────────────────────────────────────────
const supplyPct = (task) => {
  if (!task.supply_current_amount || !task.supply_min_threshold) return 100
  const max = task.supply_min_threshold * 3
  return Math.round((task.supply_current_amount / max) * 100)
}

const supplyBarClass = (pct) => {
  if (pct > 50) return 'green'
  if (pct >= 20) return 'yellow'
  return 'red'
}

// Restock modal
const restockDose = ref(null)
const restockAmount = ref(0)

function openRestock(task) {
  restockDose.value = task
  restockAmount.value = 0
}

async function handleRestock() {
  if (!restockDose.value || restockAmount.value <= 0) return
  try {
    await scheduleStore.restockSupply(restockDose.value.supply_id, restockAmount.value)
    restockDose.value = null
    showToast(locale.value === 'pl' ? 'Uzupełniono' : 'Restocked')
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd' : 'Error')
  }
}

// Dose edit modal
const doseEditOpen = ref(false)
const doseEditTask = ref(null)
const doseForm = reactive({ name_pl: '', name: '', amount: '', unit: 'ml', time: '08:00', tankId: 1 })

function openDoseEdit(task) {
  doseEditTask.value = task
  if (task) {
    doseForm.name_pl = task.supply_name_pl ?? ''
    doseForm.name = task.supply_name ?? ''
    doseForm.amount = String(task.dose_amount ?? '')
    doseForm.unit = task.dose_unit ?? 'ml'
    doseForm.time = task.time_of_day ?? '08:00'
    doseForm.tankId = task.tank_id ?? tankStore.activeTankId
  } else {
    doseForm.name_pl = ''
    doseForm.name = ''
    doseForm.amount = ''
    doseForm.unit = 'ml'
    doseForm.time = '08:00'
    doseForm.tankId = tankStore.activeTankId
  }
  doseEditOpen.value = true
}

async function saveDose() {
  const data = {
    supply_name: doseForm.name,
    supply_name_pl: doseForm.name_pl,
    dose_amount: parseFloat(doseForm.amount) || 0,
    dose_unit: doseForm.unit,
    time_of_day: doseForm.time || null,
    tank_id: doseForm.tankId,
  }
  try {
    if (doseEditTask.value) {
      await scheduleStore.updateDosingTask(doseEditTask.value.id, data)
    } else {
      await scheduleStore.createDosingTask(data)
    }
    doseEditOpen.value = false
    showToast(locale.value === 'pl' ? 'Zapisano' : 'Saved')
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd zapisu' : 'Save error')
  }
}

function formatDate(s) {
  if (!s) return '—'
  return new Date(s).toLocaleDateString('pl-PL', {
    year: 'numeric', month: '2-digit', day: '2-digit',
  })
}

// ── LsEditModal form state ────────────────────────────────────
const lsFormName = ref('')
const lsFormLatin = ref('')
const lsFormQty = ref(1)
const lsFormDate = ref('')
const lsFormKind = ref('fish')
const lsFormStatus = ref('planned')
const lsConfirmDelete = ref(false)
const lsFormImg = ref('')
const lsFormTankId = ref(1)

watch(editModal, (val) => {
  if (!val) return
  const item = val.item
  lsFormName.value = item ? (item.name_pl || item.name_en || '') : ''
  lsFormLatin.value = item?.latin || ''
  lsFormQty.value = item?.qty || 1
  lsFormDate.value = item?.added_at
    ? item.added_at.slice(0, 10)
    : new Date().toISOString().slice(0, 10)
  lsFormKind.value = val.kind || 'fish'
  lsFormStatus.value = item?.status || 'planned'
  lsConfirmDelete.value = false
  lsFormImg.value = item?.img || ''
  lsFormTankId.value = item?.tank_id ?? tankStore.activeTankId
  obsadaStore.clearSearch()
})

async function searchImg() {
  const q = lsFormLatin.value || editModal.value?.item?.name_en || lsFormName.value
  if (!q) return
  await obsadaStore.searchImages(q, lsFormKind.value)
}

async function saveLs() {
  if (!editModal.value) return
  const data = {
    name_en: lsFormName.value,
    name_pl: lsFormName.value,
    latin: lsFormLatin.value,
    qty: parseInt(lsFormQty.value) || 1,
    added_at: lsFormDate.value,
    img: lsFormImg.value,
    tank_id: lsFormTankId.value,
    ...(lsFormKind.value === 'fish' && { status: lsFormStatus.value }),
  }
  const { item, kind } = editModal.value
  if (item?.id) {
    if (kind === 'fish') await obsadaStore.updateFish(item.id, data)
    else await obsadaStore.updatePlant(item.id, data)
  } else {
    if (kind === 'fish') await obsadaStore.addFish(data)
    else await obsadaStore.addPlant(data)
  }
  editModal.value = null
}

async function deleteLs() {
  if (!editModal.value?.item?.id) return
  const { item, kind } = editModal.value
  if (kind === 'fish') await obsadaStore.deleteFish(item.id)
  else await obsadaStore.deletePlant(item.id)
  editModal.value = null
}
</script>
