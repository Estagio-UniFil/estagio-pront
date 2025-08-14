<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <!-- Main Container -->
        <div class="relative w-full max-w-md">
            <!-- Logo/Header Section -->
            <div class="text-center mb-8">
                <h1 class="text-3xl font-lato-black text-gray-800 mb-2">ProAMP</h1>
                <p class="text-gray-600 font-lato-regular">Prontuário Digital Anna Maria Pietta</p>
            </div>

            <!-- Content Slot -->
            <div class="relative">
                <slot />
            </div>

            <!-- Footer -->
            <div class="text-center mt-8 text-sm text-gray-500">
                <p class="font-lato-regular">© {{ currentYear }} Sistema de Prontuário Digital</p>
                <p class="font-lato-light mt-1">Desenvolvido por Luis Mineo</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const currentYear = computed(() => {
    return new Date().getFullYear();
});
</script>

<style scoped>
@keyframes float {
    0%,
    100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-10px);
    }
}

.animate-float {
    animation: float 3s ease-in-out infinite;
}

.bg-gradient-to-br {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 50%, #c7d2fe 100%);
}

.card {
    backdrop-filter: blur(10px);
    background-color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 480px) {
    .card {
        margin: 1rem;
        padding: 1.5rem;
    }
}
</style>
