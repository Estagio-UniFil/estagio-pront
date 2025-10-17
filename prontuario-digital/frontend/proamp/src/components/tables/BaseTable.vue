<template>
    <div class="overflow-x-auto">
        <table class="table">
            <!-- Table Header -->
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column.key" :style="{ width: column.width }" :class="[column.sortable ? 'cursor-pointer hover:bg-secondary' : '', column.align === 'center' ? 'text-center' : '', column.align === 'right' ? 'text-right' : '']" @click="column.sortable ? handleSort(column.key) : null">
                        <div class="flex items-center justify-between">
                            <span>{{ column.label }}</span>
                            <div v-if="column.sortable" class="ml-2">
                                <i :class="['fas text-xs transition-colors', sortColumn === column.key ? (sortDirection === 'asc' ? 'fa-sort-up text-blue-600' : 'fa-sort-down text-blue-600') : 'fa-sort text-gray-400']"></i>
                            </div>
                        </div>
                    </th>
                </tr>
            </thead>

            <!-- Table Body -->
            <tbody>
                <!-- Loading Row -->
                <tr v-if="loading">
                    <td :colspan="columns.length" class="text-center py-8">
                        <div class="flex items-center justify-center">
                            <div class="loading-spinner w-5 h-5 mr-3"></div>
                            <span class="text-gray-600 font-lato-regular">Carregando...</span>
                        </div>
                    </td>
                </tr>

                <!-- Empty State -->
                <tr v-else-if="displayData.length === 0">
                    <td :colspan="columns.length" class="text-center py-8">
                        <div class="text-gray-500">
                            <i class="fas fa-inbox text-2xl mb-2 block"> </i>
                            <span class="font-lato-regular">{{ emptyMessage }}</span>
                        </div>
                    </td>
                </tr>

                <!-- Data Rows -->
                <tr v-else v-for="(item, index) in displayData" :key="getRowKey(item, index)" class="hover:bg-secondary cursor-pointer transition-colors" @click="$emit('row-click', item, index)">
                    <td v-for="column in columns" :key="`${getRowKey(item, index)}-${column.key}`" :class="[column.align === 'center' ? 'text-center' : '', column.align === 'right' ? 'text-right' : '']">
                        <!-- Avatar Column -->
                        <div v-if="column.type === 'avatar'" class="flex items-center justify-center">
                            <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-lato-bold">
                                {{ getAvatarInitials(item) }}
                            </div>
                        </div>

                        <!-- Status Column -->
                        <span v-else-if="column.type === 'status'" :class="getStatusClass(getValue(item, column.key))">
                            {{ getStatusLabel(getValue(item, column.key)) }}
                        </span>

                        <!-- Role Column -->
                        <span v-else-if="column.type === 'role'" class="badge badge-primary">
                            {{ getRoleLabel(getValue(item, column.key)) }}
                        </span>

                        <!-- Report Type Column -->
                        <span v-else-if="column.type === 'report_type'" class="badge badge-primary">
                            {{ getReportLabel(getValue(item, column.key)) }}
                        </span>

                        <!-- Actions Column -->
                        <div v-else-if="column.type === 'actions'" class="flex items-center justify-center space-x-2">
                            <button v-for="action in column.actions" :key="action.key" @click.stop="$emit('action', { action: action.key, item, index })" :class="['p-1 rounded hover:bg-secondary transition-colors', `text-${action.color}-600 hover:text-${action.color}-800`]" :title="action.label">
                                <i :class="action.icon"></i>
                            </button>
                        </div>

                        <!-- Date Column -->
                        <span v-else-if="column.type === 'date'">
                            {{ formatDate(getValue(item, column.key)) }}
                        </span>

                        <!-- Datetime Column -->
                        <span v-else-if="column.type === 'datetime'">
                            {{ formatDateTime(getValue(item, column.key)) }}
                        </span>

                        <!-- Currency Column -->
                        <span v-else-if="column.type === 'currency'">
                            {{ formatCurrency(getValue(item, column.key)) }}
                        </span>

                        <!-- Default Column -->
                        <span v-else>
                            {{ getValue(item, column.key) }}
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="showPagination && !loading && shouldShowPagination" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <div class="text-sm text-muted font-lato-regular">Mostrando {{ paginationInfo.from }} até {{ paginationInfo.to }} de {{ paginationInfo.total }} registros</div>

            <div class="flex items-center space-x-2">
                <button @click="goToPreviousPage" :disabled="!canGoPrevious || loading" class="btn-outline px-3 py-1 text-xs disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fas fa-chevron-left"></i>
                </button>

                <div class="flex space-x-1">
                    <button v-for="page in visiblePageNumbers" :key="page" @click="goToSpecificPage(page)" :disabled="loading" :class="['px-3 py-1 text-xs rounded transition-colors', page === paginationInfo.currentPage ? 'bg-blue-600 text-white' : 'bg-primary text-secondary hover:bg-tertiary disabled:cursor-not-allowed']">
                        {{ page }}
                    </button>
                </div>

                <button @click="goToNextPage" :disabled="!canGoNext || loading" class="btn-outline px-3 py-1 text-xs disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { format, parseISO } from 'date-fns';

// Props
const props = defineProps({
    columns: {
        type: Array,
        required: true,
    },
    data: {
        type: Array,
        default: () => [],
    },
    loading: {
        type: Boolean,
        default: false,
    },
    emptyMessage: {
        type: String,
        default: ' Nenhum registro encontrado',
    },
    itemsPerPage: {
        type: Number,
        default: 10,
    },
    showPagination: {
        type: Boolean,
        default: true,
    },
    backendPagination: {
        type: Object,
        default: null, // { currentPage, totalPages, total, from, to }
    },
    rowKey: {
        type: String,
        default: 'id',
    },
});

// Emits
const emit = defineEmits(['row-click', 'action', 'sort', 'page-change']);

// State (apenas para paginação frontend)
const sortColumn = ref('');
const sortDirection = ref('asc');
const frontendCurrentPage = ref(1);

// Computed - Determina se usa paginação frontend ou backend
const isBackendPagination = computed(() => props.backendPagination !== null);

// Computed - Dados após ordenação (apenas para paginação frontend)
const sortedData = computed(() => {
    if (isBackendPagination.value || !sortColumn.value) return props.data;

    return [...props.data].sort((a, b) => {
        const aValue = getValue(a, sortColumn.value);
        const bValue = getValue(b, sortColumn.value);

        let comparison = 0;
        if (aValue < bValue) comparison = -1;
        else if (aValue > bValue) comparison = 1;

        return sortDirection.value === 'desc' ? comparison * -1 : comparison;
    });
});

// Computed - Dados a serem exibidos
const displayData = computed(() => {
    if (isBackendPagination.value) {
        // Paginação backend: mostra os dados como recebidos
        return props.data;
    }

    // Paginação frontend: aplica paginação local
    if (!props.showPagination) return sortedData.value;

    const start = (frontendCurrentPage.value - 1) * props.itemsPerPage;
    const end = start + props.itemsPerPage;
    return sortedData.value.slice(start, end);
});

// Computed - Informações de paginação unificadas
const paginationInfo = computed(() => {
    if (isBackendPagination.value) {
        // Usa dados do backend
        return props.backendPagination;
    }

    // Calcula paginação frontend
    const total = sortedData.value.length;
    const totalPages = Math.ceil(total / props.itemsPerPage);
    const from = total === 0 ? 0 : (frontendCurrentPage.value - 1) * props.itemsPerPage + 1;
    const to = Math.min(frontendCurrentPage.value * props.itemsPerPage, total);

    return {
        currentPage: frontendCurrentPage.value,
        totalPages,
        total,
        from,
        to,
    };
});

// Computed - Deve mostrar paginação?
const shouldShowPagination = computed(() => {
    if (isBackendPagination.value) {
        return paginationInfo.value.totalPages > 1;
    }
    return paginationInfo.value.total > props.itemsPerPage;
});

// Computed - Pode ir para página anterior?
const canGoPrevious = computed(() => paginationInfo.value.currentPage > 1);

// Computed - Pode ir para próxima página?
const canGoNext = computed(() => paginationInfo.value.currentPage < paginationInfo.value.totalPages);

// Computed - Números de páginas visíveis
const visiblePageNumbers = computed(() => {
    const current = paginationInfo.value.currentPage;
    const total = paginationInfo.value.totalPages;
    const delta = 2;
    const range = [];

    for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
        range.push(i);
    }

    return range;
});

// Methods
const getValue = (item, key) => {
    if (key.includes('.')) {
        return key.split('.').reduce((obj, key) => obj?.[key], item);
    }

    // Special handling for specific keys
    if (key === 'first_name') {
        return getUserName(item);
    }

    if (key === 'user_id') {
        return getUserNameRep(item);
    }

    if (key === 'city') {
        return getFullAddress(item);
    }

    if (key === 'dob') {
        return item[key];
    }

    if (key === 'user_id') {
        return getUserName(item);
    }

    return item[key];
};

const getUserName = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return user.email;
};

const getUserNameRep = (report) => {
    if (report.user_id.first_name && report.user_id.last_name) {
        return `${report.user_id.first_name} ${report.user_id.last_name}`;
    }
};

const getFullAddress = (student) => {
    if (student.city && student.state) {
        return `${student.city}/${student.state}`;
    }
};

const getAvatarInitials = (item) => {
    const name = getUserName(item);
    const names = name.split(' ');
    if (names.length >= 2) {
        return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase();
    }
    return name[0].toUpperCase();
};

const getStatusClass = (status) => {
    return status ? 'badge badge-success' : 'badge badge-danger';
};

const getStatusLabel = (status) => {
    return status ? 'Ativo' : 'Inativo';
};

const getRoleLabel = (role) => {
    const roleMap = {
        admin: 'Administrador',
        manager: 'Gestor',
        health_prof: 'Prof. de Saúde',
    };
    return roleMap[role] || role;
};

const getReportLabel = (report_type) => {
    const map = {
        GM: 'Relatório Mensal Geral',
        GSP: 'Relatório Geral por Período',
        SHAT: 'Histórico Geral de Estudante',
        SHSP: 'Relatório de Estudante por Período',
    };
    return map[report_type] || report_type;
};

const formatDate = (date) => {
    if (!date) return '-';
    return new Date(date).toLocaleDateString('pt-BR');
};

const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    return format(parseISO(dateString), 'dd/MM/yyyy HH:mm');
};

const formatCurrency = (value) => {
    if (!value) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(value);
};

const getRowKey = (item, index) => {
    return item[props.rowKey] || index;
};

const handleSort = (column) => {
    if (sortColumn.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn.value = column;
        sortDirection.value = 'asc';
    }

    emit('sort', { column, direction: sortDirection.value });
};

// Métodos de paginação
const goToSpecificPage = (page) => {
    if (page < 1 || page > paginationInfo.value.totalPages) return;

    if (isBackendPagination.value) {
        // Emite evento para o componente pai gerenciar
        emit('page-change', page);
    } else {
        // Gerencia paginação frontend localmente
        frontendCurrentPage.value = page;
    }
};

const goToPreviousPage = () => {
    const targetPage = paginationInfo.value.currentPage - 1;
    if (targetPage >= 1) {
        goToSpecificPage(targetPage);
    }
};

const goToNextPage = () => {
    const targetPage = paginationInfo.value.currentPage + 1;
    if (targetPage <= paginationInfo.value.totalPages) {
        goToSpecificPage(targetPage);
    }
};

// Watchers
watch(
    () => props.data,
    () => {
        // Reset frontend pagination quando dados mudam
        if (!isBackendPagination.value) {
            frontendCurrentPage.value = 1;
        }
    },
);
</script>
