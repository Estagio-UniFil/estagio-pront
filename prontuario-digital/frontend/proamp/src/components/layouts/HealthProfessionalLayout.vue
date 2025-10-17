<template>
    <BaseLayout user-type="health-professional" :layout-config="healthProfessionalConfig">
        <router-view />
    </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { getLayoutConfig } from '@/config/layoutConfigs.js';

// Configuração específica do profissional de saúde
const healthProfessionalConfig = getLayoutConfig('health-professional');
</script>
