<template>
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
            <h1 class="text-2xl font-lato-bold text-primary">Painel de usuários</h1>
            <p class="text-muted font-lato-regular mt-1">Gerencie os usuários</p>
        </div>

        <div class="mt-4 sm:mt-0 flex space-x-3">
            <button class="btn-primary" @click="openCreateModal">
                <i class="fas fa-plus mr-2"></i>
                Novo Usuário
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
                    <input v-model="filters.search" type="text" placeholder="Nome ou email" class="input-field pl-10" @input="debouncedSearch" />
                    <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                </div>
            </div>

            <!-- Role Filter -->
            <div>
                <label class="input-label">Função</label>
                <select v-model="filters.specialty" class="input-field" @change="applyFilters">
                    <option value="">Todas as especialidades</option>
                    <option value="psychologist">Psicologia</option>
                    <option value="physiotherapist">Fisioterapia</option>
                    <option value="social_worker">Assistencia Social</option>
                    <option value="speech_therapist">Fonoaudiologia</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Users Table -->
    <div class="card">
        <!-- Table Header with Stats -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <div>
                <h3 class="card-title">Lista de Usuários</h3>
                <p class="card-subtitle">{{ userStore.pros.length }} usuários {{ showingUserStatusText }} no total</p>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="userStore.loading" class="flex justify-center items-center h-64">
            <div class="loading-spinner w-8 h-8"></div>
            <span class="ml-3 text-gray-600 font-lato-regular">Carregando usuários...</span>
        </div>

        <!-- Error State -->
        <div v-else-if="userStore.error" class="alert alert-error">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            {{ userStore.error }}
            <button @click="loadUsers" class="ml-4 text-red-800 underline hover:no-underline">Tentar novamente</button>
        </div>

        <!-- Table View -->
        <div v-else-if="viewMode === 'table'" class="overflow-x-auto">
            <BaseTable :columns="tableColumns" :data="filteredUsers" :loading="userStore.loading" :backend-pagination="userStore.pagination" @row-click="handleRowClick" @action="handleTableAction" @page-change="handlePageChange" />
        </div>

        <!-- Empty State -->
        <div v-if="!userStore.loading && userStore.pros.length === 0" class="text-center py-12">
            <i class="fas fa-users text-4xl text-gray-400 mb-4"></i>
            <h3 class="text-lg font-lato-bold text-gray-900 mb-2">
                {{ hasActiveFilters ? 'Nenhum usuário encontrado' : 'Nenhum usuário cadastrado' }}
            </h3>
            <p class="text-gray-600 font-lato-regular mb-4">
                {{ hasActiveFilters ? 'Tente ajustar os filtros de busca' : 'Comece adicionando o primeiro usuário' }}
            </p>
        </div>
    </div>

    <UserModal :show="showUserModal" :user="selectedUser" :is-editing="false" @close="closeUserModal" />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useUserStore } from '@/stores/userStore';
import { useAlertStore } from '@/stores/alertStore';
import UserModal from '@/components/modals/UserModal.vue';

const userStore = useUserStore();
const alertStore = useAlertStore();

// States
const viewMode = ref('table');
const searchTimeout = ref(null);
const showUserModal = ref(false);
const selectedUser = ref(null);
const isShowingActive = ref(true);

const filters = ref({
    search: '',
    specialty: '',
});

// Table configuration
const tableColumns = ref([
    {
        key: 'avatar',
        label: '',
        width: '60px',
        type: 'avatar',
    },
    {
        key: 'first_name',
        label: 'Nome',
        sortable: true,
    },
    {
        key: 'email',
        label: 'E-mail',
        sortable: true,
    },
    {
        key: 'health_profile.specialty',
        label: 'Função',
        sortable: true,
        type: 'role',
    },
    {
        key: 'actions',
        label: 'Ações',
        width: '120px',
        type: 'actions',
        actions: [{ key: 'view', label: 'Visualizar', icon: 'fas fa-eye', color: 'blue' }],
    },
]);

// Computed
const filteredUsers = computed(() => {
    let users = [...userStore.pros];

    if (filters.value.search) {
        const search = filters.value.search.toLowerCase();
        users = users.filter((user) => {
            const name = getUserName(user).toLowerCase();
            const email = user.email.toLowerCase();

            return name.includes(search) || email.includes(search);
        });
    }

    if (filters.value.specialty) {
        users = users.filter((user) => user.health_profile.specialty === filters.value.specialty);
    }

    return users;
});

const hasActiveFilters = computed(() => {
    return filters.value.search || filters.value.role;
});

const showingUserStatusText = computed(() => {
    if (isShowingActive.value) {
        return 'ativos';
    }

    return 'inativos';
});

// Methods
const getUserName = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return user.email;
};

const closeUserModal = () => {
    showUserModal.value = false;
    selectedUser.value = null;
};

const debouncedSearch = () => {
    clearTimeout(searchTimeout.value);
    searchTimeout.value = setTimeout(() => {
        applyFilters();
    }, 300);
};

const applyFilters = async () => {
    loadUsers();
};

const loadUsers = async () => {
    try {
        await userStore.fetchAllHealthPros();
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
        alertStore.triggerAlert({ message: 'Erro ao carregar usuários: ' + error, type: 'error' });
    }
};

const handleRowClick = (user) => {
    handleView(user);
    console.log(user);
    console.log(user.health_profile.specialty);
    console.log(filters.value.specialty);
};

const handlePageChange = async (page) => {
    if (page >= 1 && page <= userStore.pagination.totalPages && !userStore.loading) {
        await loadUsers(page);
    }
};

const handleTableAction = ({ action, item }) => {
    switch (action) {
        case 'view':
            handleView(item);
            break;
    }
};

const handleView = (user) => {
    selectedUser.value = user;
    showUserModal.value = true;
};

// Lifecycle
onMounted(() => {
    loadUsers();
});
</script>
