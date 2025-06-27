import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const detectVideo = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post(`${API_BASE_URL}/detect/video`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const detectAudio = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post(`${API_BASE_URL}/detect/audio`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

