import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/api/authService';

export const useAuthStore = defineStore('auth', () => {
    // Estados
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
    const isLoading = ref(false);
    const error = ref(null);

    // Getters
    const isAuthenticated = computed(() => {
        return !!user.value;
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
    const login = async (email, password, rememberMe = false) => {
        try {
            isLoading.value = true;
            error.value = null;

            const response = await authService.login(email, password, rememberMe);

            // Salva dados do usuário
            user.value = {
                id: response.data.user_id,
                email: response.data.email,
                role: response.data.role,
                first_name: response.data.first_name || '',
                last_name: response.data.last_name || '',
                session_expiry: response.data.session_expiry,
            };

            // Se for profissional de saúde, adiciona dados do perfil
            if (response.data.health_profile) {
                user.value.health_profile = response.data.health_profile;
            }

            // Persiste no localStorage
            localStorage.setItem('user', JSON.stringify(user.value));

            return response.data;
        } catch (err) {
            // Trata mensagens de erro do backend
            if (err.response?.data?.error) {
                error.value = err.response.data.error;
            } else if (err.response?.status === 401) {
                error.value = 'Email ou senha incorretos';
            } else {
                error.value = 'Erro ao fazer login. Tente novamente.';
            }
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const logout = async () => {
        try {
            isLoading.value = true;

            // Chama o logout no backend
            await authService.logout();

            // Limpa o estado local
            user.value = null;
            error.value = null;
            localStorage.removeItem('user');
        } catch (err) {
            console.error('Erro no logout:', err);
            // Mesmo com erro, limpa dados locais
            user.value = null;
            localStorage.removeItem('user');
        } finally {
            isLoading.value = false;
        }
    };

    const checkAuthStatus = async () => {
        try {
            const response = await authService.checkAuth();

            if (response.data.is_authenticated && user.value.health_profile) {
                user.value = {
                    id: response.data.user_id,
                    email: response.data.email,
                    role: response.data.role,
                    first_name: response.data.first_name || '',
                    last_name: response.data.last_name || '',
                    health_profile: user.value.health_profile,
                };

                localStorage.setItem('user', JSON.stringify(user.value));
                return true;
            } else if (response.data.is_authenticated) {
                // Atualiza dados do usuário
                user.value = {
                    id: response.data.user_id,
                    email: response.data.email,
                    role: response.data.role,
                    first_name: response.data.first_name || '',
                    last_name: response.data.last_name || '',
                };

                localStorage.setItem('user', JSON.stringify(user.value));
                return true;
            } else {
                // Não autenticado
                user.value = null;
                localStorage.removeItem('user');
                return false;
            }
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            user.value = null;
            localStorage.removeItem('user');
            return false;
        }
    };

    const setUser = (newUserData) => {
        user.value = { ...user.value, ...newUserData };
        localStorage.setItem('user', JSON.stringify(user.value));
    };

    const initializeAuth = async () => {
        const savedUser = localStorage.getItem('user');

        if (savedUser) {
            checkAuthStatus().then((isValid) => {
                if (!isValid) {
                    user.value = null;
                    localStorage.removeItem('user');
                }
            });
        }
    };

    const clearError = () => {
        error.value = null;
    };

    const clearAuth = () => {
        user.value = null;
        error.value = null;
        localStorage.removeItem('user');
    };

    const fetchMe = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const me = await authService.getUserLogged();
            user.value = { ...(user.value || {}), ...me };
            return user.value;
        } catch (e) {
            error.value = e.data || e.message || 'Falha ao carregar perfil';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const updateMe = async (payload) => {
        isLoading.value = true;
        error.value = null;
        try {
            const updated = await authService.patchUserLogged(payload);
            user.value = { ...(user.value || {}), ...updated };
            return user.value;
        } catch (e) {
            error.value = e.data || e.message || 'Falha ao atualizar perfil';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // Estados
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
        checkAuthStatus,
        initializeAuth,
        clearError,
        clearAuth,
        setUser,
        updateMe,
        fetchMe,
    };
});
