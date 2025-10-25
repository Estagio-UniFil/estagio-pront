import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/services/api/authService';

export const useAuthStore = defineStore('auth', () => {
    // States
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

    const mustChangePassword = computed(() => user.value?.must_change_password || false);

    // Actions
    const login = async (email, password, rememberMe = false) => {
        try {
            isLoading.value = true;
            error.value = null;

            const response = await authService.login(email, password, rememberMe);

            user.value = {
                id: response.data.user_id,
                email: response.data.email,
                role: response.data.role,
                first_name: response.data.first_name || '',
                last_name: response.data.last_name || '',
                session_expiry: response.data.session_expiry,
                must_change_password: response.data.must_change_password,
            };

            // For Health Pro
            if (response.data.health_profile) {
                user.value.health_profile = response.data.health_profile;
            }

            localStorage.setItem('user', JSON.stringify(user.value));

            return response.data;
        } catch (err) {
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

            await authService.logout();

            // Clear local data
            user.value = null;
            error.value = null;
            localStorage.removeItem('user');
        } catch (err) {
            console.error('Erro no logout:', err);
            user.value = null;
            localStorage.removeItem('user');
        } finally {
            isLoading.value = false;
        }
    };

    const checkAuthStatus = async () => {
        try {
            const response = await authService.checkAuth();

            // if (response.data.is_authenticated && user.value.health_profile) {
            //     user.value = {
            //         ...(user.value || {}),
            //         id: response.data.user_id,
            //         email: response.data.email,
            //         role: response.data.role,
            //         first_name: response.data.first_name || '',
            //         last_name: response.data.last_name || '',
            //     };

            //     localStorage.setItem('user', JSON.stringify(user.value));
            //     return true;
            // }
            if (response.data.is_authenticated) {
                user.value = {
                    ...(user.value || {}),
                    id: response.data.user_id,
                    email: response.data.email,
                    role: response.data.role,
                    first_name: response.data.first_name || '',
                    last_name: response.data.last_name || '',
                    must_change_password: response.data.must_change_password,
                };

                localStorage.setItem('user', JSON.stringify(user.value));
                return true;
            } else {
                // Not authenticated
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
            user.value = JSON.parse(savedUser);
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

    const setPassword = async (passwordData) => {
        try {
            isLoading.value = true;
            error.value = null;
            await authService.setPassword(passwordData);
            // If success, update local data
            if (user.value) {
                user.value.must_change_password = false;
                localStorage.setItem('user', JSON.stringify(user.value));
            }
        } catch (err) {
            const errorMessage = err.response?.data?.error || err.response?.data?.confirm_password?.[0] || 'Erro ao alterar a senha.';
            error.value = errorMessage;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const fetchMe = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const meData = await authService.getUserLogged();
            user.value = { ...(user.value || {}), ...meData };
            localStorage.setItem('user', JSON.stringify(user.value));
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
            const updatedData = await authService.patchUserLogged(payload);
            user.value = { ...(user.value || {}), ...updatedData };
            localStorage.setItem('user', JSON.stringify(user.value));
            return user.value;
        } catch (e) {
            error.value = e.data || e.message || 'Falha ao atualizar perfil';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // States
        user: computed(() => user.value),
        isLoading: computed(() => isLoading.value),
        error: computed(() => error.value),

        // Getters
        isAuthenticated,
        userRole,
        isAdmin,
        isProfessional,
        isManager,
        mustChangePassword,

        // Actions
        login,
        logout,
        checkAuthStatus,
        setPassword,
        initializeAuth,
        clearError,
        clearAuth,
        setUser,
        updateMe,
        fetchMe,
    };
});
