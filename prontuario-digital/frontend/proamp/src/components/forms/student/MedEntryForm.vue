<template>
    <div class="form-container">
        <!-- Student Dropdown -->
        <div v-if="mode === 'create'" class="form-group">
            <label for="student-select" class="input-label">Selecionar Estudante*</label>
            <select id="student-select" v-model="selectedStudentId" class="input-field" @change="handleStudentChange" required>
                <option value="" disabled>Selecione um estudante</option>
                <option v-for="student in students" :key="student.id" :value="student.id">{{ student.name }} - CGM: {{ student.cgm }}</option>
            </select>
        </div>

        <!-- View mode -->
        <div v-if="mode !== 'create'" class="form-group">
            <label for="student-name" class="input-label">Aluno</label>
            <input id="student-name" type="text" :value="studentName" class="input-field" disabled />
        </div>

        <div v-if="mode !== 'create'" class="form-group">
            <label for="healthpro-name" class="input-label">Profissional de Saúde</label>
            <input id="healthpro-name" type="text" :value="healthproName" class="input-field" disabled />
        </div>

        <div v-if="mode !== 'create'" class="form-group">
            <label for="entry-date" class="input-label">Data da Entrada</label>
            <input id="entry-date" type="text" :value="formattedEntryDate" class="input-field" disabled />
        </div>

        <!-- Edit fields -->
        <div class="form-group">
            <label for="description" class="input-label">Descrição{{ mode === 'create' ? '*' : '' }}</label>
            <textarea id="description" v-model="localDescription" class="input-field" :readonly="readonly" rows="4" placeholder="Descrição detalhada do atendimento..." :required="mode === 'create'"></textarea>
        </div>

        <div class="form-group">
            <label for="notes" class="input-label">Observações Adicionais</label>
            <textarea id="notes" v-model="localNotes" class="input-field" :readonly="readonly" rows="3" placeholder="Notas ou observações adicionais..."></textarea>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
    modelValue: {
        type: Object,
        required: true,
    },
    readonly: {
        type: Boolean,
        default: false,
    },
    mode: {
        type: String,
        default: 'view',
        validator: (value) => ['view', 'create', 'delete'].includes(value),
    },
    students: {
        type: Array,
        default: () => [],
    },
});

const emit = defineEmits(['update:modelValue', 'student-selected']);

// Local refs
const selectedStudentId = ref(props.modelValue.student?.id || '');
const localDescription = ref(props.modelValue.description || '');
const localNotes = ref(props.modelValue.notes || '');

// Update values
watch(
    () => props.modelValue,
    (newValue) => {
        selectedStudentId.value = newValue.student?.id || '';
        localDescription.value = newValue.description || '';
        localNotes.value = newValue.notes || '';
    },
    { deep: true },
);

// Emit changes
watch([localDescription, localNotes], () => {
    emit('update:modelValue', {
        ...props.modelValue,
        description: localDescription.value,
        notes: localNotes.value,
    });
});

const handleStudentChange = () => {
    const student = props.students.find((s) => s.id === selectedStudentId.value);
    if (student) {
        emit('student-selected', student);
    }
};

// Formatting
const studentName = computed(() => {
    return props.modelValue.student?.name || 'Não informado';
});

const getHealthProName = (user) => {
    if (user?.first_name && user?.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return null;
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
.input-field[readonly],
.input-field[disabled] {
    background-color: var(--bg-tertiary);
    color: var(--text-muted);
    cursor: not-allowed;
}

select.input-field {
    cursor: pointer;
}

select.input-field:disabled {
    cursor: not-allowed;
}
</style>
