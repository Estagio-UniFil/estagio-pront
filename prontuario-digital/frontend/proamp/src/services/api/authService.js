import api from './baseService.js';

export const authService = {
    // Get CSRF token before login
    async getCsrfToken() {
        try {
            const response = await api.get('csrf/');
            return response.data.csrfToken;
        } catch (error) {
            console.error('Erro ao obter CSRF token:', error);
            return null;
        }
    },

    // Sessions login
    async login(email, password, rememberMe = false) {
        try {
            // Guarantee CSRF token
            await this.getCsrfToken();

            // Login
            const response = await api.post('login/', {
                email: email,
                password: password,
                remember_me: rememberMe,
            });

            return response;
        } catch (error) {
            console.error('Erro no login:', error);
            throw error;
        }
    },

    // Logout
    async logout() {
        try {
            await api.post('logout/');
            localStorage.removeItem('user');
        } catch (error) {
            console.error('Erro no logout:', error);
            localStorage.removeItem('user');
            throw error;
        }
    },

    async checkAuth() {
        try {
            const response = await api.get('check-auth/');
            return response;
        } catch (error) {
            return { error: error, data: { is_authenticated: false } };
        }
    },

    async getUserLogged() {
        try {
            const response = await api.get('api/auth/users/me/');
            return response.data;
        } catch (error) {
            console.error('Erro:', error);
            throw error;
        }
    },

    async patchUserLogged(userData) {
        try {
            const response = await api.patch('api/auth/users/me/', userData);
            return response.data;
        } catch (error) {
            console.error('Erro:', error);
            throw error;
        }
    },

    async setPassword(passwordData) {
        try {
            const response = await api.post('api/auth/users/set-password/', passwordData);
            return response.data;
        } catch (error) {
            console.error('Erro ao definir senha:', error);
            throw error;
        }
    },

    // User data from localStorage
    getCurrentUser() {
        const userData = localStorage.getItem('user');
        return userData ? JSON.parse(userData) : null;
    },
};
