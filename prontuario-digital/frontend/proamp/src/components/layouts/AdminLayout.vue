<template>
    <BaseLayout user-type="admin" :layout-config="adminConfig">
        <router-view />
    </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { getLayoutConfig } from '@/config/layoutConfigs.js';

const adminConfig = getLayoutConfig('admin');
</script>
