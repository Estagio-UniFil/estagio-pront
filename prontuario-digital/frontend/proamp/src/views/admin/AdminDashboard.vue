<template>
    <AdminLayout>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Total Funcionários -->
            <div class="card">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
                        <i class="fas fa-user-md text-2xl"></i>
                    </div>
                    <div>
                        <p class="text-sm font-lato-regular text-gray-600">Funcionários</p>
                        <p class="text-2xl font-lato-bold text-gray-900">{{ stats.totalEmployees }}</p>
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
                        <p class="text-sm font-lato-regular text-gray-600">Alunos Ativos</p>
                        <p class="text-2xl font-lato-bold text-gray-900">{{ stats.activeStudents }}</p>
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
                        <p class="text-sm font-lato-regular text-gray-600">Atendimentos Mensais</p>
                        <p class="text-2xl font-lato-bold text-gray-900">{{ stats.appointmentsThisMonth }}</p>
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
                        <p class="text-sm font-lato-regular text-gray-600">Prontuários Hoje</p>
                        <p class="text-2xl font-lato-bold text-gray-900">{{ stats.recordsToday }}</p>
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
                    <p class="card-subtitle">Consultas e atualizações de prontuários</p>
                </div>

                <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                    <div class="text-center">
                        <i class="fas fa-chart-line text-4xl text-gray-400 mb-4"></i>
                        <p class="text-gray-500 font-lato-regular">Gráfico de atividade</p>
                        <p class="text-sm text-gray-400 font-lato-light">Em desenvolvimento</p>
                    </div>
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

                    <router-link :to="{ name: 'admin-settings' }" class="btn-outline w-full">
                        <i class="fas fa-cog mr-2"></i>
                        Configurações
                    </router-link>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import AdminLayout from '@/components/layouts/AdminLayout.vue';

import { useUserStore } from '@/stores/userStore';
import { useStudentStore } from '@/stores/studentStore';

const userStore = useUserStore();
const studentStore = useStudentStore();

const totalUsers = computed(() => userStore.users.length);
const activeStudents = computed(() => studentStore.students.filter((student) => student.active).length);

const loadData = async () => {
    try {
        await userStore.fetchUsers();
        await studentStore.fetchStudents(true);
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
};

const stats = computed(() => ({
    totalEmployees: totalUsers.value,
    activeStudents: activeStudents.value,
    appointmentsThisMonth: 12,
    recordsToday: 8,
}));

// Lifecycle
onMounted(async () => {
    console.log('Dashboard carregado');
    await loadData();
});
</script>
