import axios from "axios";
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://157.230.150.167:8000" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
