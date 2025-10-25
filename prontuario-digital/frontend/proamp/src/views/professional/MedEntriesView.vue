<template>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
            <h1 class="text-2xl font-lato-bold text-primary">Entradas de Prontuário</h1>
            <p class="text-muted font-lato-regular mt-1">Visualize as últimas entradas de prontuário registradas no sistema.</p>
        </div>
        <button class="btn-outline" @click="openCreateModal">
            <i class="fas fa-plus mr-2"></i>
            Nova Entrada
        </button>
    </div>

    <div class="card">
        <div class="mb-6">
            <h3 class="card-title">Últimas Entradas</h3>
            <p class="card-subtitle" v-if="!medEntryStore.isLoading">{{ medEntryStore.entries.length }} entradas encontradas</p>
        </div>

        <div v-if="medEntryStore.isLoading" class="flex justify-center items-center h-64">
            <div class="loading-spinner w-8 h-8"></div>
            <span class="ml-3 text-gray-600 font-lato-regular">Carregando entradas...</span>
        </div>

        <div v-else-if="medEntryStore.error" class="alert alert-error">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            {{ medEntryStore.error }}
            <button @click="fetchEntries" class="ml-4 text-red-800 underline hover:no-underline">Tentar novamente</button>
        </div>

        <div class="overflow-x-auto">
            <BaseTable :columns="tableColumns" :data="medEntryStore.entries" :loading="medEntryStore.isLoading" @row-click="handleRowClick" @action="handleTableAction" />
        </div>

        <div v-if="!medEntryStore.isLoading && medEntryStore.entries.length === 0" class="text-center py-12">
            <i class="fas fa-file-medical-alt text-4xl text-gray-400 mb-4"></i>
            <h3 class="text-lg font-lato-bold text-gray-900 mb-2">Nenhuma entrada de prontuário encontrada</h3>
            <p class="text-gray-600 font-lato-regular">Ainda não há nenhuma entrada de prontuário registrada.</p>
        </div>
    </div>

    <!-- Modal Simplificado -->
    <MedEntryModal :show="showModal" :mode="modalMode" :entry-data="selectedEntry" @close="closeModal" @success="handleSuccess" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useMedEntryStore } from '@/stores/medEntryStore';
import MedEntryModal from '@/components/modals/MedEntryModal.vue';
import { useAlertStore } from '@/stores/alertStore';

const medEntryStore = useMedEntryStore();
const alertStore = useAlertStore();

const showModal = ref(false);
const modalMode = ref('view');
const selectedEntry = ref({});

const tableColumns = ref([
    {
        key: 'entry_date',
        label: 'Data da Entrada',
        sortable: true,
        type: 'datetime',
    },
    {
        key: 'student.name',
        label: 'Estudante',
        sortable: true,
    },
    {
        key: 'healthpro.first_name',
        label: 'Profissional',
        sortable: true,
    },
    {
        key: 'description',
        label: 'Descrição',
        sortable: false,
    },
    {
        key: 'actions',
        label: 'Ações',
        width: '100px',
        type: 'actions',
        actions: [
            { key: 'view', label: 'Visualizar Detalhes', icon: 'fas fa-eye', color: 'blue' },
            { key: 'delete', label: 'Excluir', icon: 'fas fa-trash', color: 'red' },
        ],
    },
]);

const fetchEntries = () => {
    medEntryStore.fetchAllEntries();
};

const openCreateModal = () => {
    modalMode.value = 'create';
    selectedEntry.value = {};
    showModal.value = true;
};

const openViewModal = (entry) => {
    selectedEntry.value = entry;
    modalMode.value = 'view';
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    selectedEntry.value = {};
};

const handleSuccess = () => {
    showModal.value = false;
    alertStore.triggerAlert({ message: 'Entrada de prontuário registrada.', type: 'success' });
    fetchEntries();
};

const handleTableAction = ({ action, item }) => {
    if (action === 'view') {
        openViewModal(item);
    }
    if (action === 'delete') {
        handleDelete(item);
    }
};

const handleDelete = (entry) => {
    modalMode.value = 'delete';
    selectedEntry.value = entry;
    showModal.value = true;
    console.log(entry);
};

const handleRowClick = (entry) => {
    openViewModal(entry);
};

onMounted(() => {
    fetchEntries();
});
</script>
