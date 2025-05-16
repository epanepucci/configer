// frontend/src/api/index.js
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json"
  }
})

export const instrumentsApi = {
  getAll: () => api.get("/instruments"),
  getById: (id) => api.get(`/instruments/${id}`),
  create: (data) => api.post("/instruments", data)
}

export const configsApi = {
  getConfig: (instrumentId) => api.get(`/configs/${instrumentId}`),
  updateConfig: (instrumentId, data) => api.put(`/configs/${instrumentId}`, data),
  getVersions: (instrumentId) => api.get(`/configs/${instrumentId}/versions`),
  getVersion: (instrumentId, versionId) => api.get(`/configs/${instrumentId}/versions/${versionId}`)
}

export const snapshotsApi = {
  createSnapshot: (instrumentId, data) => api.post(`/snapshots/${instrumentId}`, data),
  getSnapshots: (instrumentId) => api.get(`/snapshots/${instrumentId}`),
  getSnapshot: (instrumentId, snapshotName) => api.get(`/snapshots/${instrumentId}/${snapshotName}`)
}

export default api
