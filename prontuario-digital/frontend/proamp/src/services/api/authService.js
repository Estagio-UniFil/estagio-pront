import api from './baseService.js';

export const authService = {
    login: (email, password) => {
        return api.post('api/login/', { username: email, password });
    },
    logout: () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        return Promise.resolve();
    },
};
