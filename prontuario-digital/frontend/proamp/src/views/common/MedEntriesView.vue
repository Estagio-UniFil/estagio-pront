<template>
    <AdminLayout>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
            <div>
                <h1 class="text-2xl font-lato-bold text-gray-900">Entradas de Prontuário</h1>
                <p class="text-gray-600 font-lato-regular mt-1">Visualize as últimas entradas de prontuário registradas no sistema.</p>
            </div>
            <button class="btn-outline" @click="openExportModal">
                <i class="fas fa-download mr-2"></i>
                Exportar
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

        <MedEntryModal :show="isModalVisible" :mode="modalMode" :entry-data="selectedEntry" @close="closeModal" @success="fetchEntries" />
    </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import { ref, onMounted } from 'vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useMedEntryStore } from '@/stores/medEntryStore';
import { useReportStore } from '@/stores/reportStore';
import MedEntryModal from '@/components/modals/MedEntryModal.vue';

const medEntryStore = useMedEntryStore();
const reportStore = useReportStore();

const isModalVisible = ref(false);
const modalMode = ref('view');
const selectedEntry = ref(null);

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
        actions: [{ key: 'view', label: 'Visualizar Detalhes', icon: 'fas fa-eye', color: 'blue' }],
    },
]);

// Métodos
const openExportModal = () => {
    console.log('modal de exportação');
    //debugger;
    reportStore.exportMonthlyReport();
};

const fetchEntries = () => {
    medEntryStore.fetchAllEntries();
};

const openViewModal = (entry) => {
    selectedEntry.value = entry;
    modalMode.value = 'view';
    isModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
    selectedEntry.value = null;
};

// Funções utilitárias
const format = (dateString) => new Date(dateString).toLocaleString('pt-BR');
const truncate = (text, length = 50) => (text.length > length ? text.substring(0, length) + '...' : text);

const handleTableAction = ({ action, item }) => {
    if (action === 'view') {
        openViewModal(item);
        console.log('Visualizar entrada:', item);
    }
};

const handleRowClick = (entry) => {
    openViewModal(entry);
    console.log('Ver detalhes da entrada:', entry);
};

onMounted(() => {
    fetchEntries();
});
</script>
