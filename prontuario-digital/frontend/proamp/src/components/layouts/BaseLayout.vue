<template>
    <div :class="layoutConfig.containerClass">
        <!-- Sidebar -->
        <Sidebar :sidebarOpen="sidebarOpen" :config="layoutConfig.sidebar" :userType="userType" />

        <!-- Custom alert message -->
        <div class="fixed top-24 left-1/2 -translate-x-1/2 z-100 w-full max-w-xl px-4">
            <Transition name="fade">
                <BaseAlert v-if="alertStore.show" :type="alertStore.type" :title="alertStore.title" :message="alertStore.message" @close="alertStore.hideAlert()" />
            </Transition>
        </div>

        <!-- Main Content Area -->
        <div :class="layoutConfig.mainContentClass">
            <Header @toggle-sidebar="toggleSidebar" @toggle-UserMenu="toggleUserMenu" :config="layoutConfig.header" :userType="userType" :showSearch="layoutConfig.header.showSearch" />

            <!-- Page content -->
            <main class="mt-6">
                <slot />
            </main>
        </div>

        <!-- Mobile Menu Overlay -->
        <div v-if="sidebarOpen" class="mobile-overlay" @click="closeSidebar"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Sidebar from '../common/Sidebar.vue';
import Header from '../common/Header.vue';
import BaseAlert from '@/components/common/BaseAlert.vue';
import { useAlertStore } from '../../stores/alertStore';

// Props
const props = defineProps({
    userType: {
        type: String,
        required: true,
        validator: (value) => ['admin', 'manager', 'health-professional'].includes(value),
    },
    layoutConfig: {
        type: Object,
        required: true,
    },
});

// State
const sidebarOpen = ref(false);
const showUserMenu = ref(false);
const alertStore = useAlertStore();

// Methods
const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
};

const closeSidebar = () => {
    sidebarOpen.value = false;
};

const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value;
};

const handleResize = () => {
    if (window.innerWidth >= 1024) {
        sidebarOpen.value = false;
    }
};

// Lifecycle
onMounted(() => {
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
});

// Expose methods for child components
defineExpose({
    toggleSidebar,
    closeSidebar,
    sidebarOpen,
});
</script>

<style scoped>
.mobile-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 40;
    display: none;
}

@media (max-width: 1024px) {
    .main-content {
        margin-left: 0;
    }

    .mobile-overlay {
        display: block;
    }
}
</style>
