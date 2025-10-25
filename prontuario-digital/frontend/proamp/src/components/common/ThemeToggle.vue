<template>
    <button @click="toggleTheme" class="theme-toggle" :class="{ [`theme-toggle-${size}`]: size !== 'default' }" :title="isDark ? 'Alternar para tema claro' : 'Alternar para tema escuro'" type="button">
        <div class="theme-toggle-slider">
            <i :class="isDark ? 'fas fa-moon' : 'fas fa-sun'"></i>
        </div>
    </button>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme';

// Props
defineProps({
    size: {
        type: String,
        default: 'default',
        validator: (value) => ['small', 'default', 'large'].includes(value),
    },
});

// Theme composable
const { isDark, toggleTheme } = useTheme();
</script>

<script>
export default {
    name: 'ThemeToggle',
};
</script>

<style scoped>
.theme-toggle-small {
    width: 48px;
    height: 24px;
}

.theme-toggle-small .theme-toggle-slider {
    width: 18px;
    height: 18px;
}

.theme-toggle-small .theme-toggle-slider i {
    font-size: 10px;
}

.theme-toggle-large {
    width: 72px;
    height: 36px;
}

.theme-toggle-large .theme-toggle-slider {
    width: 28px;
    height: 28px;
}

.theme-toggle-large .theme-toggle-slider i {
    font-size: 14px;
}

[data-theme='dark'] .theme-toggle-large .theme-toggle-slider {
    transform: translateX(34px);
}

[data-theme='dark'] .theme-toggle-small .theme-toggle-slider {
    transform: translateX(22px);
}

/* Default Style */
.theme-toggle-slider i {
    font-size: 12px;
    color: white;
    transition: all 0.3s ease;
}
</style>
