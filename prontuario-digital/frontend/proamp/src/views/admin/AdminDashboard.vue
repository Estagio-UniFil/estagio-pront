<template>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total employees -->
        <div class="card">
            <div class="flex items-center">
                <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
                    <i class="fas fa-user-md text-2xl"></i>
                </div>
                <div>
                    <p class="text-sm font-lato-regular text-muted">Funcionários</p>
                    <p class="text-2xl font-lato-bold text-primary">{{ stats.totalEmployees }}</p>
                </div>
            </div>
        </div>

        <!-- Active students -->
        <div class="card">
            <div class="flex items-center">
                <div class="p-3 rounded-full bg-green-100 text-green-600 mr-4">
                    <i class="fas fa-users text-2xl"></i>
                </div>
                <div>
                    <p class="text-sm font-lato-regular text-muted">Alunos Ativos</p>
                    <p class="text-2xl font-lato-bold text-primary">{{ stats.activeStudents }}</p>
                </div>
            </div>
        </div>

        <!-- Appointments today -->
        <div class="card">
            <div class="flex items-center">
                <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
                    <i class="fas fa-calendar-check text-2xl"></i>
                </div>
                <div>
                    <p class="text-sm font-lato-regular text-muted">Atendimentos Mensais</p>
                    <p class="text-2xl font-lato-bold text-primary">{{ stats.appointmentsThisMonth }}</p>
                </div>
            </div>
        </div>

        <!-- Records today -->
        <div class="card">
            <div class="flex items-center">
                <div class="p-3 rounded-full bg-orange-100 text-orange-600 mr-4">
                    <i class="fas fa-file-medical text-2xl"></i>
                </div>
                <div>
                    <p class="text-sm font-lato-regular text-muted">Prontuários Hoje</p>
                    <p class="text-2xl font-lato-bold text-primary">{{ stats.recordsToday }}</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Charts and Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Activity Chart -->
        <div class="lg:col-span-2 card">
            <div class="card-header">
                <h3 class="card-title">Atividade dos Últimos 7 Dias</h3>
                <p class="card-subtitle">Atendimentos e atualizações de prontuários</p>
            </div>

            <div class="pt-4" style="height: 280px">
                <Line :data="chartData" :options="chartOptions" />
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Ações Rápidas</h3>
                <p class="card-subtitle">Acesso rápido às principais funções</p>
            </div>

            <div class="space-y-3">
                <router-link :to="{ name: 'admin-users' }" class="btn-outline w-full">
                    <i class="fas fa-user-plus mr-2"></i>
                    Novo Funcionário
                </router-link>

                <router-link :to="{ name: 'admin-students' }" class="btn-outline w-full">
                    <i class="fas fa-user-graduate mr-2"></i>
                    Novo Aluno
                </router-link>

                <button class="btn-outline w-full" @click="exportReport">
                    <i class="fas fa-chart-line mr-2"></i>
                    Exportar Relatório Mensal
                </button>

                <router-link :to="{ name: 'admin-profile' }" class="btn-outline w-full">
                    <i class="fa-solid fa-user mr-2"></i>
                    Meu Perfil
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';

import { useUserStore } from '@/stores/userStore';
import { useStudentStore } from '@/stores/studentStore';
import { useMedEntryStore } from '@/stores/medEntryStore';
import { useReportStore } from '@/stores/reportStore';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const userStore = useUserStore();
const studentStore = useStudentStore();
const medEntryStore = useMedEntryStore();
const reportStore = useReportStore();

const totalUsers = computed(() => userStore.users.length);
const activeStudents = computed(() => studentStore.students.filter((student) => student.active).length);
const totalMonthlyEntries = computed(() => filteredMonthlyData.value.length);
const totalDailyEntries = computed(() => filteredDailyData.value.length);

const loadData = async () => {
    try {
        await userStore.fetchUsers();
        await studentStore.fetchStudents(true);
        await medEntryStore.fetchAllEntries();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
};

const params = { reportType: 'general_monthly', year: null, month: null, studentId: null, startDate: '', endDate: '' };
const exportReport = () => {
    reportStore.exportMonthlyReport(params);
};

const filteredMonthlyData = computed(() => {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    return medEntryStore.entries.filter((entry) => {
        const entryDate = new Date(entry.entry_date);

        return entryDate.getMonth() === currentMonth && entryDate.getFullYear() === currentYear;
    });
});

const filteredDailyData = computed(() => {
    const currentDate = new Date();
    const today = currentDate.getDate();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    return medEntryStore.entries.filter((entry) => {
        const entryDate = new Date(entry.entry_date);

        return entryDate.getDate() === today && entryDate.getMonth() === currentMonth && entryDate.getFullYear() === currentYear;
    });
});

const stats = computed(() => ({
    totalEmployees: totalUsers.value,
    activeStudents: activeStudents.value,
    appointmentsThisMonth: totalMonthlyEntries.value,
    recordsToday: totalDailyEntries.value,
}));

// Chart
const chartData = computed(() => {
    const labels = [];
    const dataPoints = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
        const targetDate = new Date();
        targetDate.setDate(today.getDate() - i);

        labels.push(targetDate.toLocaleDateString('pt-BR', { weekday: 'short' }));

        const targetDay = targetDate.getDate();
        const targetMonth = targetDate.getMonth();
        const targetYear = targetDate.getFullYear();

        const countForDay = medEntryStore.entries.filter((entry) => {
            const entryDate = new Date(entry.entry_date);
            return entryDate.getDate() === targetDay && entryDate.getMonth() === targetMonth && entryDate.getFullYear() === targetYear;
        }).length;

        dataPoints.push(countForDay);
    }

    return {
        labels: labels,
        datasets: [
            {
                label: 'Atendimentos',
                data: dataPoints,
                backgroundColor: 'rgba(26, 86, 219, 0.2)',
                borderColor: 'rgba(26, 86, 219, 1)',
                tension: 0.3,
                fill: true,
            },
        ],
    };
});

const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
    },
    scales: {
        y: {
            beginAtZero: true,
        },
    },
});

// Lifecycle
onMounted(async () => {
    console.log('Dashboard carregado');
    await loadData();
});
</script>
