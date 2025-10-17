<template>
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
            <h1 class="text-2xl font-lato-bold text-primary">Estudantes</h1>
            <p class="text-muted font-lato-regular mt-1">Gerencie prontuários de estudantes</p>
        </div>
    </div>
    <!-- Filters and Search -->
    <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Search -->
            <div class="md:col-span-2">
                <label class="input-label">Buscar</label>
                <div class="relative">
                    <input v-model="filters.search" type="text" placeholder="Nome do aluno..." class="input-field pl-10" @input="debouncedSearch" />
                    <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                </div>
            </div>
            <!-- Status Filter -->
            <div>
                <label class="input-label">Status</label>
                <select v-model="filters.status" class="input-field" @change="handleStatusChange">
                    <option value="active">Ativos</option>
                    <option value="inactive">Inativos</option>
                </select>
            </div>
        </div>
    </div>
    <!-- Users Table -->
    <div class="card">
        <!-- Table Header with Stats -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <div>
                <h3 class="card-title">Lista de estudantes</h3>
                <p class="card-subtitle">{{ filteredStudents.length }} de {{ studentStore.students.length }} estudantes</p>
            </div>
        </div>
        <!-- Loading State -->
        <div v-if="studentStore.loading" class="flex justify-center items-center h-64">
            <div class="loading-spinner w-8 h-8"></div>
            <span class="ml-3 text-gray-600 font-lato-regular">Carregando estudantes...</span>
        </div>
        <!-- Error State -->
        <div v-else-if="studentStore.error" class="alert alert-error">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            {{ studentStore.error }}
            <button @click="loadStudents" class="ml-4 text-red-800 underline hover:no-underline">Tentar novamente</button>
        </div>
        <!-- Table View -->
        <div class="overflow-x-auto">
            <BaseTable :columns="tableColumns" :data="filteredStudents" :loading="studentStore.loading" @row-click="handleRowClick" @action="handleTableAction" />
        </div>
        <!-- Empty State -->
        <div v-if="!studentStore.loading && filteredStudents.length === 0" class="text-center py-12">
            <i class="fas fa-users text-4xl text-gray-400 mb-4"></i>
            <h3 class="text-lg font-lato-bold text-gray-900 mb-2">
                {{ hasActiveFilters ? 'Nenhum estudante encontrado' : 'Nenhum estudante cadastrado' }}
            </h3>
            <p class="text-gray-600 font-lato-regular mb-4">
                {{ hasActiveFilters ? 'Tente ajustar os filtros de busca' : 'Comece adicionando o primeiro estudante' }}
            </p>
            <button v-if="!hasActiveFilters" @click="openCreateModal" class="btn-primary">
                <i class="fas fa-plus mr-2"></i>
                Adicionar Estudante
            </button>
        </div>
    </div>

    <MedEntriesStudentModal :show="showStudentModal" :student="selectedStudent" @close="closeStudentModal"></MedEntriesStudentModal>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useStudentStore } from '@/stores/studentStore';
import MedEntriesStudentModal from '@/components/modals/MedEntriesStudentModal.vue';

const studentStore = useStudentStore();

// Modal states
const showConfirmModal = ref(false);
const itemForAction = ref(null);
const modalAction = ref('');
const modalActionName = ref('');
const modalTitle = ref('');
const modalMessage = ref('');
const showStudentModal = ref(false);
const selectedStudent = ref(null);
const isEditingMode = ref(false);

// States
const currentPage = ref(1);
const searchTimeout = ref(null);
const filters = ref({
    search: '',
    status: 'active',
});

// Table configuration
const tableColumns = computed(() => [
    {
        key: 'name',
        label: 'Nome',
        sortable: true,
    },
    {
        key: 'cgm',
        label: 'CGM',
        sortable: true,
    },
    {
        key: 'dob',
        label: 'Data de nascimento',
        sortable: true,
        type: 'date',
    },
    {
        key: 'guardian',
        label: 'Responsável',
        sortable: true,
    },
    {
        key: 'city',
        label: 'Cidade/UF',
        sortable: true,
    },
    {
        key: 'actions',
        label: 'Ações',
        width: '120px',
        type: 'actions',
        actions: filters.value.status === 'active' ? [{ key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' }] : [{ key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' }],
    },
]);

// Computed
const filteredStudents = computed(() => {
    let students = [...studentStore.students];
    if (filters.value.search) {
        const search = filters.value.search.toLowerCase();
        students = students.filter((student) => {
            const name = getStudentName(student).toLowerCase();
            return name.includes(search);
        });
    }
    return students;
});

const hasActiveFilters = computed(() => {
    return filters.value.search;
});

// Methods
const closeStudentModal = () => {
    showStudentModal.value = false;
    selectedStudent.value = null;
};

const getStudentName = (student) => {
    if (student?.name) {
        return `${student.name}`;
    }
    return '';
};

const debouncedSearch = () => {
    clearTimeout(searchTimeout.value);
    searchTimeout.value = setTimeout(applyFilters, 300);
};

const applyFilters = () => {
    currentPage.value = 1;
};

const handleStatusChange = async () => {
    currentPage.value = 1;
    await loadStudents();
};

const getStatusBoolean = (status) => {
    return status === 'active';
};

const loadStudents = async () => {
    const isActive = getStatusBoolean(filters.value.status);
    try {
        await studentStore.fetchStudents(isActive);
    } catch (error) {
        console.error('Erro ao carregar estudantes:', error);
    }
};

const openCreateModal = () => {
    selectedStudent.value = null;
    isEditingMode.value = true;
    showStudentModal.value = true;
};

const handleRowClick = (student) => {
    handleView(student);
    console.log('Ver detalhes do estudante:', student);
};

const handleTableAction = ({ action, item }) => {
    switch (action) {
        case 'view':
            handleView(item);
            break;
    }
};

const closeConfirmModal = () => {
    showConfirmModal.value = false;
    setTimeout(() => {
        itemForAction.value = null;
        modalAction.value = '';
        modalActionName.value = '';
    }, 300);
};

const handleView = (student) => {
    selectedStudent.value = student;
    showStudentModal.value = true;
};

// Lifecycle
onMounted(loadStudents);

watch(
    () => filters.value.search,
    () => {
        currentPage.value = 1;
    },
);
</script>
