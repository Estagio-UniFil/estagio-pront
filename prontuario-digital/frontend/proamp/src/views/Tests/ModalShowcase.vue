<template>
    <div class="p-8">
        <div class="fixed top-24 left-1/2 -translate-x-1/2 z-50 w-full max-w-xl px-4">
            <Transition name="fade">
                <BaseAlert v-if="showAlert" type="success" title="Sucesso" :closable="true" @close="closeAlert"> Ação de salvar executada com sucesso! </BaseAlert>
            </Transition>
        </div>

        <h1 class="text-3xl font-lato-black mb-6">Testando Modais</h1>
        <p class="text-gray-600 mb-8">Esta página demonstra a utilização do componente BaseModal com diferentes configurações.</p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="card">
                <h3 class="card-title">Modal Padrão</h3>
                <p class="card-subtitle mb-4">Um modal simples com título, conteúdo e um botão de fechar.</p>
                <button @click="showSimpleModal = true" class="btn-primary">Abrir Modal Padrão</button>
            </div>

            <div class="card">
                <h3 class="card-title">Modal com Rodapé</h3>
                <p class="card-subtitle mb-4">Modal com botões de ação no rodapé.</p>
                <button @click="showFooterModal = true" class="btn-primary">Abrir Modal com Rodapé</button>
            </div>

            <div class="card">
                <h3 class="card-title">Modal Inclosable</h3>
                <p class="card-subtitle mb-4">Um modal que só pode ser fechado por um botão interno.</p>
                <button @click="showUnclosableModal = true" class="btn-primary">Abrir Modal Inclosable</button>
            </div>
        </div>

        <BaseModal :show="showSimpleModal" title="Modal Padrão" @close="showSimpleModal = false">
            <p>Este é um modal padrão com um título e um conteúdo simples. Ele pode ser fechado clicando fora ou no botão "x".</p>
        </BaseModal>

        <BaseModal :show="showFooterModal" title="Modal com Ações" @close="showFooterModal = false">
            <p>Este modal tem uma área de rodapé personalizada com botões para "Salvar" e "Cancelar".</p>
            <template #footer>
                <button @click="showFooterModal = false" class="btn-secondary">Cancelar</button>
                <button @click="handleSave" class="btn-primary">Salvar</button>
            </template>
        </BaseModal>

        <BaseModal :show="showUnclosableModal" title="Atenção!" :closable="false" maxWidth="32rem">
            <p class="text-red-600 font-lato-bold mb-4">Você precisa confirmar sua ação antes de fechar este modal.</p>
            <p>Este é um modal crítico. Você não pode fechá-lo clicando no fundo ou usando a tecla ESC.</p>
            <template #footer>
                <button @click="showUnclosableModal = false" class="btn-danger">Entendido</button>
            </template>
        </BaseModal>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import BaseAlert from '@/components/common/BaseAlert.vue';

const showSimpleModal = ref(false);
const showFooterModal = ref(false);
const showUnclosableModal = ref(false);
const showAlert = ref(false);

const handleSave = () => {
    // Em vez de um alert nativo, definimos o estado para mostrar nosso alerta
    openAlertWithTimeout();
    showFooterModal.value = false;
};

const openAlertWithTimeout = () => {
    // Certifica-se de que o alerta anterior esteja fechado
    showAlert.value = false;

    // Aguarda um ciclo de renderização para a transição
    setTimeout(() => {
        showAlert.value = true;

        // Define o timer para fechar o alerta após 3 segundos
        setTimeout(() => {
            showAlert.value = false;
        }, 3000); // 3000 milissegundos = 3 segundos
    }, 100); // Um pequeno delay para garantir que a transição de entrada funcione corretamente
};

// Adicione um método para fechar o alerta
const closeAlert = () => {
    showAlert.value = false;
};
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
