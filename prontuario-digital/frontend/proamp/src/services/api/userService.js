import api from './baseService';

export const userService = {
    async getUsers(params = {}) {
        // Get users with params for pagination
        const response = await api.get('api/auth/users/', { params });
        return response.data;
    },

    async getAllUsers() {
        const response = await api.get('api/auth/users/');
        return response.data;
    },

    async getAllHealthPros(params = {}) {
        const response = await api.get('api/managerview/', { params });
        return response.data;
    },

    async getUser(id) {
        const response = await api.get(`api/auth/users/${id}/`);
        return response.data;
    },

    async createUser(userData) {
        const response = await api.post('api/auth/users/', userData);
        return response.data;
    },

    async updateUser(id, userData) {
        const response = await api.patch(`api/auth/users/${id}/`, userData);
        return response.data;
    },

    async deleteUser(id) {
        const response = await api.delete(`api/auth/users/${id}/`);
        return response.data;
    },
};

export default userService;
