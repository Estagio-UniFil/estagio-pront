<template>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
            <h1 class="text-2xl font-lato-bold text-primary">Logs de Geração de Relatórios</h1>
            <p class="text-muted font-lato-regular mt-1">Visualize o histórico de geração de relatórios para auditoria.</p>
        </div>
        <button class="btn-outline" @click="openExportModal">
            <i class="fas fa-download mr-2"></i>
            Exportar
        </button>
    </div>

    <div class="card">
        <div class="mb-6">
            <h3 class="card-title">Últimos Relatórios</h3>
            <p class="card-subtitle" v-if="!reportStore.isLoading">{{ reportStore.logEntries.length }} entradas encontradas</p>
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
            <BaseTable :columns="tableColumns" :data="reportStore.logEntries" :loading="reportStore.isLoading" />
        </div>

        <div v-if="!reportStore.isLoading && reportStore.logEntries.length === 0" class="text-center py-12">
            <i class="fas fa-file-medical-alt text-4xl text-gray-400 mb-4"></i>
            <h3 class="text-lg font-lato-bold text-gray-900 mb-2">Nenhuma entrada de prontuário encontrada</h3>
            <p class="text-gray-600 font-lato-regular">Ainda não há nenhuma entrada de prontuário registrada.</p>
        </div>
    </div>

    <ReportParamsModal :show="isModalVisible" @close="closeModal" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useMedEntryStore } from '@/stores/medEntryStore';
import { useReportStore } from '@/stores/reportStore';
import ReportParamsModal from '@/components/modals/ReportParamsModal.vue';

const medEntryStore = useMedEntryStore();
const reportStore = useReportStore();

const isModalVisible = ref(false);

const tableColumns = ref([
    {
        key: 'date',
        label: 'Data da Entrada',
        sortable: true,
        type: 'datetime',
    },
    {
        key: 'user_id',
        label: 'Usuário',
        sortable: true,
    },
    {
        key: 'report_type',
        label: 'Tipo de Relatório',
        sortable: true,
        type: 'report_type',
    },
]);

// Methods
const openExportModal = () => {
    console.log('modal de exportação');
    isModalVisible.value = true;
};

const fetchEntries = () => {
    reportStore.fetchAllLogEntries();
};

const closeModal = () => {
    isModalVisible.value = false;
};

onMounted(() => {
    fetchEntries();
});
</script>
