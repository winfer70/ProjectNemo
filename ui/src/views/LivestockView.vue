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
        <div style="padding:16px;overflow-y:auto;flex:1">
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
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">
              <div
                v-for="img in obsadaStore.searchResults.images"
                :key="img.url"
                style="aspect-ratio:1;border-radius:8px;overflow:hidden;cursor:pointer;border:2px solid transparent"
                :style="{ borderColor: lsFormImg === img.url ? 'var(--accent)' : 'transparent' }"
                @click="lsFormImg = img.url"
              >
                <img :src="img.thumb || img.url" style="width:100%;height:100%;object-fit:cover">
              </div>
            </div>
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
</template>

<script setup>
import { useObsadaStore } from '../stores/obsada'
import { useI18n } from 'vue-i18n'
import { ref, computed, onMounted, watch } from 'vue'

const { locale } = useI18n()
const obsadaStore = useObsadaStore()

// ── UI state ──────────────────────────────────────────────────
const statusPicker = ref(null)   // id of item showing status picker
const editModal = ref(null)      // null | { item: fish|plant|null, kind: 'fish'|'plant' }

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
const fish = computed(() => obsadaStore.fish.map(f => ({ ...f, kind: 'fish' })))
const plants = computed(() => obsadaStore.plants.map(p => ({ ...p, kind: 'plant' })))

onMounted(() => {
  obsadaStore.fetchFish()
  obsadaStore.fetchPlants()
})

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
  obsadaStore.clearSearch()
})

async function searchImg() {
  const q = lsFormName.value || lsFormLatin.value
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
