<template>
    <BaseModal :show="show" @close="handleClose" :title="modalTitle">
        <MedEntryForm v-if="mode === 'view' || mode === 'create'" v-model="formData" :readonly="isViewMode" :mode="mode" :students="studentList" @student-selected="handleStudentSelected" />

        <div v-if="mode === 'delete'">
            <p class="mb-6">Você tem certeza que deseja excluir esta entrada de prontuário? Esta ação não pode ser desfeita.</p>
            <div class="form-group">
                <label for="delete-reason" class="input-label">Motivo da Exclusão</label>
                <input type="text" class="input-field" id="delete-reason" v-model="deleteReason" placeholder="É obrigatório informar o motivo da exclusão." /><input />
            </div>
        </div>

        <template #footer>
            <button @click="handleClose" class="btn btn-secondary">
                {{ isViewMode ? 'Fechar' : 'Cancelar' }}
            </button>

            <button v-if="mode === 'create'" @click="submitCreate" class="btn btn-primary" :disabled="isLoading || !selectedStudentId || !formData.description">
                {{ isLoading ? 'Salvando...' : 'Salvar' }}
            </button>

            <button v-if="mode === 'delete'" @click="submitDelete" class="btn btn-danger" :disabled="isLoading || !deleteReason.trim()">
                {{ isLoading ? 'Excluindo...' : 'Confirmar Exclusão' }}
            </button>
        </template>
    </BaseModal>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import MedEntryForm from '@/components/forms/student/MedEntryForm.vue';
import { useAlertStore } from '@/stores/alertStore';
import { useStudentStore } from '@/stores/studentStore';
import { useMedEntryStore } from '@/stores/medEntryStore';
import { useAuth } from '@/composables/useAuth';

const props = defineProps({
    show: {
        type: Boolean,
        required: true,
    },
    mode: {
        type: String,
        required: true,
        validator: (value) => ['view', 'create', 'delete'].includes(value),
    },
    entryData: {
        type: Object,
        default: () => ({}),
    },
});

const emit = defineEmits(['close', 'success']);

const alertStore = useAlertStore();
const studentStore = useStudentStore();
const medEntryStore = useMedEntryStore();
const { user } = useAuth();

const isLoading = ref(false);
const formData = ref({});
const deleteReason = ref('');
const selectedStudentId = ref(null);
const studentList = ref([]);

// Carregar lista de estudantes quando o modal abrir no modo create
watch(
    () => props.show,
    async (newValue) => {
        if (newValue && props.mode === 'create') {
            await loadStudents();
            initializeCreateMode();
        } else if (newValue && (props.mode === 'view' || props.mode === 'delete')) {
            formData.value = { ...props.entryData };
        }
    },
    { immediate: true },
);

const loadStudents = async () => {
    try {
        if (studentStore.students.length === 0) {
            await studentStore.fetchStudents(true); // true = ativos
        }
        studentList.value = studentStore.students;
    } catch (error) {
        console.error('Erro ao carregar estudantes:', error);
        alertStore.triggerAlert({ message: 'Erro ao carregar lista de estudantes.', type: 'error' });
    }
};

const initializeCreateMode = () => {
    selectedStudentId.value = null;
    formData.value = {
        description: '',
        notes: '',
        student: null,
        healthpro: user.value,
        entry_date: new Date().toISOString(),
    };
};

const handleStudentSelected = (student) => {
    selectedStudentId.value = student.id;
    formData.value.student = {
        id: student.id,
        name: student.name,
    };
};

const isViewMode = computed(() => props.mode === 'view');

const modalTitle = computed(() => {
    if (props.mode === 'view') return 'Detalhes da Entrada de Prontuário';
    if (props.mode === 'create') return 'Nova Entrada de Prontuário';
    if (props.mode === 'delete') return 'Excluir Entrada de Prontuário';
    return '';
});

const handleClose = () => {
    if (!isLoading.value) {
        deleteReason.value = '';
        selectedStudentId.value = null;
        formData.value = {};
        emit('close');
    }
};

const submitCreate = async () => {
    if (!selectedStudentId.value) {
        alertStore.triggerAlert('Selecione um estudante.', 'warning');
        return;
    }

    if (!formData.value.description || !formData.value.description.trim()) {
        alertStore.triggerAlert('A descrição é obrigatória.', 'warning');
        return;
    }

    isLoading.value = true;
    try {
        const payload = {
            student_id: selectedStudentId.value,
            description: formData.value.description,
            notes: formData.value.notes || '',
        };

        await medEntryStore.createEntry(payload);
        alertStore.triggerAlert('Entrada criada com sucesso!', 'success');
        emit('success');
        handleClose();
    } catch (error) {
        alertStore.triggerAlert('Erro ao criar entrada.', 'error');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};

const submitDelete = async () => {
    if (!deleteReason.value.trim()) {
        alertStore.triggerAlert('O motivo da exclusão é obrigatório.', 'warning');
        return;
    }

    isLoading.value = true;
    try {
        await medEntryStore.deleteEntry(props.entryData.id, deleteReason.value);
        deleteReason.value = '';
        alertStore.triggerAlert('Entrada excluída com sucesso!', 'success');
        emit('success');
        handleClose();
    } catch (error) {
        alertStore.triggerAlert('Erro ao excluir entrada.', 'error');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};
</script>
