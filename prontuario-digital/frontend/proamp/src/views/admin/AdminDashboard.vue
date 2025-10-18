<template>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Funcionários -->
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

        <!-- Total Alunos Ativos -->
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

        <!-- Atendimentos Hoje -->
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

        <!-- Prontuários Atualizados -->
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

                <router-link :to="{ name: 'admin-reports' }" class="btn-outline w-full">
                    <i class="fas fa-file-download mr-2"></i>
                    Gerar Relatório
                </router-link>

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
import { endOfToday, endOfYesterday, startOfToday } from 'date-fns';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const userStore = useUserStore();
const studentStore = useStudentStore();
const medEntryStore = useMedEntryStore();

const totalUsers = computed(() => userStore.users.length);
const activeStudents = computed(() => studentStore.students.filter((student) => student.active).length);
const totalEntries = computed(() => medEntryStore.entries.length);

const loadData = async () => {
    try {
        await userStore.fetchUsers();
        await studentStore.fetchStudents(true);
        await medEntryStore.fetchAllEntries();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
};

const stats = computed(() => ({
    totalEmployees: totalUsers.value,
    activeStudents: activeStudents.value,
    appointmentsThisMonth: totalEntries.value,
    recordsToday: totalEntries.value,
}));

// Chart
const chartData = ref({
    labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
    datasets: [
        {
            label: 'Atendimentos',
            data: [31, 40, 28, 51, 42, 109, 100],
            backgroundColor: 'rgba(26, 86, 219, 0.2)',
            borderColor: 'rgba(26, 86, 219, 1)',
            tension: 0.3,
            fill: true,
        },
    ],
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
