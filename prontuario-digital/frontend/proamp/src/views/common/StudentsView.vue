<template>
    <AdminLayout>
        <!-- Page Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
            <div>
                <h1 class="text-2xl font-lato-bold text-primary">Estudantes</h1>
                <p class="text-muted font-lato-regular mt-1">Gerencie estudantes</p>
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
        <!-- <div v-if="filteredStudents.length > 0" class="mt-6 flex justify-between items-center">
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
        </div> -->

        <StudentModal :show="showStudentModal" :student="selectedStudent" :is-editing="isEditingMode" :is-submitting="studentStore.loading" @close="closeStudentModal" @submit="handleSaveStudent" />

        <!-- Confirm Modal -->
        <ConfirmModal v-if="itemForAction" :show="showConfirmModal" :title="modalTitle" :message="modalMessage" :action-type="modalActionName" :entryName="getStudentName(itemForAction)" @confirm="handleConfirmAction" @cancel="closeConfirmModal" />
    </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useStudentStore } from '@/stores/studentStore';
import { useAlertStore } from '@/stores/alertStore';
import ConfirmModal from '@/components/modals/ConfirmModal.vue';
import StudentModal from '@/components/modals/StudentModal.vue';

const router = useRouter();
const studentStore = useStudentStore();
const alertStore = useAlertStore();

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
const itemsPerPage = ref(10);
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
        actions:
            filters.value.status === 'active'
                ? [
                      { key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' },
                      { key: 'edit', label: 'Editar', icon: 'fas fa-edit', color: 'blue' },
                      { key: 'delete', label: 'Excluir', icon: 'fas fa-trash', color: 'red' },
                  ]
                : [
                      { key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' },
                      { key: 'restore', label: 'Reativar', icon: 'fas fa-undo', color: 'green' },
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
        case 'edit':
            handleEdit(item);
            break;
        case 'delete':
            handleDelete(item);
            break;
        case 'restore':
            handleRestore(item);
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

const handleSaveStudent = async (studentData) => {
    try {
        if (studentData.id) {
            await studentStore.updateStudent(studentData.id, studentData);
            alertStore.triggerAlert({ message: 'Estudante atualizado com sucesso.' });
        } else {
            await studentStore.createStudent(studentData);
            alertStore.triggerAlert({ message: 'Novo estudante criado com sucesso.' });
        }
        await loadStudents();
        closeStudentModal();
    } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Não foi possível salvar o estudante. Tente novamente.';
        alertStore.triggerAlert({ message: errorMessage, type: 'error' });
    }
};

const handleConfirmAction = async () => {
    if (!itemForAction.value) return;

    try {
        if (modalAction.value === 'delete') {
            await studentStore.deleteStudent(itemForAction.value.id);
            //alertMessage.value = `O estudante ${getStudentName(itemForAction.value)} foi desativado com sucesso.`;
            alertStore.triggerAlert({ message: `O estudante ${getStudentName(itemForAction.value)} foi desativado com sucesso.` });
        } else if (modalAction.value === 'restore') {
            await studentStore.restoreStudent(itemForAction.value.id);
            //alertMessage.value = `O estudante ${getStudentName(itemForAction.value)} foi reativado com sucesso.`;
            alertStore.triggerAlert({ message: `O estudante ${getStudentName(itemForAction.value)} foi reativado com sucesso.` });
        }
        await loadStudents();
    } catch (error) {
        //console.error(`Erro ao ${modalAction.value === 'delete' ? 'desativar' : 'reativar'} estudante:`, error);
        const errorMessage = error.response?.data?.detail || `Não foi possível ${modalAction.value === 'delete' ? 'desativar' : 'reativar'} o estudante. Tente novamente.`;
        alertStore.triggerAlert({ message: errorMessage, type: 'error' });
    } finally {
        closeConfirmModal();
    }
};

const handleView = (student) => {
    selectedStudent.value = student;
    isEditingMode.value = false;
    showStudentModal.value = true;
};

const handleEdit = (student) => {
    selectedStudent.value = { ...student };
    isEditingMode.value = true;
    showStudentModal.value = true;
};

const handleDelete = (student) => {
    itemForAction.value = student;
    modalAction.value = 'delete';
    modalTitle.value = 'Confirmar Desativação';
    modalActionName.value = 'desativar';
    modalMessage.value = 'Você tem certeza de que deseja desativar este estudante? Ele será movido para a lista de inativos.';
    showConfirmModal.value = true;
};

const handleRestore = (student) => {
    itemForAction.value = student;
    modalAction.value = 'restore';
    modalTitle.value = 'Confirmar Restauração';
    modalActionName.value = 'restaurar';
    modalMessage.value = 'Você tem certeza de que deseja reativar este estudante? Ele voltará para a lista de ativos.';
    showConfirmModal.value = true;
};

const previousPage = () => {
    if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
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
