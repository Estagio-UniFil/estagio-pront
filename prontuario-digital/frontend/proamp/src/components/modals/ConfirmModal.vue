<template>
    <BaseModal :show="show" title="Confirmar Desativação" :closable="false" maxWidth="32rem">
        <p class="text-primary">Tem certeza que deseja {{ actionType }} o registro de {{ entryName }}?</p>

        <template #footer>
            <div class="flex justify-end w-full space-x-4">
                <button @click="$emit('cancel')" class="btn-secondary">Cancelar</button>
                <button @click="$emit('confirm')" class="btn-danger">Sim, {{ actionType }}</button>
            </div>
        </template>
    </BaseModal>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';

defineProps({
    show: {
        type: Boolean,
        required: true,
    },
    entryName: {
        type: String,
        default: 'object-name-info',
    },
    actionType: {
        type: String,
        default: 'action-type-info',
    },
});

defineEmits(['confirm', 'cancel']);
</script>
