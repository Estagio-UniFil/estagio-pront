=== MedEntriesStudentModal.vue ===
<template>
    <BaseModal :show="show" :title="modalTitle" @close="handleClose">
        <!-- Dados do Estudante -->
        <div class="mb-6">
            <h4 class="text-lg font-semibold mb-4">Dados do Estudante</h4>
            <StudentForm :student="studentData" :is-editing="false" :is-submitting="false" :read-only="true" />
        </div>

        <!-- Seção de Entradas Médicas -->
        <div>
            <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-semibold">Entradas de Prontuário</h4>
                <button @click="refreshEntries" class="btn-secondary" :disabled="medEntryStore.isLoading">
                    <i class="fas fa-sync-alt mr-2" :class="{ 'animate-spin': medEntryStore.isLoading }"></i>
                    Atualizar
                </button>
            </div>

            <!-- Loading State -->
            <div v-if="medEntryStore.isLoading" class="flex justify-center items-center py-8">
                <div class="loading-spinner w-6 h-6"></div>
                <span class="ml-3 text-gray-600">Carregando entradas...</span>
            </div>

            <!-- Error State -->
            <div v-else-if="medEntryStore.error" class="alert alert-error mb-4">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                {{ medEntryStore.error }}
                <button @click="refreshEntries" class="ml-4 text-red-800 underline hover:no-underline">Tentar novamente</button>
            </div>

            <!-- Table -->
            <div v-else class="overflow-x-auto">
                <BaseTable :columns="tableColumns" :data="medEntryStore.entries" :loading="medEntryStore.isLoading" @row-click="handleRowClick" @action="handleTableAction" />
            </div>
        </div>
    </BaseModal>

    <MedEntryModal :show="showModal" :mode="modalMode" :entry-data="selectedEntry" @close="closeModalDetails" @success="handleSuccess" />
</template>

<script setup>
import { computed, watch, ref } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import StudentForm from '@/components/forms/student/StudentForm.vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useMedEntryStore } from '@/stores/medEntryStore';
import MedEntryModal from '@/components/modals/MedEntryModal.vue';

const medEntryStore = useMedEntryStore();

const showModal = ref(false);
const modalMode = ref('view');
const selectedEntry = ref({});

const props = defineProps({
    show: {
        type: Boolean,
        default: false,
    },
    student: {
        type: Object,
        default: null,
    },
});

const emit = defineEmits(['close']);

// Computed properties
const modalTitle = computed(() => {
    if (props.student?.name) {
        return `Prontuário - ${props.student.name}`;
    }
    return 'Prontuário do Estudante';
});

const studentData = computed(() => props.student || {});

// Table configuration
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
]);

// Methods
const handleClose = () => {
    emit('close');
};

const handleRowClick = (entry) => {
    console.log('Entrada clicada:', entry);
    selectedEntry.value = entry;
    modalMode.value = 'view';
    showModal.value = true;
};

const closeModalDetails = () => {
    showModal.value = false;
    selectedEntry.value = {};
};

const handleTableAction = ({ action, item }) => {
    switch (action) {
        case 'view':
            handleRowClick(item);
            break;
        default:
            console.warn('Ação não implementada:', action);
    }
};

const fetchEntries = async () => {
    if (props.student?.id) {
        try {
            await medEntryStore.fetchStudentEntries(props.student.id);
        } catch (error) {
            console.error('Erro ao carregar entradas do estudante:', error);
        }
    }
};

const refreshEntries = () => {
    fetchEntries();
};

// Watchers
watch(
    () => [props.show, props.student?.id],
    ([show, studentId]) => {
        if (show && studentId) {
            fetchEntries();
        }
    },
    { immediate: true },
);

// Clear data when modal is closed
watch(
    () => props.show,
    (show) => {
        if (!show) {
            medEntryStore.entries = [];
        }
    },
);
</script>
