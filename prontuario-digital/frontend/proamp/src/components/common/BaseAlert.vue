<template>
    <Transition name="fade">
        <div v-if="isVisible" :class="alertClasses" role="alert">
            <div class="flex items-start">
                <div class="mr-4 mt-1" :class="iconColor">
                    <i :class="alertIcon"></i>
                </div>

                <div class="flex-1">
                    <p v-if="title" class="font-lato-bold text-sm mb-1">{{ title }}</p>
                    <p class="font-lato-regular text-sm">
                        <slot>{{ message }}</slot>
                    </p>
                </div>

                <button v-if="closable" @click="close" class="ml-auto p-1 rounded-full hover:bg-opacity-20 transition-colors" :class="hoverBgColor">
                    <i class="fas fa-times" :class="iconColor"></i>
                </button>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    type: {
        type: String,
        default: 'info', // 'success', 'error', 'warning', 'info'
    },
    title: {
        type: String,
        default: '',
    },
    message: {
        type: String,
        default: '',
    },
    closable: {
        type: Boolean,
        default: true,
    },
});

const isVisible = ref(true);

const alertClasses = computed(() => {
    return ['alert', `alert-${props.type}`];
});

const alertIcon = computed(() => {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle',
    };
    return icons[props.type] || icons.info;
});

const iconColor = computed(() => {
    const colors = {
        success: 'success-text',
        error: 'error-text',
        warning: 'text-warning-text',
        info: 'text-blue-800',
    };
    return colors[props.type] || colors.info;
});

const hoverBgColor = computed(() => {
    const colors = {
        success: 'hover:bg-success-bg',
        error: 'hover:bg-error-bg',
        warning: 'hover:bg-warnig-bg',
        info: 'hover:bg-blue-200',
    };
    return colors[props.type] || colors.info;
});

const close = () => {
    isVisible.value = false;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.3s ease,
        transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
