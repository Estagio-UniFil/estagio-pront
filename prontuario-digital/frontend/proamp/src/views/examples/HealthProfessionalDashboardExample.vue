<!-- Exemplo de página usando HealthProfessionalLayout -->
<template>
    <HealthProfessionalLayout>
        <div class="space-y-6">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Dashboard do Profissional de Saúde</h2>
                <p class="text-gray-600 dark:text-gray-300">Esta é uma página de exemplo usando o HealthProfessionalLayout. Observe que a navegação inclui itens específicos para profissionais de saúde.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-red-900 dark:text-red-100 mb-2">Pacientes</h3>
                    <p class="text-red-700 dark:text-red-300">Gerencie seus pacientes</p>
                </div>

                <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">Consultas</h3>
                    <p class="text-blue-700 dark:text-blue-300">Agende e acompanhe consultas</p>
                </div>

                <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">Prontuários</h3>
                    <p class="text-green-700 dark:text-green-300">Acesse prontuários médicos</p>
                </div>

                <div class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">Agenda</h3>
                    <p class="text-purple-700 dark:text-purple-300">Visualize sua agenda</p>
                </div>
            </div>
        </div>
    </HealthProfessionalLayout>
</template>

<script setup>
import HealthProfessionalLayout from '@/components/layouts/HealthProfessionalLayout.vue';
</script>
