<template>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
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
                    <p class="text-2xl font-lato-bold text-primary">temp</p>
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
                    <p class="text-2xl font-lato-bold text-primary">temp</p>
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

            <div class="h-64 flex items-center justify-center bg-tertiary rounded-lg">
                <div class="text-center">
                    <i class="fas fa-chart-line text-4xl text-muted mb-4"></i>
                    <p class="text-muted font-lato-regular">Gráfico de atividade</p>
                    <p class="text-sm text-muted font-lato-light">Em desenvolvimento</p>
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
                    Nova Entrada
                </router-link>

                <router-link :to="{ name: 'admin-students' }" class="btn-outline w-full">
                    <i class="fas fa-user-graduate mr-2"></i>
                    Exportar Relatório
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';

import { useStudentStore } from '@/stores/studentStore';
import { useMedEntryStore } from '@/stores/medEntryStore';
import { useAuthStore } from '@/stores/authStore';

const studentStore = useStudentStore();
const medEntryStore = useMedEntryStore();
const authStore = useAuthStore();

const activeStudents = computed(() => studentStore.students.filter((student) => student.active).length);
const totalEntries = computed(() => medEntryStore.entries.length);

const loadData = async () => {
    try {
        await studentStore.fetchStudents(true);
        await medEntryStore.fetchAllEntries();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
};

const stats = computed(() => ({
    activeStudents: activeStudents.value,
    appointmentsThisMonth: totalEntries.value,
}));

// Lifecycle
onMounted(async () => {
    console.log('Dashboard carregado');
    console.log(authStore.fetchMe());
});
</script>
