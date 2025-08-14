<template>
    <header class="bg-white border-b border-gray-200 px-6 py-4">
        <div class="flex items-center justify-between">
            <!-- Mobile Menu Button + Title -->
            <div class="flex items-center">
                <!-- Mobile menu button -->
                <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 mr-4">
                    <i class="fas fa-bars text-lg"></i>
                </button>

                <!-- Page Title -->
                <div>
                    <h1 class="text-xl font-lato-bold text-gray-900">Painel de administrador</h1>
                    <p v-if="pageSubtitle" class="text-sm text-gray-600 font-lato-regular">{{ pageSubtitle }}</p>
                </div>
            </div>

            <!-- Right Side - Actions -->
            <div class="flex items-center space-x-4">
                <!-- User Menu -->
                <div class="relative">
                    <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-lato-bold">
                        {{ userInitials }}
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const user = authStore.user;

// Props
const props = defineProps({
    showSearch: {
        type: Boolean,
        default: false,
    },
});

// Emits
const emit = defineEmits(['toggle-sidebar']);

// State
const searchQuery = ref('');
const showNotifications = ref(false);
const showUserMenu = ref(false);
const notificationCount = ref(3); // Mock data
const notifications = ref([
    { id: 1, message: 'Novo funcionário cadastrado', time: '5 min atrás' },
    { id: 2, message: 'Relatório mensal disponível', time: '1 hora atrás' },
    { id: 3, message: 'Sistema atualizado', time: '2 horas atrás' },
]);

// Computed
const pageTitle = computed(() => {
    if (user?.role == 'admin') {
        const routeMap = {
            'admin-dashboard': 'Dashboard',
            'admin-users': 'Funcionários',
            'admin-students': 'Alunos',
            'admin-reports': 'Relatórios',
            'admin-settings': 'Configurações',
        };
        return routeMap[route.name];
    }
});

const pageSubtitle = computed(() => {
    const name = user?.first_name;

    if (user?.role == 'admin') {
        const subtitleMap = {
            'admin-dashboard': `Bem vindo, ${name}!`,
            'admin-users': 'Admin > Funcionários',
            'admin-students': 'Admin > Alunos',
            'admin-reports': 'Admin > Relatórios',
            'admin-settings': 'Admin > Configurações',
        };
        return subtitleMap[route.name] || null;
    }
});

const userName = computed(() => {
    const user = authStore.user;
    if (user?.first_name) {
        return `${user.first_name}`;
    }
    return user?.email || 'Usuário';
});

const userEmail = computed(() => {
    return authStore.user?.email || '';
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
const toggleNotifications = () => {
    showNotifications.value = !showNotifications.value;
    showUserMenu.value = false;
};

const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value;
    showNotifications.value = false;
};

const handleLogout = async () => {
    try {
        await authStore.logout();
        router.push({ name: 'login' });
    } catch (error) {
        console.error('Erro no logout:', error);
    }
};

const closeDropdowns = () => {
    showNotifications.value = false;
    showUserMenu.value = false;
};

// Lifecycle
onMounted(() => {
    document.addEventListener('click', closeDropdowns);
});

onUnmounted(() => {
    document.removeEventListener('click', closeDropdowns);
});
</script>
