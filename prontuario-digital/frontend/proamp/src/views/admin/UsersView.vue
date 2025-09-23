<template>
    <AdminLayout>
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
                    <select v-model="filters.role" class="input-field" @change="applyFilters">
                        <option value="">Todas as funções</option>
                        <option value="admin">Administrador</option>
                        <option value="manager">Gestor</option>
                        <option value="health_prof">Profissional de Saúde</option>
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
                    <p class="card-subtitle">{{ filteredUsers.length }} de {{ userStore.users.length }} usuários</p>
                </div>

                <!-- View Toggle -->
                <div class="mt-4 sm:mt-0 flex bg-primary rounded-lg p-1">
                    <button @click="viewMode = 'table'" :class="['px-3 py-1 rounded text-sm font-lato-regular transition-colors', viewMode === 'table' ? 'bg-secondary text-blue-600 shadow-sm cursor-pointer' : 'text-primary hover:text-muted cursor-pointer']">
                        <i class="fas fa-list mr-1 cursor-pointer"></i>
                        Tabela
                    </button>
                    <button @click="viewMode = 'cards'" :class="['px-3 py-1 rounded text-sm font-lato-regular transition-colors cursor-pointer', viewMode === 'cards' ? 'bg-secondary text-blue-600 shadow-sm cursor-pointer' : 'text-primary hover:text-muted']">
                        <i class="fas fa-th-large mr-1"></i>
                        Cards
                    </button>
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
                <BaseTable :columns="tableColumns" :data="filteredUsers" :loading="userStore.loading" @row-click="handleRowClick" @action="handleTableAction" />
            </div>

            <!-- Cards View -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="user in filteredUsers" :key="user.id" class="bg-tertiary border border-primary rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="handleRowClick(user)">
                    <!-- User Avatar and Basic Info -->
                    <div class="flex items-center mb-3">
                        <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-lato-bold mr-3">
                            {{ getUserInitials(user) }}
                        </div>
                        <div class="flex-1">
                            <h4 class="font-lato-bold text-primary">{{ getUserName(user) }}</h4>
                            <p class="text-sm text-primary font-lato-regular">{{ getRoleLabel(user.role) }}</p>
                        </div>
                    </div>

                    <!-- Contact Info -->
                    <div class="space-y-1 mb-3">
                        <p class="text-sm text-secondary font-lato-regular">
                            <i class="fas fa-envelope w-4 mr-2"></i>
                            {{ user.email }}
                        </p>
                    </div>

                    <!-- Actions -->
                    <div class="flex justify-end space-x-2">
                        <button @click.stop="handleEdit(user)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button @click.stop="handleDelete(user)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="!userStore.loading && filteredUsers.length === 0" class="text-center py-12">
                <i class="fas fa-users text-4xl text-gray-400 mb-4"></i>
                <h3 class="text-lg font-lato-bold text-gray-900 mb-2">
                    {{ hasActiveFilters ? 'Nenhum usuário encontrado' : 'Nenhum usuário cadastrado' }}
                </h3>
                <p class="text-gray-600 font-lato-regular mb-4">
                    {{ hasActiveFilters ? 'Tente ajustar os filtros de busca' : 'Comece adicionando o primeiro usuário' }}
                </p>
                <button v-if="!hasActiveFilters" @click="openCreateModal" class="btn-primary">
                    <i class="fas fa-plus mr-2"></i>
                    Adicionar Usuário
                </button>
            </div>
        </div>

        <!-- Pagination -->
        <!-- <div v-if="filteredUsers.length > 0" class="mt-6 flex justify-between items-center">
            <p class="text-sm text-gray-600 font-lato-regular">Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} até {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} de {{ filteredUsers.length }} usuários</p>

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

        <!-- New user modal -->
        <UserModal :show="showUserModal" :user="selectedUser" :is-editing="isEditingMode" :is-submitting="userStore.loading" @close="closeUserModal" @submit="handleSaveUser" />

        <!-- Delete modal -->
        <ConfirmModal v-if="itemToDelete" :show="showDeleteModal" :entryName="getUserName(itemToDelete)" @confirm="handleConfirmDelete" :action-type="'deletar'" @cancel="closeDeleteModal" />

        <!-- Custom alert message -->
        <!-- <div class="fixed top-24 left-1/2 -translate-x-1/2 z-50 w-full max-w-xl px-4">
            <Transition name="fade">
                <BaseAlert v-if="showAlert" type="success" title="Sucesso!" :message="alertMessage" @close="closeAlert" />
            </Transition>
        </div> -->
    </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import BaseTable from '@/components/tables/BaseTable.vue';
import { useUserStore } from '@/stores/userStore';
import { useAlertStore } from '@/stores/alertStore';
// import BaseAlert from '@/components/common/BaseAlert.vue';
import UserModal from '@/components/modals/UserModal.vue';
import ConfirmModal from '@/components/modals/ConfirmModal.vue';

const router = useRouter();
const userStore = useUserStore();
const alertStore = useAlertStore();

// States
const viewMode = ref('table');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const searchTimeout = ref(null);
const showDeleteModal = ref(false);
const itemToDelete = ref(null);
const showUserModal = ref(false);
const selectedUser = ref(null);
const isEditingMode = ref(false);

const filters = ref({
    search: '',
    role: '',
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
        key: 'role',
        label: 'Função',
        sortable: true,
        type: 'role',
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
const filteredUsers = computed(() => {
    let users = [...userStore.users];

    // Search filter
    if (filters.value.search) {
        const search = filters.value.search.toLowerCase();
        users = users.filter((user) => {
            const name = getUserName(user).toLowerCase();
            const email = user.email.toLowerCase();

            return name.includes(search) || email.includes(search);
        });
    }

    // Role filter
    if (filters.value.role) {
        users = users.filter((user) => user.role === filters.value.role);
    }

    return users;
});

const totalPages = computed(() => {
    return Math.ceil(filteredUsers.value.length / itemsPerPage.value);
});

const hasActiveFilters = computed(() => {
    return filters.value.search || filters.value.role;
});

// Methods
const openDeleteModal = (user) => {
    itemToDelete.value = user;
    showDeleteModal.value = true;
};

const closeUserModal = () => {
    showUserModal.value = false;
    selectedUser.value = null;
};

// const closeAlert = () => {
//     showAlert.value = false;
// };

const closeDeleteModal = () => {
    showDeleteModal.value = false;
    itemToDelete.value = null;
};

// const openAlertWithTimeout = () => {
//     showAlert.value = false;
//     setTimeout(() => {
//         showAlert.value = true;

//         setTimeout(() => {
//             showAlert.value = false;
//         }, 3000);
//     }, 100);
// };

const getUserName = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return user.email;
};

const getUserInitials = (user) => {
    const name = getUserName(user);
    const names = name.split(' ');
    if (names.length >= 2) {
        return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase();
    }
    return name[0].toUpperCase();
};

const getRoleLabel = (role) => {
    const roleMap = {
        admin: 'Administrador',
        manager: 'Gestor',
        health_prof: 'Prof. de Saúde',
    };
    return roleMap[role] || role;
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

const loadUsers = async () => {
    try {
        await userStore.fetchUsers();
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
        alertStore.triggerAlert({ message: 'Erro ao carregar usuários:' + error });
    }
};

const openCreateModal = () => {
    selectedUser.value = null;
    isEditingMode.value = true;
    showUserModal.value = true;
};

const handleRowClick = (user) => {
    handleView(user);
};

const handleSaveUser = async (userData) => {
    try {
        if (userData.id) {
            await userStore.updateUser(userData.id, userData);
            alertStore.triggerAlert({ message: 'Usuário atualizado com sucesso.' });
        } else {
            await userStore.createUser(userData);
            alertStore.triggerAlert({ message: 'Novo usuário criado com sucesso.' });
        }
        await loadUsers();
        closeUserModal();
    } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Não foi possível salvar o usuário. Tente novamente.';
        alertStore.triggerAlert({ message: errorMessage, type: 'error' });
    }
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

const handleView = (user) => {
    selectedUser.value = user;
    isEditingMode.value = false;
    showUserModal.value = true;
};

const handleEdit = (user) => {
    selectedUser.value = { ...user };
    isEditingMode.value = true;
    showUserModal.value = true;
};

const handleDelete = (user) => {
    openDeleteModal(user);
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

const handleConfirmDelete = async () => {
    if (!itemToDelete.value) return;

    try {
        await userStore.deleteUser(itemToDelete.value.id);

        // alertMessage.value = `O usuário ${getUserName(itemToDelete.value)} foi desativado com sucesso.`;
        // openAlertWithTimeout();
        const userName = getUserName(itemToDelete.value);
        alertStore.triggerAlert({ message: `O usuário ${userName} foi desativado com sucesso.` });
    } catch (error) {
        console.error('Erro ao desativar:', error);
        const errorMessage = error.response?.data?.detail || 'Não foi possível desativar o usuário. Tente novamente.';
        alertStore.triggerAlert({ message: errorMessage, type: 'error' });
    } finally {
        closeDeleteModal();
    }
};

// Lifecycle
onMounted(() => {
    loadUsers();
});

// Watchers
watch(
    () => filters.value,
    () => {
        currentPage.value = 1;
    },
    { deep: true },
);
</script>

<style>
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.3s ease,
        transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
