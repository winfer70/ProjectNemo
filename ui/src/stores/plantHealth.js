import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const usePlantHealthStore = defineStore('plantHealth', () => {
  const deficiencies = ref([])
  const events = ref([])
  const scanning = ref(false)

  async function fetchDeficiencies() {
    if (deficiencies.value.length) return
    const r = await axios.get('/api/plant-health/deficiencies')
    deficiencies.value = r.data
  }

  async function fetchEvents(plantId = null) {
    const params = plantId ? { plant_id: plantId } : {}
    const r = await axios.get('/api/plant-health/events', { params })
    events.value = r.data
  }

  async function logEvent(plantId, deficiencyKey, notes = null) {
    const r = await axios.post('/api/plant-health/events', {
      plant_id: plantId, deficiency_key: deficiencyKey, notes,
    })
    events.value.unshift(r.data)
  }

  async function scanLeaf(plantId, file) {
    scanning.value = true
    try {
      const form = new FormData()
      form.append('file', file)
      const r = await axios.post('/api/plant-health/scan', form, {
        params: { plant_id: plantId },
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      events.value.unshift(r.data)
      return r.data
    } finally {
      scanning.value = false
    }
  }

  async function treatEvent(id, treatmentNotes = null) {
    const r = await axios.patch(`/api/plant-health/events/${id}/treat`, { treatment_notes: treatmentNotes })
    const idx = events.value.findIndex(e => e.id === id)
    if (idx !== -1) events.value[idx] = r.data
  }

  async function correctEvent(id, correctedKey, correctionNotes = null) {
    const r = await axios.patch(`/api/plant-health/events/${id}/correct`, {
      corrected_deficiency_key: correctedKey, correction_notes: correctionNotes,
    })
    const idx = events.value.findIndex(e => e.id === id)
    if (idx !== -1) events.value[idx] = r.data
  }

  return {
    deficiencies, events, scanning,
    fetchDeficiencies, fetchEvents,
    logEvent, scanLeaf, treatEvent, correctEvent,
  }
})
