<template>
    <BaseLayout user-type="manager" :layout-config="managerConfig">
        <router-view />
    </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { getLayoutConfig } from '@/config/layoutConfigs.js';

const managerConfig = getLayoutConfig('manager');
</script>
