<template>
    <BaseModal :show="show" :title="modalTitle" @close="handleClose">
        <UserForm :user="userData" :is-editing="isEditing" :is-submitting="isSubmitting" @submit="handleSubmit" @cancel="handleClose" />
    </BaseModal>
</template>

<script setup>
import { computed } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import UserForm from '@/components/forms/user/UserForm.vue';

const props = defineProps({
    show: {
        type: Boolean,
        default: false,
    },
    user: {
        type: Object,
        default: null,
    },
    isEditing: {
        type: Boolean,
        default: false,
    },
    isSubmitting: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['close', 'submit']);

const modalTitle = computed(() => {
    if (!props.user) {
        return 'Novo usuário';
    }
    return props.isEditing ? `Editar:  ${props.user.first_name}` : `Detalhes:  ${props.user.first_name}`;
});

const userData = computed(() => props.user || {});

const handleSubmit = (payload) => {
    emit('submit', payload);
};

const handleClose = () => {
    emit('close');
};
</script>
