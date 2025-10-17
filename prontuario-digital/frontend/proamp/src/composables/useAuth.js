// src/composables/useAuth.js
import { computed } from 'vue';
import { useRouter } from 'vue-router';

export function useAuth() {
    const router = useRouter();

    const user = computed(() => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    });

    const isAuthenticated = computed(() => !!user.value);

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        router.push('/login');
    };

    return {
        user,
        isAuthenticated,
        logout,
    };
}
