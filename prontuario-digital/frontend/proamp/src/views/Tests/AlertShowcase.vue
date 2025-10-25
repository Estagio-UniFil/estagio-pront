<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
        <div class="p-8 max-w-lg mx-auto bg-white rounded-xl shadow-lg">
            <div class="fixed top-5 right-5 z-[100] w-full max-w-sm">
                <BaseAlert v-if="show" :type="type" :title="title" :message="message" @close="alertStore.hideAlert()" />
            </div>
            <h1 class="text-2xl font-lato-bold mb-6 text-gray-900">Mostruário de Alertas (ProAMP)</h1>
            <p class="mb-6 text-gray-600 font-lato-regular">Clique nos botões abaixo para disparar os diferentes tipos de alertas globais. Os alertas devem aparecer no canto da tela (conforme configurado no seu layout principal, ex: <code>App.vue</code>).</p>
            <div class="flex flex-col space-y-4">
                <button @click="showSuccess" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 font-lato-bold">Disparar Alerta de Sucesso</button>
                <button @click="showError" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 font-lato-bold">Disparar Alerta de Erro</button>
                <button @click="showWarning" class="px-4 py-2 bg-yellow-500 text-gray-800 rounded-lg hover:bg-yellow-600 transition-colors duration-200 font-lato-bold">Disparar Alerta de Aviso</button>
                <button @click="showInfo" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-lato-bold">Disparar Alerta de Informação</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAlertStore } from '@/stores/alertStore';
import { storeToRefs } from 'pinia';
import BaseAlert from '@/components/common/BaseAlert.vue';

const alertStore = useAlertStore();

const { show, message, title, type } = storeToRefs(alertStore);

const showSuccess = () => {
    alertStore.triggerAlert({
        message: 'O item foi salvo com sucesso no banco de dados.',
        type: 'success',
        title: 'Sucesso!',
    });
};

const showError = () => {
    alertStore.triggerAlert({
        message: 'Não foi possível completar a operação. Verifique os campos.',
        type: 'error',
        title: 'Falha na Validação',
    });
};

const showWarning = () => {
    alertStore.triggerAlert({
        message: 'Seu token de acesso expirará em breve.',
        type: 'warning',
        title: 'Atenção!',
    });
};

const showInfo = () => {
    alertStore.triggerAlert({
        message: 'A manutenção do sistema está agendada para domingo às 22:00.',
        type: 'info',
        title: 'Aviso do Sistema',
    });
};
</script>

<style scoped></style>
