<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-sheet obsada-modal">
      <div class="modal-title">
        {{ editItem ? $t('obsada.edit') : (type === 'fish' ? $t('obsada.addFish') : $t('obsada.addPlant')) }}
      </div>

      <!-- Search row -->
      <div class="obsada-search-row">
        <input
          v-model="form.name_en"
          :placeholder="$t('obsada.searchPlaceholder')"
          class="obsada-input obsada-input-grow"
        />
        <button class="btn btn-secondary obsada-search-btn" @click="doSearch" :disabled="store.searching">
          {{ store.searching ? '...' : $t('obsada.search') }}
        </button>
      </div>

      <!-- Wikipedia extract -->
      <div v-if="store.searchResults?.wiki_extract" class="obsada-extract">
        <span class="obsada-extract-label">{{ store.searchResults.scientific_name }}</span>
        {{ store.searchResults.wiki_extract }}
        <a v-if="store.searchResults.wiki_url" :href="store.searchResults.wiki_url" target="_blank" class="obsada-wiki-link">Wikipedia ↗</a>
      </div>

      <!-- Image picker -->
      <div v-if="store.searchResults?.images?.length" class="obsada-image-grid">
        <img
          v-for="(img, i) in store.searchResults.images"
          :key="i"
          :src="img.thumb || img.url"
          class="obsada-img-thumb"
          :class="{ selected: form.img === img.url }"
          @click="form.img = img.url"
          loading="lazy"
        />
      </div>

      <!-- Selected image preview -->
      <div v-if="form.img" class="obsada-preview-row">
        <img :src="form.img" class="obsada-preview-img" />
        <button class="btn btn-secondary btn-sm" @click="form.img = null">{{ $t('obsada.selectImage') }}</button>
      </div>

      <!-- Fields -->
      <div class="obsada-fields">
        <input v-model="form.name_pl"  :placeholder="locale === 'pl' ? 'Nazwa PL' : 'PL name'"   class="obsada-input" />
        <input v-model="form.latin"    placeholder="Łacińska / Latin"                             class="obsada-input obsada-italic" />
        <div class="obsada-fields-row">
          <input v-model.number="form.qty" type="number" min="1" :placeholder="$t('obsada.qty')"   class="obsada-input obsada-input-sm" />
          <input v-if="type === 'fish'" v-model="form.zone"     :placeholder="$t('obsada.zone')"   class="obsada-input" />
          <input v-if="type === 'plant'" v-model="form.location" placeholder="Location"            class="obsada-input" />
        </div>
        <input v-if="type === 'fish'" v-model="form.temp" placeholder="Temp range e.g. 24–28°C"   class="obsada-input" />
        <select v-if="type === 'fish'" v-model="form.status" class="obsada-input obsada-select">
          <option value="in_tank">{{ $t('obsada.in_tank') }}</option>
          <option value="planned">{{ $t('obsada.planned') }}</option>
        </select>
        <textarea v-model="form.notes_pl" :placeholder="locale === 'pl' ? 'Notatki PL' : 'Notes PL'" class="obsada-textarea" rows="2" />
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" style="flex:1" @click="$emit('close')">{{ $t('maintenance.cancel') }}</button>
        <button class="btn btn-primary" style="flex:1" @click="save">{{ $t('maintenance.confirm') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useObsadaStore } from '../stores/obsada'

const { locale } = useI18n()
const store = useObsadaStore()

const props = defineProps({
  type: { type: String, default: 'fish' },  // 'fish' | 'plant'
  editItem: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const form = reactive({
  name_en: '',
  name_pl: null,
  latin: null,
  qty: 1,
  zone: null,
  location: null,
  status: 'in_tank',
  temp: null,
  notes_pl: null,
  img: null,
})

// Pre-fill on edit
watch(() => props.editItem, (item) => {
  if (!item) return
  Object.assign(form, {
    name_en: item.name_en || '',
    name_pl: item.name_pl || null,
    latin: item.latin || null,
    qty: item.qty || 1,
    zone: item.zone || null,
    location: item.location || null,
    status: item.status || 'in_tank',
    temp: item.temp || null,
    notes_pl: item.notes_pl || null,
    img: item.img || null,
  })
}, { immediate: true })

async function doSearch() {
  if (!form.name_en.trim()) return
  await store.searchImages(form.name_en.trim(), props.type)
  if (store.searchResults?.scientific_name && !form.latin) {
    form.latin = store.searchResults.scientific_name
  }
  // Auto-select first image if none chosen yet
  if (!form.img && store.searchResults?.images?.length) {
    form.img = store.searchResults.images[0].url
  }
}

async function save() {
  const payload = {
    name_en: form.name_en,
    name_pl: form.name_pl || null,
    latin: form.latin || null,
    qty: form.qty || 1,
    notes_pl: form.notes_pl || null,
    img: form.img || null,
  }
  if (props.type === 'fish') {
    Object.assign(payload, { zone: form.zone || null, status: form.status, temp: form.temp || null })
  } else {
    Object.assign(payload, { location: form.location || null })
  }

  if (props.editItem) {
    if (props.type === 'fish') await store.updateFish(props.editItem.id, payload)
    else await store.updatePlant(props.editItem.id, payload)
  } else {
    if (props.type === 'fish') await store.addFish(payload)
    else await store.addPlant(payload)
  }

  store.clearSearch()
  emit('saved')
  emit('close')
}
</script>

<style scoped>
.obsada-modal {
  max-height: 90vh;
  overflow-y: auto;
}

.obsada-search-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
.obsada-input {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  padding: 8px 10px;
  font-size: 13px;
  width: 100%;
}
.obsada-input-grow { flex: 1; }
.obsada-input-sm   { width: 80px; flex-shrink: 0; }
.obsada-italic     { font-style: italic; }
.obsada-select     { cursor: pointer; }
.obsada-search-btn { white-space: nowrap; }

.obsada-extract {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  background: rgba(0,180,216,0.06);
  border-radius: 6px;
  padding: 8px 10px;
  margin-bottom: 8px;
}
.obsada-extract-label {
  display: block;
  font-style: italic;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 4px;
}
.obsada-wiki-link {
  display: inline-block;
  margin-top: 4px;
  color: var(--accent);
  font-size: 11px;
  text-decoration: none;
}

.obsada-image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 8px;
}
.obsada-img-thumb {
  width: 100%;
  aspect-ratio: 4/3;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.15s;
}
.obsada-img-thumb.selected {
  border-color: var(--accent);
}

.obsada-preview-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.obsada-preview-img {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

.obsada-fields {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}
.obsada-fields-row {
  display: flex;
  gap: 8px;
}
.obsada-textarea {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  padding: 8px 10px;
  font-size: 13px;
  resize: none;
  width: 100%;
}
</style>
