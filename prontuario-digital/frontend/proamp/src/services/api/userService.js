import api from './baseService';

export const userService = {
    async getUsers() {
        const response = await api.get('api/auth/users/');
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
        const response = await api.put(`api/auth/users/${id}/`, userData);
        return response.data;
    },

    async deleteUser(id) {
        const response = await api.delete(`api/auth/users/${id}/`);
        return response.data;
    },
};
