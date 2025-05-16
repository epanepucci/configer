// frontend/src/stores/configs.js
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { configsApi } from "../api"

export const useConfigsStore = defineStore("configs", () => {
  // State
  const currentConfig = ref({})
  const versions = ref([])
  const currentVersion = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Actions
  async function fetchConfig(instrumentId) {
    loading.value = true
    error.value = null
    try {
      const response = await configsApi.getConfig(instrumentId)
      currentConfig.value = response.data
    } catch (err) {
      error.value = err.message || "Failed to fetch configuration"
      console.error("Error fetching configuration:", err)
    } finally {
      loading.value = false
    }
  }
  
  async function updateConfig(instrumentId, configData, comment = "") {
    loading.value = true
    error.value = null
    try {
      const payload = {
        data: configData,
        comment
      }
      const response = await configsApi.updateConfig(instrumentId, payload)
      currentConfig.value = response.data.config
      return response.data
    } catch (err) {
      error.value = err.message || "Failed to update configuration"
      console.error("Error updating configuration:", err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function fetchVersions(instrumentId) {
    loading.value = true
    error.value = null
    try {
      const response = await configsApi.getVersions(instrumentId)
      versions.value = response.data
    } catch (err) {
      error.value = err.message || "Failed to fetch versions"
      console.error("Error fetching versions:", err)
    } finally {
      loading.value = false
    }
  }
  
  async function fetchVersion(instrumentId, versionId) {
    loading.value = true
    error.value = null
    try {
      const response = await configsApi.getVersion(instrumentId, versionId)
      currentVersion.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || "Failed to fetch version"
      console.error("Error fetching version:", err)
    } finally {
      loading.value = false
    }
  }
  
  // Reset store
  function resetState() {
    currentConfig.value = {}
    versions.value = []
    currentVersion.value = null
    error.value = null
  }
  
  return {
    // State
    currentConfig,
    versions,
    currentVersion,
    loading,
    error,
    
    // Actions
    fetchConfig,
    updateConfig,
    fetchVersions,
    fetchVersion,
    resetState
  }
})
