<template>
    <AdminLayout>
        <!-- Page Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
            <div>
                <h1 class="text-2xl font-lato-bold text-gray-900">Estudantes</h1>
                <p class="text-gray-600 font-lato-regular mt-1">Gerencie estudantes</p>
            </div>
            <div class="mt-4 sm:mt-0 flex space-x-3">
                <button class="btn-primary" @click="openCreateModal">
                    <i class="fas fa-plus mr-2"></i>
                    Novo Estudante
                </button>
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
        <!-- Pagination -->
        <div v-if="filteredStudents.length > 0" class="mt-6 flex justify-between items-center">
            <p class="text-sm text-gray-600 font-lato-regular">Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} até {{ Math.min(currentPage * itemsPerPage, filteredStudents.length) }} de {{ filteredStudents.length }} estudantes</p>
            <div class="flex space-x-2">
                <button @click="previousPage" :disabled="currentPage === 1" class="btn-outline px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fas fa-chevron-left mr-1"></i>
                    Anterior
                </button>
                <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-outline px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed">
                    Próximo
                    <i class="fas fa-chevron-right ml-1"></i>
                </button>
            </div>
        </div>
    </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useStudentStore } from '@/stores/studentStore';

const router = useRouter();
const studentStore = useStudentStore();

// States
const currentPage = ref(1);
const itemsPerPage = ref(10);
const searchTimeout = ref(null);
const filters = ref({
    search: '',
    status: 'active',
});

// Table configuration
const tableColumns = ref([
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
        actions: [
            { key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' },
            { key: 'edit', label: 'Editar', icon: 'fas fa-edit', color: 'blue' },
            { key: 'delete', label: 'Excluir', icon: 'fas fa-trash', color: 'red' },
        ],
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

const totalPages = computed(() => {
    return Math.ceil(filteredStudents.value.length / itemsPerPage.value);
});

const hasActiveFilters = computed(() => {
    return filters.value.search;
});

// Methods
const getStudentName = (student) => {
    if (student.name) {
        return `${student.name}`;
    }
};

const debouncedSearch = () => {
    clearTimeout(searchTimeout.value);
    searchTimeout.value = setTimeout(() => {
        applyFilters();
    }, 300);
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
    // Navegar para página de criação ou abrir modal
    console.log('Abrir modal de criação');
};

const handleRowClick = (user) => {
    console.log('Ver detalhes do usuário:', user);
};

const handleTableAction = ({ action, item }) => {
    switch (action) {
        case 'view':
            handleView(item);
            break;
        case 'edit':
            handleEdit(item);
            break;
        case 'delete':
            handleDelete(item);
            break;
    }
};

const handleView = (student) => {
    console.log('Visualizar estudante:', student);
};

const handleEdit = (student) => {
    console.log('Editar estudante:', student);
};

const handleDelete = (student) => {
    if (confirm(`Tem certeza que deseja destativar ${getStudentName(student)}?`)) {
        studentStore.deleteStudent(student.id);
    }
};

const previousPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

// Lifecycle
onMounted(() => {
    loadStudents();
});

watch(
    () => filters.value.search,
    () => {
        currentPage.value = 1;
    },
);
</script>
