<template>
    <div class="admin-layout">
        <!-- Sidebar -->
        <Sidebar :sidebarOpen="sidebarOpen" />

        <!-- Main Content Area -->
        <div class="main-content lg:ml-64 lg:px-12">
            <!-- Header -->
            <Header @toggle-sidebar="toggleSidebar" @toggle-UserMenu="toggleUserMenu" />

            <!-- Page Content -->
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

const sidebarOpen = ref(false);
const showUserMenu = ref(false);

const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
};

const closeSidebar = () => {
    sidebarOpen.value = false;
};

const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value;
};

// Fechar sidebar ao redimensionar para desktop
const handleResize = () => {
    if (window.innerWidth >= 1024) {
        sidebarOpen.value = false;
    }
};

onMounted(() => {
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
});

// Expor métodos para componentes filhos
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
