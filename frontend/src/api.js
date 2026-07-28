import axios from "axios";

const API_BASE = "/api";

const api = axios.create({
  baseURL: API_BASE,
});

// Single prediction
export const predictSingle = (data) =>
  api.post("/predict/", data);

// Batch prediction
export const predictBatch = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/predict/batch", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

// History
export const getHistory = (limit = 50, offset = 0, filterType = null) => {
  let url = `/predict/history?limit=${limit}&offset=${offset}`;
  if (filterType) url += `&filter_type=${filterType}`;
  return api.get(url);
};

export const getHistoryCount = (filterType = null) => {
  let url = "/predict/history/count";
  if (filterType) url += `?filter_type=${filterType}`;
  return api.get(url);
};

export const getHistoryStats = () => api.get("/predict/history/stats");

export const deletePrediction = (id) => api.delete(`/predict/history/${id}`);

export const clearHistory = () => api.delete("/predict/history");

export const exportHistory = () =>
  api.get("/predict/export", { responseType: "blob" });

// Dashboard
export const getMetrics = () => api.get("/dashboard/metrics");

export const getCharts = () => api.get("/dashboard/charts");

export const getRechartsData = () => api.get("/dashboard/recharts");

export const getDatasetInfo = () => api.get("/dashboard/dataset");

// Model
export const retrainModel = () => api.post("/model/retrain");

export const healthCheck = () => api.get("/health");

export default api;
