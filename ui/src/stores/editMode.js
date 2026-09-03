import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEditModeStore = defineStore('editMode', () => {
  const enabled = ref(false)
  function toggle() {
    enabled.value = !enabled.value
  }
  return { enabled, toggle }
})
