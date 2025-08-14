import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/api/authService';

export const useAuthStore = defineStore('auth', () => {
    // Estados
    const token = ref(localStorage.getItem('authToken'));
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
    const isLoading = ref(false);
    const error = ref(null);

    // Getters
    const isAuthenticated = computed(() => {
        return !!token.value;
    });

    const userRole = computed(() => {
        return user.value?.role || null;
    });

    const isAdmin = computed(() => {
        return userRole.value === 'admin';
    });

    const isProfessional = computed(() => {
        return userRole.value === 'health_prof';
    });

    const isManager = computed(() => {
        return userRole.value === 'manager';
    });

    // Actions
    const login = async (email, password) => {
        try {
            isLoading.value = true;
            error.value = null;

            const response = await authService.login(email, password);

            // Salvar token e dados do usuário
            token.value = response.data.token;
            user.value = {
                id: response.data.user_id,
                email: response.data.email,
                role: response.data.role,
                first_name: response.data.first_name || '',
                last_name: response.data.last_name || '',
            };

            // Persistir no localStorage
            localStorage.setItem('token', token.value);
            localStorage.setItem('user', JSON.stringify(user.value));

            return response.data;
        } catch (err) {
            error.value = err.response?.data?.detail || 'Erro ao fazer login';
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const logout = async () => {
        try {
            isLoading.value = true;

            // Chama o service de logout (limpa localStorage)
            await authService.logout();

            // Limpa o estado do store
            token.value = null;
            user.value = null;
            error.value = null;
        } catch (err) {
            console.error('Erro no logout:', err);
        } finally {
            isLoading.value = false;
        }
    };

    const initializeAuth = () => {
        // Verifica se tem dados salvos no localStorage
        const savedToken = localStorage.getItem('token');
        const savedUser = localStorage.getItem('user');

        if (savedToken && savedUser) {
            token.value = savedToken;
            user.value = JSON.parse(savedUser);
        }
    };

    const clearError = () => {
        error.value = null;
    };

    const clearAuth = () => {
        // Limpa tudo (usado em caso de token inválido)
        token.value = null;
        user.value = null;
        error.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    };

    return {
        // Estados (readonly para evitar modificação direta)
        token: computed(() => token.value),
        user: computed(() => user.value),
        isLoading: computed(() => isLoading.value),
        error: computed(() => error.value),

        // Getters
        isAuthenticated,
        userRole,
        isAdmin,
        isProfessional,
        isManager,

        // Actions
        login,
        logout,
        initializeAuth,
        clearError,
        clearAuth,
    };
});
