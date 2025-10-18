// src/stores/userStore.js
import { defineStore } from 'pinia';
import { userService } from '@/services/api/userService';

export const useUserStore = defineStore('user', {
    state: () => ({
        users: [],
        pros: [],
        user: [],
        loading: false,
        error: null,
        pagination: {
            currentPage: 1,
            totalPages: 1,
            total: 0,
            from: 0,
            to: 0,
            pageSize: 10,
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
                const response = await userService.getAllUsers();
                // No pagination
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
                    // DRF paginations
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

        async fetchUserById(id) {
            try {
                const response = await userService.getUser(id);
                this.user = response.data;
                return response.data;
            } catch (e) {
                this.error = e.response?.data?.message || 'Erro ao carregar usuário';
            }
        },

        async fetchAllHealthPros(page = 1) {
            this.loading = true;
            this.error = null;

            try {
                const offset = (page - 1) * this.pagination.pageSize;
                const params = {
                    limit: this.pagination.pageSize,
                    offset: offset,
                };

                const response = await userService.getAllHealthPros(params);

                // Resposta paginada do DRF
                this.pros = response || [];
                this.pagination = {
                    currentPage: page,
                    totalPages: Math.ceil(response.count / this.pagination.pageSize),
                    total: response.count,
                    from: offset + 1,
                    to: offset + (response.results?.length || 0),
                    pageSize: this.pagination.pageSize,
                };
                console.log(this.pros.length);
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao carregar usuários';
                console.error('Erro ao buscar usuários:', error);
            } finally {
                this.loading = false;
            }
        },

        async goToPage(page) {
            if (page >= 1 && page <= this.pagination.totalPages) {
                await this.fetchUsers(page);
            }
        },

        async nextPage() {
            if (this.pagination.currentPage < this.pagination.totalPages) {
                await this.goToPage(this.pagination.currentPage + 1);
            }
        },

        async previousPage() {
            if (this.pagination.currentPage > 1) {
                await this.goToPage(this.pagination.currentPage - 1);
            }
        },

        async createUser(userData) {
            this.loading = true;
            this.error = null;

            try {
                const newUser = await userService.createUser(userData);
                // Recarrega a página atual para manter consistência
                await this.fetchUsers(this.pagination.currentPage);
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
                // Atualiza o usuário na lista atual
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
                // Recarrega a página atual
                await this.fetchUsers(this.pagination.currentPage);
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
