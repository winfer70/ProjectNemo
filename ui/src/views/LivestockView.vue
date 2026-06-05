<template>
  <div class="ls-container">

    <!-- ── Fish section ──────────────────────────────────────────── -->
    <div class="ls-section-header">
      <span class="ls-section-title">{{ locale === 'pl' ? 'Ryby' : 'Fish' }}</span>
      <span class="badge ls-count-badge">{{ store.fish.length }} {{ locale === 'pl' ? 'gatunków' : 'species' }}</span>
      <button class="btn btn-primary ls-add-btn" @click="openAdd('fish')">+</button>
    </div>

    <div v-for="fish in store.fish" :key="fish.id" class="card ls-fish-card">
      <div class="ls-media-row">
        <img v-if="fish.img" :src="fish.img" :alt="fish.latin" class="ls-thumb" loading="lazy" />
        <div v-else class="ls-thumb ls-thumb-placeholder"></div>
        <div class="ls-media-body">
          <div class="ls-card-top">
            <div class="ls-card-name-block">
              <div class="ls-name">{{ locale === 'pl' && fish.name_pl ? fish.name_pl : fish.name_en }}</div>
              <div class="ls-latin">{{ fish.latin }}</div>
            </div>
            <span class="badge" :class="statusBadgeClass(fish.status)">{{ statusLabel(fish.status) }}</span>
          </div>
          <div class="ls-badges-row">
            <span class="badge ls-badge-qty">× {{ fish.qty }}</span>
            <span v-if="fish.zone" class="badge ls-badge-zone">{{ fish.zone }}</span>
            <span v-if="fish.temp" class="badge ls-badge-temp">🌡 {{ fish.temp }}</span>
          </div>
          <div v-if="fish.notes_pl" class="ls-notes">{{ fish.notes_pl }}</div>
        </div>
        <div class="ls-card-actions">
          <button class="ls-action-btn" @click="openEdit('fish', fish)">✏️</button>
          <button class="ls-action-btn ls-action-del" @click="confirmDelete('fish', fish)">🗑</button>
        </div>
      </div>
    </div>

    <!-- ── Plants section ───────────────────────────────────────── -->
    <div class="ls-section-header ls-section-gap">
      <span class="ls-section-title">{{ locale === 'pl' ? 'Rośliny' : 'Plants' }}</span>
      <span class="badge ls-count-badge">{{ store.plants.length }} {{ locale === 'pl' ? 'gatunków' : 'species' }}</span>
      <button class="btn btn-primary ls-add-btn" @click="openAdd('plant')">+</button>
    </div>

    <div v-for="plant in store.plants" :key="plant.id" class="card ls-plant-card">
      <div class="ls-media-row">
        <img v-if="plant.img" :src="plant.img" :alt="plant.latin" class="ls-thumb" loading="lazy" />
        <div v-else class="ls-thumb ls-thumb-placeholder"></div>
        <div class="ls-media-body">
          <div class="ls-card-top">
            <div class="ls-card-name-block">
              <div class="ls-name">{{ locale === 'pl' && plant.name_pl ? plant.name_pl : plant.name_en }}</div>
              <div class="ls-latin">{{ plant.latin }}</div>
            </div>
            <span v-if="plant.location" class="badge ls-badge-location">{{ plant.location }}</span>
          </div>
          <div v-if="plant.notes_pl" class="ls-notes">{{ plant.notes_pl }}</div>
        </div>
        <div class="ls-card-actions">
          <button class="ls-action-btn" @click="openEdit('plant', plant)">✏️</button>
          <button class="ls-action-btn ls-action-del" @click="confirmDelete('plant', plant)">🗑</button>
        </div>
      </div>
    </div>

    <!-- ── Delete confirmation banner ───────────────────────────── -->
    <div v-if="pendingDelete" class="banner-danger">
      <span>{{ $t('obsada.confirmDelete') }}: <strong>{{ pendingDelete.item.name_en }}</strong></span>
      <div style="display:flex;gap:8px;margin-top:8px;">
        <button class="btn btn-secondary btn-sm" @click="pendingDelete = null">{{ $t('maintenance.cancel') }}</button>
        <button class="btn btn-danger btn-sm" @click="doDelete">{{ $t('obsada.delete') }}</button>
      </div>
    </div>

  </div>

  <!-- ── Modal ────────────────────────────────────────────────── -->
  <ObsadaAddModal
    v-if="modal.open"
    :type="modal.type"
    :edit-item="modal.editItem"
    @close="closeModal"
    @saved="closeModal"
  />
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useObsadaStore } from '../stores/obsada'
import ObsadaAddModal from '../components/ObsadaAddModal.vue'

const { locale } = useI18n()
const store = useObsadaStore()

const modal = reactive({ open: false, type: 'fish', editItem: null })
const pendingDelete = ref(null)

onMounted(async () => {
  await Promise.all([store.fetchFish(), store.fetchPlants()])
})

function openAdd(type) {
  modal.type = type
  modal.editItem = null
  modal.open = true
}

function openEdit(type, item) {
  modal.type = type
  modal.editItem = item
  modal.open = true
}

function closeModal() {
  modal.open = false
  modal.editItem = null
  store.clearSearch()
}

function confirmDelete(type, item) {
  pendingDelete.value = { type, item }
}

async function doDelete() {
  if (!pendingDelete.value) return
  const { type, item } = pendingDelete.value
  if (type === 'fish') await store.deleteFish(item.id)
  else await store.deletePlant(item.id)
  pendingDelete.value = null
}

function statusLabel(status) {
  const labels = locale.value === 'pl'
    ? { in_tank: '✅ W akwarium', planned: '🛒 Planowane' }
    : { in_tank: '✅ In tank',    planned: '🛒 Planned' }
  return labels[status] ?? status
}

function statusBadgeClass(status) {
  return status === 'in_tank' ? 'ls-status-green' : 'ls-status-blue'
}
</script>

<style scoped>
.ls-container {
  padding-bottom: 8px;
}

.ls-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.ls-section-gap {
  margin-top: 16px;
}
.ls-section-title {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}
.ls-count-badge {
  background: rgba(0, 180, 216, 0.12);
  color: var(--accent);
  border: 1px solid rgba(0, 180, 216, 0.25);
}
.ls-add-btn {
  margin-left: auto;
  padding: 2px 12px;
  font-size: 18px;
  line-height: 1.3;
  min-width: 32px;
}

.ls-fish-card,
.ls-plant-card {
  margin-bottom: 8px;
}

.ls-media-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.ls-thumb {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}
.ls-thumb-placeholder {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
}
.ls-media-body {
  flex: 1;
  min-width: 0;
}

.ls-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}
.ls-card-name-block {
  flex: 1;
  min-width: 0;
}
.ls-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
}
.ls-latin {
  font-size: 11px;
  font-style: italic;
  color: var(--text-muted);
  margin-top: 2px;
}

.ls-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.ls-badge-qty {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text);
  border: 1px solid var(--border);
  font-weight: 700;
}
.ls-badge-zone {
  background: rgba(72, 202, 228, 0.10);
  color: var(--accent2);
  border: 1px solid rgba(72, 202, 228, 0.20);
}
.ls-badge-temp {
  background: rgba(230, 57, 70, 0.10);
  color: #f4a261;
  border: 1px solid rgba(230, 57, 70, 0.20);
}
.ls-badge-location {
  background: rgba(46, 196, 182, 0.10);
  color: var(--ok);
  border: 1px solid rgba(46, 196, 182, 0.20);
  white-space: nowrap;
}

.ls-status-green {
  background: rgba(46, 196, 182, 0.15);
  color: var(--ok);
  border: 1px solid rgba(46, 196, 182, 0.30);
  white-space: nowrap;
  flex-shrink: 0;
}
.ls-status-blue {
  background: rgba(0, 180, 216, 0.15);
  color: var(--accent);
  border: 1px solid rgba(0, 180, 216, 0.30);
  white-space: nowrap;
  flex-shrink: 0;
}

.ls-notes {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}

.ls-card-actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
}
.ls-action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 4px;
  border-radius: 4px;
  opacity: 0.6;
  transition: opacity 0.15s;
}
.ls-action-btn:hover { opacity: 1; }
.ls-action-del:hover { color: var(--danger, #e63946); }

.banner-danger {
  background: rgba(230, 57, 70, 0.10);
  border: 1px solid rgba(230, 57, 70, 0.30);
  border-radius: 8px;
  padding: 12px;
  margin-top: 8px;
  font-size: 13px;
  color: var(--text);
}
.btn-danger {
  background: rgba(230, 57, 70, 0.80);
  color: #fff;
}
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}
</style>
