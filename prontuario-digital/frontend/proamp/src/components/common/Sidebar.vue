<template>
    <aside class="sidebar" :class="{ open: sidebarOpen }">
        <!-- Logo/Header -->
        <div class="sidebar-header flex items-center gap-2">
            <div>
                <a href="/">
                    <LogoProamp class="w-15 h-auto fill-current text-secondary dark:text-slate-100 transition-colors duration-300" />
                </a>
            </div>
            <div>
                <h1 class="sidebar-title">{{ config.title }}</h1>
                <p class="text-xs text-muted font-lato-medium mt-1">{{ config.subtitle }}</p>
            </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="flex-1 py-4">
            <router-link v-for="item in config.navigation" :key="item.route" :to="{ name: item.route }" class="nav-link" :class="{ active: $route.name === item.route }">
                <i :class="item.icon" class="w-5 mr-3"></i>
                {{ item.name }}
            </router-link>
        </nav>

        <!-- User Info / Logout -->
        <div class="p-4 border-t border-primary">
            <router-link :to="{ name: `${userType}-profile` }" :class="{ active: $route.name === `${userType}-profile` }">
                <div class="flex items-center mb-3">
                    <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-lato-bold">
                        {{ userInitials }}
                    </div>
                    <div class="ml-3 flex-1">
                        <p class="text-sm font-lato-bold text-primary">{{ userName }}</p>
                        <p class="text-xs text-muted">{{ config.userRole }}</p>
                    </div>
                </div>
            </router-link>
            <button @click="handleLogout" class="btn-logout w-full text-left px-3 py-2 text-sm hover:bg-red-50 rounded-lg transition-colors font-lato-regular" :disabled="authStore.isLoading">
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
import LogoProamp from '../logo/LogoProamp.vue';

const router = useRouter();
const authStore = useAuthStore();

// Props
const props = defineProps({
    sidebarOpen: {
        type: Boolean,
        default: false,
    },
    config: {
        type: Object,
        required: true,
    },
    userType: {
        type: String,
        required: true,
    },
});

// Computed
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

/* Font Awesome fallback */
.fas::before {
    font-family: 'Font Awesome 6 Free';
    font-weight: 900;
}
</style>
