<template>
    <BaseLayout user-type="health-professional" :layout-config="healthProfessionalConfig">
        <router-view />
    </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { getLayoutConfig } from '@/config/layoutConfigs.js';

const healthProfessionalConfig = getLayoutConfig('health-professional');
</script>
