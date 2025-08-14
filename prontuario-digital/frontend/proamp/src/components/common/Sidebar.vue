<template>
    <aside class="sidebar" :class="{ open: sidebarOpen }">
        <!-- Logo/Header -->
        <div class="sidebar-header">
            <h1 class="sidebar-title">ProAMP</h1>
            <p class="text-xs text-gray-500 font-lato-light mt-1">Administração</p>
        </div>

        <!-- Navigation Menu -->
        <nav class="flex-1 py-4">
            <!-- Dashboard -->
            <router-link :to="{ name: 'admin-dashboard' }" class="nav-link" :class="{ active: $route.name === 'admin-dashboard' }">
                <i class="fas fa-tachometer-alt w-5 mr-3"></i>
                Dashboard
            </router-link>

            <!-- Funcionários -->
            <router-link :to="{ name: 'admin-users' }" class="nav-link" :class="{ active: $route.name === 'admin-users' }">
                <i class="fas fa-user-md w-5 mr-3"></i>
                Funcionários
            </router-link>

            <!-- Alunos -->
            <router-link :to="{ name: 'admin-students' }" class="nav-link" :class="{ active: $route.name === 'admin-students' }">
                <i class="fas fa-users w-5 mr-3"></i>
                Alunos
            </router-link>

            <!-- Relatórios -->
            <router-link :to="{ name: 'admin-reports' }" class="nav-link" :class="{ active: $route.name === 'admin-reports' }">
                <i class="fas fa-chart-bar w-5 mr-3"></i>
                Relatórios
            </router-link>

            <!-- Separador -->
            <div class="border-t border-gray-200 mx-4 my-4"></div>

            <!-- Configurações -->
            <router-link :to="{ name: 'admin-settings' }" class="nav-link" :class="{ active: $route.name === 'admin-settings' }">
                <i class="fas fa-cog w-5 mr-3"></i>
                Configurações
            </router-link>
        </nav>

        <!-- User Info / Logout -->
        <div class="p-4 border-t border-gray-200">
            <div class="flex items-center mb-3">
                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-lato-bold">
                    {{ userInitials }}
                </div>
                <div class="ml-3 flex-1">
                    <p class="text-sm font-lato-bold text-gray-900">{{ userName }}</p>
                    <p class="text-xs text-gray-500">Administrador</p>
                </div>
            </div>

            <button @click="handleLogout" class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors font-lato-regular" :disabled="authStore.isLoading">
                <i class="fas fa-sign-out-alt w-4 mr-2"></i>
                {{ authStore.isLoading ? 'Saindo...' : 'Sair' }}
            </button>
        </div>
    </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

// Props (se necessário para controle do mobile)
const props = defineProps({
    sidebarOpen: {
        type: Boolean,
        default: false,
    },
});

// Computeds
const userName = computed(() => {
    const user = authStore.user;
    if (user?.first_name && user?.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return user?.email || 'Usuário';
});

const userInitials = computed(() => {
    const user = authStore.user;
    if (user?.first_name && user?.last_name) {
        return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
    }
    if (user?.email) {
        return user.email[0].toUpperCase();
    }
    return 'U';
});

// Methods
const handleLogout = async () => {
    try {
        await authStore.logout();
        router.push({ name: 'login' });
    } catch (error) {
        console.error('Erro no logout:', error);
    }
};
</script>

<style scoped>
/* Mobile responsive */
@media (max-width: 1024px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s ease-in-out;
        z-index: 50;
    }

    .sidebar.open {
        transform: translateX(0);
    }
}

/* Font Awesome fallback se não carregou */
.fas::before {
    font-family: 'Font Awesome 6 Free';
    font-weight: 900;
}
</style>
