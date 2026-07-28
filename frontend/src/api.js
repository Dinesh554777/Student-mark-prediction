import axios from "axios";

const API_BASE = "/api";

const api = axios.create({
  baseURL: API_BASE,
});

export const predictSingle = (studyHours) =>
  api.post("/predict/", { study_hours: studyHours });

export const predictBatch = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/predict/batch", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getHistory = (limit = 50, offset = 0) =>
  api.get(`/predict/history?limit=${limit}&offset=${offset}`);

export const getHistoryCount = () => api.get("/predict/history/count");

export const getMetrics = () => api.get("/dashboard/metrics");

export const getCharts = () => api.get("/dashboard/charts");

export const getDatasetInfo = () => api.get("/dashboard/dataset");

export const retrainModel = () => api.post("/model/retrain");

export const healthCheck = () => api.get("/health");

export default api;
