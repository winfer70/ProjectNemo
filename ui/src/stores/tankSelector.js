import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useSensorsStore } from './sensors'

const STORAGE_KEY = 'nemo_active_tank'
const VIEW_MODE_KEY = 'nemo_tank_view_mode'

export const useTankSelectorStore = defineStore('tankSelector', () => {
  const sensorsStore = useSensorsStore()

  const activeTankId = ref(Number(localStorage.getItem(STORAGE_KEY)) || 1)
  // 'single' = one tank's tiles shown at a time (Lighting/Maintenance/Plugs
  // always follow this regardless of viewMode). 'combined' additionally
  // renders the Dzisiaj (Today) section as one tile per tank side by side -
  // scoped to Dzisiaj only, per user's explicit request.
  const viewMode = ref(localStorage.getItem(VIEW_MODE_KEY) || 'single')

  watch(activeTankId, (val) => localStorage.setItem(STORAGE_KEY, String(val)))
  watch(viewMode, (val) => localStorage.setItem(VIEW_MODE_KEY, val))

  // Sourced from /api/sensors/current's tanks array (already fetched by
  // sensorsStore) so names/ids stay in sync with backend config - no
  // separate fetch, no hardcoded tank list.
  const tanks = computed(() => {
    const t = sensorsStore.current?.tanks
    return t?.length ? t.map((x) => ({ id: Number(x.id), name: x.name })) : [{ id: 1, name: 'Tank 1' }]
  })

  function setActiveTank(id) {
    activeTankId.value = Number(id)
    viewMode.value = 'single'
  }

  function setCombinedView() {
    viewMode.value = 'combined'
  }

  // Items predate multi-tank support and were backfilled to tank_id=1 - treat
  // missing tank_id as tank 1 rather than hiding them from every filtered view.
  function matchesActiveTank(item) {
    return (item.tank_id ?? 1) === activeTankId.value
  }

  return { activeTankId, viewMode, tanks, setActiveTank, setCombinedView, matchesActiveTank }
})
