// v-resizable="'unique.tile.id'" - lets the user drag-resize a tile in
// "edit layout" mode (see stores/editMode.js) via CSS zoom, which scales
// text/icons/padding along with the box (unlike transform:scale). Persisted
// per-device in localStorage so it survives refresh but isn't tied to an
// account/server - each tablet/phone keeps its own layout.
import { useEditModeStore } from '../stores/editMode'

const STORAGE_KEY = 'nemo_tile_scale'
const MIN_SCALE = 0.5
const MAX_SCALE = 2

function readScales() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
  } catch {
    return {}
  }
}

function writeScale(id, scale) {
  const all = readScales()
  all[id] = scale
  localStorage.setItem(STORAGE_KEY, JSON.stringify(all))
}

export default {
  mounted(el, binding) {
    const id = binding.value
    if (!id) return

    const initial = readScales()[id]
    if (initial) el.style.zoom = String(initial)
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative'

    let handle = null
    let startY = 0
    let startScale = 1

    function onPointerMove(e) {
      const dy = e.clientY - startY
      const newScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, startScale + dy / 300))
      el.style.zoom = String(newScale)
    }
    function onPointerUp() {
      window.removeEventListener('pointermove', onPointerMove)
      window.removeEventListener('pointerup', onPointerUp)
      writeScale(id, parseFloat(el.style.zoom) || 1)
    }
    function onPointerDown(e) {
      e.preventDefault()
      e.stopPropagation()
      startY = e.clientY
      startScale = parseFloat(el.style.zoom) || 1
      window.addEventListener('pointermove', onPointerMove)
      window.addEventListener('pointerup', onPointerUp)
    }

    function addHandle() {
      if (handle) return
      handle = document.createElement('div')
      handle.className = 'tile-resize-handle'
      handle.innerHTML = '&#8600;'
      handle.title = 'Drag to resize'
      handle.addEventListener('pointerdown', onPointerDown)
      el.appendChild(handle)
    }
    function removeHandle() {
      if (!handle) return
      handle.removeEventListener('pointerdown', onPointerDown)
      handle.remove()
      handle = null
    }

    const editStore = useEditModeStore()
    if (editStore.enabled) addHandle()
    const stop = editStore.$subscribe(() => {
      if (editStore.enabled) addHandle()
      else removeHandle()
    })

    el._resizableCleanup = () => {
      stop()
      removeHandle()
    }
  },
  unmounted(el) {
    el._resizableCleanup?.()
  },
}
