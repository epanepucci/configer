// frontend/src/stores/instruments.js
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { instrumentsApi } from "../api"

export const useInstrumentsStore = defineStore("instruments", () => {
  // State
  const instruments = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Getters
  const getInstrumentById = computed(() => {
    return (id) => instruments.value.find(instrument => instrument.id === id)
  })
  
  // Actions
  async function fetchInstruments() {
    loading.value = true
    error.value = null
    try {
      const response = await instrumentsApi.getAll()
      instruments.value = response.data.instruments
    } catch (err) {
      error.value = err.message || "Failed to fetch instruments"
      console.error("Error fetching instruments:", err)
    } finally {
      loading.value = false
    }
  }
  
  async function createInstrument(instrumentData) {
    loading.value = true
    error.value = null
    try {
      const response = await instrumentsApi.create(instrumentData)
      instruments.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message || "Failed to create instrument"
      console.error("Error creating instrument:", err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  return {
    // State
    instruments,
    loading,
    error,
    
    // Getters
    getInstrumentById,
    
    // Actions
    fetchInstruments,
    createInstrument
  }
})
