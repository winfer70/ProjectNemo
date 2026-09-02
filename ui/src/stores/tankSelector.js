import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useSensorsStore } from './sensors'

const STORAGE_KEY = 'nemo_active_tank'

export const useTankSelectorStore = defineStore('tankSelector', () => {
  const sensorsStore = useSensorsStore()

  const activeTankId = ref(Number(localStorage.getItem(STORAGE_KEY)) || 1)

  watch(activeTankId, (val) => localStorage.setItem(STORAGE_KEY, String(val)))

  // Sourced from /api/sensors/current's tanks array (already fetched by
  // sensorsStore) so names/ids stay in sync with backend config - no
  // separate fetch, no hardcoded tank list.
  const tanks = computed(() => {
    const t = sensorsStore.current?.tanks
    return t?.length ? t.map((x) => ({ id: Number(x.id), name: x.name })) : [{ id: 1, name: 'Tank 1' }]
  })

  function setActiveTank(id) {
    activeTankId.value = Number(id)
  }

  // Items predate multi-tank support and were backfilled to tank_id=1 - treat
  // missing tank_id as tank 1 rather than hiding them from every filtered view.
  function matchesActiveTank(item) {
    return (item.tank_id ?? 1) === activeTankId.value
  }

  return { activeTankId, tanks, setActiveTank, matchesActiveTank }
})
