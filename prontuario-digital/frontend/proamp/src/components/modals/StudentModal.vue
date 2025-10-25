<template>
    <BaseModal :show="show" :title="modalTitle" @close="handleClose">
        <StudentForm :student="studentData" :is-editing="isEditing" :is-submitting="isSubmitting" :validation-errors="props.validationErrors" @submit="handleSubmit" @cancel="handleClose" />
    </BaseModal>
</template>

<script setup>
import { computed } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import StudentForm from '@/components/forms/student/StudentForm.vue';

const props = defineProps({
    show: {
        type: Boolean,
        default: false,
    },
    student: {
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
    validationErrors: {
        type: Object,
        default: () => ({}),
    },
});

const emit = defineEmits(['close', 'submit']);

const modalTitle = computed(() => {
    if (!props.student) {
        return 'Novo Estudante';
    }
    return props.isEditing ? `Editar:  ${props.student.name}` : `Detalhes:  ${props.student.name}`;
});

const studentData = computed(() => props.student || {});

const handleSubmit = (payload) => {
    emit('submit', payload);
};

const handleClose = () => {
    emit('close');
};
</script>
