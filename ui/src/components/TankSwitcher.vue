<template>
  <div v-if="tankStore.tanks.length > 1" class="seg tank-switcher">
    <button
      v-for="t in tankStore.tanks"
      :key="t.id"
      :class="{ on: tankStore.viewMode === 'single' && tankStore.activeTankId === t.id }"
      @click="tankStore.setActiveTank(t.id)"
    >
      {{ t.name }}
    </button>
    <button
      v-if="allowCombined"
      :class="{ on: tankStore.viewMode === 'combined' }"
      @click="tankStore.setCombinedView()"
    >
      {{ locale === 'pl' ? 'Oba' : 'Both' }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useTankSelectorStore } from '../stores/tankSelector'

defineProps({
  allowCombined: { type: Boolean, default: false },
})

const { locale } = useI18n()
const tankStore = useTankSelectorStore()
</script>

<style scoped>
.tank-switcher {
  margin-bottom: 12px;
}
</style>
