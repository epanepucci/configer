// frontend/src/stores/snapshots.js
import { defineStore } from "pinia"
import { ref } from "vue"
import { snapshotsApi } from "../api"

export const useSnapshotsStore = defineStore("snapshots", () => {
  // State
  const snapshots = ref([])
  const currentSnapshot = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Actions
  async function fetchSnapshots(instrumentId) {
    loading.value = true
    error.value = null
    try {
      const response = await snapshotsApi.getSnapshots(instrumentId)
      snapshots.value = response.data
    } catch (err) {
      error.value = err.message || "Failed to fetch snapshots"
      console.error("Error fetching snapshots:", err)
    } finally {
      loading.value = false
    }
  }
  
  async function fetchSnapshot(instrumentId, snapshotName) {
    loading.value = true
    error.value = null
    try {
      const response = await snapshotsApi.getSnapshot(instrumentId, snapshotName)
      currentSnapshot.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || "Failed to fetch snapshot"
      console.error("Error fetching snapshot:", err)
    } finally {
      loading.value = false
    }
  }
  
  async function createSnapshot(instrumentId, snapshotData) {
    loading.value = true
    error.value = null
    try {
      const response = await snapshotsApi.createSnapshot(instrumentId, snapshotData)
      await fetchSnapshots(instrumentId) // Refresh the list
      return response.data
    } catch (err) {
      error.value = err.message || "Failed to create snapshot"
      console.error("Error creating snapshot:", err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // Reset store
  function resetState() {
    snapshots.value = []
    currentSnapshot.value = null
    error.value = null
  }
  
  return {
    // State
    snapshots,
    currentSnapshot,
    loading,
    error,
    
    // Actions
    fetchSnapshots,
    fetchSnapshot,
    createSnapshot,
    resetState
  }
})
