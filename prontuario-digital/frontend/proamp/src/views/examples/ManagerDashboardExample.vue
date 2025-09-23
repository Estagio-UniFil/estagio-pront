<!-- Exemplo de página usando ManagerLayout -->
<template>
    <ManagerLayout>
        <div class="space-y-6">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Dashboard do Gestor</h2>
                <p class="text-gray-600 dark:text-gray-300">Esta é uma página de exemplo usando o ManagerLayout. Observe que a navegação e o cabeçalho são específicos para gestores.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">Equipe</h3>
                    <p class="text-blue-700 dark:text-blue-300">Gerencie sua equipe de profissionais</p>
                </div>

                <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">Alunos</h3>
                    <p class="text-green-700 dark:text-green-300">Acompanhe o progresso dos alunos</p>
                </div>

                <div class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">Agenda</h3>
                    <p class="text-purple-700 dark:text-purple-300">Visualize e gerencie a agenda</p>
                </div>
            </div>
        </div>
    </ManagerLayout>
</template>

<script setup>
import ManagerLayout from '@/components/layouts/ManagerLayout.vue';
</script>
