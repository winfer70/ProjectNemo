import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useObsadaStore = defineStore('obsada', () => {
  const fish = ref([])
  const plants = ref([])
  const searchResults = ref(null)
  const searching = ref(false)

  async function fetchFish() {
    const r = await axios.get('/api/obsada/fish')
    fish.value = r.data
  }

  async function fetchPlants() {
    const r = await axios.get('/api/obsada/plants')
    plants.value = r.data
  }

  async function addFish(data) {
    const r = await axios.post('/api/obsada/fish', data)
    fish.value.push(r.data)
  }

  async function updateFish(id, data) {
    const r = await axios.put(`/api/obsada/fish/${id}`, data)
    const idx = fish.value.findIndex(f => f.id === id)
    if (idx !== -1) fish.value[idx] = r.data
  }

  async function deleteFish(id) {
    await axios.delete(`/api/obsada/fish/${id}`)
    fish.value = fish.value.filter(f => f.id !== id)
  }

  async function addPlant(data) {
    const r = await axios.post('/api/obsada/plants', data)
    plants.value.push(r.data)
  }

  async function updatePlant(id, data) {
    const r = await axios.put(`/api/obsada/plants/${id}`, data)
    const idx = plants.value.findIndex(p => p.id === id)
    if (idx !== -1) plants.value[idx] = r.data
  }

  async function deletePlant(id) {
    await axios.delete(`/api/obsada/plants/${id}`)
    plants.value = plants.value.filter(p => p.id !== id)
  }

  async function searchImages(query, type = 'fish') {
    searching.value = true
    searchResults.value = null
    try {
      const r = await axios.get('/api/obsada/search', { params: { q: query, type } })
      searchResults.value = r.data
    } finally {
      searching.value = false
    }
  }

  function clearSearch() {
    searchResults.value = null
  }

  return {
    fish, plants, searchResults, searching,
    fetchFish, fetchPlants,
    addFish, updateFish, deleteFish,
    addPlant, updatePlant, deletePlant,
    searchImages, clearSearch,
  }
})
