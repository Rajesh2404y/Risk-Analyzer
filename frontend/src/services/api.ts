import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle authentication errors (401) and JWT validation errors (422)
    // 422 occurs when Flask-JWT-Extended receives an invalid/malformed token
    if (error.response?.status === 401 || error.response?.status === 422) {
      // Only redirect if we're not already on auth pages and have a token stored
      const token = localStorage.getItem('token');
      const isAuthEndpoint = error.config?.url?.includes('/auth/');
      
      if (token && !isAuthEndpoint) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (email: string, password: string, full_name: string) =>
    api.post('/auth/register', { email, password, full_name }),
  getCurrentUser: () => api.get('/auth/me'),
  changePassword: (current_password: string, new_password: string) =>
    api.post('/auth/change-password', { current_password, new_password }),
  getPreferences: () => api.get('/auth/preferences'),
  updatePreferences: (data: Record<string, unknown>) =>
    api.put('/auth/preferences', data),
};

export const transactionsAPI = {
  getTransactions: (params?: Record<string, unknown>) =>
    api.get('/transactions', { params }),
  createTransaction: (data: Record<string, unknown>) =>
    api.post('/transactions', data),
  updateTransaction: (id: number, data: Record<string, unknown>) =>
    api.put(`/transactions/${id}`, data),
  deleteTransaction: (id: number) => api.delete(`/transactions/${id}`),
};

export const analyticsAPI = {
  getSummary: (params?: Record<string, unknown>) =>
    api.get('/analytics/summary', { params }),
  getTrends: (params?: Record<string, unknown>) =>
    api.get('/analytics/trends', { params }),
  getCategoryBreakdown: (params?: Record<string, unknown>) =>
    api.get('/analytics/category-breakdown', { params }),
  getComparison: () => api.get('/analytics/comparison'),
};

export const predictionsAPI = {
  getPredictions: (months: number = 3) =>
    api.get('/predictions/expenses', { params: { months } }),
  getCategoryPredictions: (months: number = 3) =>
    api.get('/predictions/by-category', { params: { months } }),
};

export const recommendationsAPI = {
  getRecommendations: () => api.get('/recommendations'),
  sendAlertEmail: () => api.post('/recommendations/send-alerts'),
};

export const riskAPI = {
  getRiskScore: () => api.get('/risk/score'),
};

export const categoriesAPI = {
  getCategories: () => api.get('/categories'),
  createCategory: (data: Record<string, unknown>) =>
    api.post('/categories', data),
  updateCategory: (id: number, data: Record<string, unknown>) =>
    api.put(`/categories/${id}`, data),
  deleteCategory: (id: number) => api.delete(`/categories/${id}`),
};

export const budgetsAPI = {
  getBudgets: () => api.get('/budgets'),
  createBudget: (data: Record<string, unknown>) =>
    api.post('/budgets', data),
  updateBudget: (id: number, data: Record<string, unknown>) =>
    api.put(`/budgets/${id}`, data),
  deleteBudget: (id: number) => api.delete(`/budgets/${id}`),
};

export const uploadAPI = {
  uploadFile: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  confirmTransactions: (uploadId: number, transactions: Record<string, unknown>[]) =>
    api.post('/upload/confirm', { upload_id: uploadId, transactions }),
  getUploadHistory: () => api.get('/upload/history'),
  deleteUpload: (id: number) => api.delete(`/upload/${id}`),
};

export default api;
