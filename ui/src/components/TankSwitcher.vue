<template>
  <div v-if="tankStore.tanks.length > 1" class="seg tank-switcher">
    <button
      v-for="t in tankStore.tanks"
      :key="t.id"
      :class="{ on: tankStore.activeTankId === t.id }"
      @click="tankStore.setActiveTank(t.id)"
    >
      {{ t.name }}
    </button>
  </div>
</template>

<script setup>
import { useTankSelectorStore } from '../stores/tankSelector'

const tankStore = useTankSelectorStore()
</script>

<style scoped>
.tank-switcher {
  margin-bottom: 12px;
}
</style>
