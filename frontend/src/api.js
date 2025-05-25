import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8800', // Cambia este valor si tu backend usa otro puerto
  withCredentials: true, // Si usas JWT en cookies
});

// Interceptor para agregar el token a cada solicitud
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default api;
