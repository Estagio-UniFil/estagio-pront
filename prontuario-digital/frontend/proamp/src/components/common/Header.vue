<template>
    <header class="bg-secondary border-b rounded-md border-primary px-6 py-4">
        <div class="flex items-center justify-between">
            <!-- Mobile Menu Button + Title -->
            <div class="flex items-center">
                <!-- Mobile menu button -->
                <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 mr-4">
                    <i class="fas fa-bars text-lg"></i>
                </button>

                <!-- Page Title -->
                <div>
                    <h1 class="text-xl font-lato-bold text-primary">{{ headerTitle }}</h1>
                    <p v-if="pageSubtitle" class="text-sm text-muted font-lato-regular">{{ pageSubtitle }}</p>
                </div>
            </div>

            <!-- Right Side -->
            <div class="flex items-center space-x-4">
                <ThemeToggle />
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
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import ThemeToggle from './ThemeToggle.vue';

const route = useRoute();
const authStore = useAuthStore();
const user = authStore.user;

// Props
const props = defineProps({
    showSearch: {
        type: Boolean,
        default: false,
    },
    config: {
        type: Object,
        default: () => ({}),
    },
    userType: {
        type: String,
        default: 'admin',
    },
});

// Emits
const emit = defineEmits(['toggle-sidebar']);

// State
const showNotifications = ref(false);
const showUserMenu = ref(false);

// Computed
const headerTitle = computed(() => {
    return props.config.title || 'Painel de administrador';
});

const pageSubtitle = computed(() => {
    const subtitleMap = props.config.subtitleMap || {};
    let subtitle = subtitleMap[route.name] || '';

    // Substituir placeholder {name} pelo nome do usuário
    if (subtitle.includes('{name}') && user?.first_name) {
        subtitle = subtitle.replace('{name}', user.first_name);
    }

    return subtitle;
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
