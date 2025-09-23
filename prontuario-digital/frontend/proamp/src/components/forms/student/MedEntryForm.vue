<template>
    <div class="form-container">
        <div class="form-group">
            <label for="student-name" class="input-label">Aluno</label>
            <input id="student-name" type="text" :value="studentName" class="input-field bg-tertiary" disabled />
        </div>
        <div class="form-group">
            <label for="healthpro-name" class="input-label">Profissional de Saúde</label>
            <input id="healthpro-name" type="text" :value="healthproName" class="input-field bg-tertiary" disabled />
        </div>
        <div class="form-group">
            <label for="entry-date" class="input-label">Data da Entrada</label>
            <input id="entry-date" type="text" :value="formattedEntryDate" class="input-field bg-tertiary" disabled />
        </div>
        <div class="form-group">
            <label for="description" class="input-label">Descrição</label>
            <textarea id="description" v-model="editableData.description" class="input-field bg-tertiary" :readonly="readonly" rows="4" placeholder="Descrição detalhada do atendimento..."></textarea>
        </div>
        <div class="form-group">
            <label for="notes" class="input-label">Observações Adicionais</label>
            <textarea id="notes" v-model="editableData.notes" class="input-field bg-tertiary" :readonly="readonly" rows="3" placeholder="Notas ou observações adicionais..."></textarea>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
    modelValue: {
        type: Object,
        required: true,
    },
    readonly: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['update:modelValue']);

const editableData = ref({ ...props.modelValue });

watch(
    () => props.modelValue,
    (newValue) => {
        editableData.value = { ...newValue };
    },
    { deep: true },
);

watch(
    editableData,
    (newValue) => {
        emit('update:modelValue', newValue);
    },
    { deep: true },
);

// Formatting
const studentName = computed(() => {
    return props.modelValue.student?.name || 'Não informado';
});

const getHealthProName = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
};

const healthproName = computed(() => {
    return getHealthProName(props.modelValue.healthpro) || 'Não informado';
});

const formattedEntryDate = computed(() => {
    if (!props.modelValue.entry_date) return 'N/A';
    return new Date(props.modelValue.entry_date).toLocaleString('pt-BR');
});
</script>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.form-group {
    display: flex;
    flex-direction: column;
}
.form-group label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}
.input-field bg-tertiary[readonly],
.input-field bg-tertiary[disabled] {
    background-color: #f0f0f0;
    cursor: not-allowed;
}
</style>
