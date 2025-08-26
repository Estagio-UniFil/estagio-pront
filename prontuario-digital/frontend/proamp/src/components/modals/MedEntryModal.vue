<template>
    <BaseModal :show="show" @close="handleClose" :title="modalTitle">
        <MedEntryForm v-if="mode === 'view' || mode === 'create'" v-model="formData" :readonly="isViewMode" />

        <div v-if="mode === 'delete'">
            <p>Você tem certeza que deseja excluir esta entrada de prontuário? Esta ação não pode ser desfeita.</p>
            <div class="form-group">
                <label for="delete-reason" class="font-weight-bold">Motivo da Exclusão</label>
                <textarea id="delete-reason" v-model="deleteReason" class="form-control" rows="3" placeholder="É obrigatório informar o motivo da exclusão."></textarea>
            </div>
        </div>

        <template #footer>
            <button @click="handleClose" class="btn btn-secondary">
                {{ isViewMode ? 'Fechar' : 'Cancelar' }}
            </button>

            <button v-if="mode === 'create'" @click="submitCreate" class="btn btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Salvando...' : 'Salvar' }}
            </button>

            <button v-if="mode === 'delete'" @click="submitDelete" class="btn btn-danger" :disabled="isLoading || !deleteReason.trim()">
                {{ isLoading ? 'Excluindo...' : 'Confirmar Exclusão' }}
            </button>
        </template>
    </BaseModal>
</template>

<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import MedEntryForm from '@/components/forms/student/MedEntryForm.vue';
import { useAlertStore } from '@/stores/alertStore';
import medEntryService from '@/services/api/medEntryService';

const props = defineProps({
    show: {
        type: Boolean,
        required: true,
    },
    // 'view', 'create', 'delete'
    mode: {
        type: String,
        required: true,
        validator: (value) => ['view', 'create', 'delete'].includes(value),
    },
    // Med Entry object to view and delete
    entryData: {
        type: Object,
        default: () => ({}),
    },
    // For creating a new entry
    studentId: {
        type: [String, Number],
        default: null,
    },
});

const emit = defineEmits(['close', 'success']);

const alertStore = useAlertStore();
const isLoading = ref(false);
const formData = ref({});
const deleteReason = ref('');

// Look to entry data to populate the form
watch(
    () => props.entryData,
    (newEntry) => {
        formData.value = { ...newEntry };
    },
    { immediate: true, deep: true },
);

// Title and mode logic
const isViewMode = computed(() => props.mode === 'view');
const modalTitle = computed(() => {
    if (props.mode === 'view') return 'Detalhes da Entrada de Prontuário';
    if (props.mode === 'create') return 'Nova Entrada de Prontuário';
    if (props.mode === 'delete') return 'Excluir Entrada de Prontuário';
    return '';
});

// Methods
const handleClose = () => {
    if (!isLoading.value) {
        deleteReason.value = '';
        emit('close');
    }
};

const submitCreate = async () => {
    if (!props.studentId) {
        alertStore.triggerAlert({ message: 'ID do aluno não fornecido.', type: 'error' });
        return;
    }

    isLoading.value = true;
    try {
        const payload = {
            description: formData.value.description,
            notes: formData.value.notes,
        };
        // A API espera o student_id na query param
        await medEntryService.createEntry(props.studentId, payload);
        alertStore.showAlert('Entrada criada com sucesso!', 'success');
        emit('success'); // Emite um evento para o pai (ex: para recarregar a lista)
        handleClose();
    } catch (error) {
        alertStore.showAlert('Erro ao criar entrada.', 'error');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};

const submitDelete = async () => {
    if (!deleteReason.value.trim()) {
        alertStore.showAlert('O motivo da exclusão é obrigatório.', 'warning');
        return;
    }

    isLoading.value = true;
    try {
        const payload = { delete_reason: deleteReason.value };
        await medEntryService.deleteEntry(props.entryData.id, payload);
        alertStore.showAlert('Entrada excluída com sucesso!', 'success');
        emit('success');
        handleClose();
    } catch (error) {
        alertStore.showAlert('Erro ao excluir entrada.', 'error');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};
</script>
