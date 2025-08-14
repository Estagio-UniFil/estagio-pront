import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const authToken = localStorage.getItem('token');
        if (authToken) {
            config.headers.Authorization = `Token ${authToken}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    },
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            //window.location.href = '/login';
            console.warn('Token inválido - usuário precisa fazer login novamente');
        }

        if (error.response?.status === 500) {
            console.error('Server error:', error.response.data);
        }
        return Promise.reject(error);
    },
);

export default api;
