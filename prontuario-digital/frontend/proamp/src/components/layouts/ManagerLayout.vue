<template>
    <BaseLayout user-type="manager" :layout-config="managerConfig">
        <slot />
    </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { getLayoutConfig } from '@/config/layoutConfigs.js';

// Configuração específica do gestor
const managerConfig = getLayoutConfig('manager');
</script>
