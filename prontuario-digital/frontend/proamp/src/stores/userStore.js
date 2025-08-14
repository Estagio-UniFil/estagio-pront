// src/stores/userStore.js
import { defineStore } from 'pinia';
import { userService } from '@/services/api/userService';

export const useUserStore = defineStore('user', {
    state: () => ({
        users: [],
        loading: false,
        error: null,
        pagination: {
            currentPage: 1,
            totalPages: 1,
            total: 0,
            from: 0,
            to: 0,
        },
    }),

    getters: {
        getUserById: (state) => (id) => {
            return state.users.find((user) => user.id === id);
        },

        getUsersByRole: (state) => (role) => {
            return state.users.filter((user) => user.role === role);
        },
    },

    actions: {
        async fetchUsers() {
            this.loading = true;
            this.error = null;

            try {
                const response = await userService.getUsers();

                // Se a resposta for um array simples (sem paginação)
                if (Array.isArray(response)) {
                    this.users = response;
                    this.pagination = {
                        currentPage: 1,
                        totalPages: 1,
                        total: response.length,
                        from: 1,
                        to: response.length,
                    };
                } else {
                    // Se tiver paginação do DRF
                    this.users = response.results || response;
                    this.pagination = {
                        currentPage: 1,
                        totalPages: Math.ceil((response.count || response.length) / 10),
                        total: response.count || response.length,
                        from: 1,
                        to: response.results?.length || response.length,
                    };
                }
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao carregar usuários';
                console.error('Erro ao buscar usuários:', error);
            } finally {
                this.loading = false;
            }
        },

        async createUser(userData) {
            this.loading = true;
            this.error = null;

            try {
                const newUser = await userService.createUser(userData);
                this.users.unshift(newUser);
                return newUser;
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao criar usuário';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async updateUser(id, userData) {
            this.loading = true;
            this.error = null;

            try {
                const updatedUser = await userService.updateUser(id, userData);
                const index = this.users.findIndex((user) => user.id === id);
                if (index !== -1) {
                    this.users[index] = updatedUser;
                }
                return updatedUser;
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao atualizar usuário';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async deleteUser(id) {
            this.loading = true;
            this.error = null;

            try {
                await userService.deleteUser(id);
                this.users = this.users.filter((user) => user.id !== id);
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao excluir usuário';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        clearError() {
            this.error = null;
        },
    },
});
