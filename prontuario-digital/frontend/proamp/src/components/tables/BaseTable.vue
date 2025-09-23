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
                <tr v-else-if="sortedData.length === 0">
                    <td :colspan="columns.length" class="text-center py-8">
                        <div class="text-gray-500">
                            <i class="fas fa-inbox text-2xl mb-2 block"></i>
                            <span class="font-lato-regular">{{ emptyMessage }}</span>
                        </div>
                    </td>
                </tr>

                <!-- Data Rows -->
                <tr v-else v-for="(item, index) in paginatedData" :key="getRowKey(item, index)" class="hover:bg-secondary cursor-pointer transition-colors" @click="$emit('row-click', item, index)">
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
        <div v-if="showPagination && !loading && sortedData.length > itemsPerPage" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <div class="text-sm text-muted font-lato-regular">Mostrando {{ startItem }} até {{ endItem }} de {{ totalItems }} registros</div>

            <div class="flex items-center space-x-2">
                <button @click="previousPage" :disabled="currentPage === 1" class="btn-outline px-3 py-1 text-xs disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fas fa-chevron-left"></i>
                </button>

                <div class="flex space-x-1">
                    <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" :class="['px-3 py-1 text-xs rounded transition-colors', page === currentPage ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200']">
                        {{ page }}
                    </button>
                </div>

                <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-outline px-3 py-1 text-xs disabled:opacity-50 disabled:cursor-not-allowed">
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
        default: 'Nenhum registro encontrado',
    },
    itemsPerPage: {
        type: Number,
        default: 10,
    },
    showPagination: {
        type: Boolean,
        default: true,
    },
    rowKey: {
        type: String,
        default: 'id',
    },
});

// Emits
const emit = defineEmits(['row-click', 'action', 'sort']);

// State
const sortColumn = ref('');
const sortDirection = ref('asc');
const currentPage = ref(1);

// Computed
const sortedData = computed(() => {
    if (!sortColumn.value) return props.data;

    return [...props.data].sort((a, b) => {
        const aValue = getValue(a, sortColumn.value);
        const bValue = getValue(b, sortColumn.value);

        let comparison = 0;

        if (aValue < bValue) comparison = -1;
        else if (aValue > bValue) comparison = 1;

        return sortDirection.value === 'desc' ? comparison * -1 : comparison;
    });
});

const totalItems = computed(() => sortedData.value.length);
const totalPages = computed(() => Math.ceil(totalItems.value / props.itemsPerPage));

const paginatedData = computed(() => {
    if (!props.showPagination) return sortedData.value;

    const start = (currentPage.value - 1) * props.itemsPerPage;
    const end = start + props.itemsPerPage;
    return sortedData.value.slice(start, end);
});

const startItem = computed(() => {
    return totalItems.value === 0 ? 0 : (currentPage.value - 1) * props.itemsPerPage + 1;
});

const endItem = computed(() => {
    return Math.min(currentPage.value * props.itemsPerPage, totalItems.value);
});

const visiblePages = computed(() => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];

    for (let i = Math.max(2, currentPage.value - delta); i <= Math.min(totalPages.value - 1, currentPage.value + delta); i++) {
        range.push(i);
    }

    if (currentPage.value - delta > 2) {
        rangeWithDots.push(1, '...');
    } else {
        rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (currentPage.value + delta < totalPages.value - 1) {
        rangeWithDots.push('...', totalPages.value);
    } else if (totalPages.value > 1) {
        rangeWithDots.push(totalPages.value);
    }

    return rangeWithDots.filter((item, index, arr) => arr.indexOf(item) === index);
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

    if (key === 'city') {
        return getFullAddress(item);
    }

    if (key === 'dob') {
        return item[key];
    }

    return item[key];
};

const getUserName = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`;
    }
    return user.email;
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

const goToPage = (page) => {
    if (page !== '...' && page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
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

// Watchers
watch(
    () => props.data,
    () => {
        currentPage.value = 1;
    },
);
</script>
