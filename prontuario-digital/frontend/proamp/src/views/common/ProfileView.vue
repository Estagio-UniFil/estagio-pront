<template>
    <div class="card p-0">
        <div class="p-6 border-b border-primary">
            <h2 class="text-xl font-lato-bold text-primary">Meu Perfil</h2>
            <p class="text-secondary font-lato-regular mt-1">Veja e edite suas informações pessoais.</p>
        </div>
        <div class="p-6 flex flex-col md:flex-row items-start gap-8">
            <div class="flex flex-col items-center w-full md:w-48">
                <div class="avatar-placeholder">
                    <span>{{ userInitials }}</span>
                </div>
                <p class="font-lato-bold text-lg mt-3 text-primary">{{ user.first_name }} {{ user.last_name }}</p>
                <p class="text-sm text-muted">{{ user.email }}</p>
            </div>
            <div class="flex-1 w-full">
                <UserForm :user="user" :is-editing="true" :is-submitting="userStore.loading" :disable-role-field="true" :show-cancel-button="false" @submit="handleSave" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import UserForm from '@/components/forms/user/UserForm.vue';
import { useAuthStore } from '@/stores/authStore';
import { useUserStore } from '@/stores/userStore';
import { useAlertStore } from '@/stores/alertStore';

const authStore = useAuthStore();
const userStore = useUserStore();
const alertStore = useAlertStore();

const { user } = storeToRefs(authStore);

// Avatar
const userInitials = computed(() => {
    const firstName = user.value.first_name || '';
    const lastName = user.value.last_name || '';
    if (firstName && lastName) {
        return `${firstName[0]}${lastName[0]}`.toUpperCase();
    }
    return (firstName[0] || '').toUpperCase();
});

const handleSave = async (userData) => {
    try {
        const payload = {
            email: userData.email,
            first_name: userData.first_name,
            last_name: userData.last_name,
        };
        const updatedUser = await authStore.updateMe(payload);
        console.log(updatedUser);
        authStore.setUser(updatedUser);
        alertStore.triggerAlert({ message: 'Dados atualizados com sucesso.' });
    } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Não foi possível alterar seus dados. Tente novamente.';
        alertStore.triggerAlert({ message: errorMessage, type: 'error' });
    }
};
</script>

<style scoped>
/* --- Seção do Avatar --- */
.avatar-placeholder {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background-color: #3b82f6; /* Azul do botão Salvar */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem; /* 48px */
    font-weight: 700;
    font-family: 'Lato', sans-serif;
    border: 4px solid var(--bg-secondary);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card :deep(.input-label) {
    font-size: 0.75rem; /* 12px */
    text-transform: uppercase;
    color: var(--text-secondary); /* tom de cinza */
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.card :deep(.input-field) {
    border: none; /* Remove todas as bordas */
    border-bottom: 2px solid var(--bg-tertiary); /* Adiciona uma borda inferior sutil */
    background-color: transparent !important; /* Remove o fundo */
    border-radius: 0; /* Remove o arredondamento */
    padding-left: 0;
    padding-right: 0;
    padding-bottom: 0.5rem; /* Aumenta o espaçamento inferior */
    font-size: 1rem; /* 16px */
    color: var(--text-secondary); /* Cor de texto escuro */
    font-weight: 500;
    transition: border-color 0.2s ease-in-out;
}

/* Efeito ao focar no campo */
.card :deep(.input-field:focus) {
    outline: none; /* Remove a borda de foco padrão */
    box-shadow: none; /* Remove a sombra de foco padrão */
    border-bottom-color: #3b82f6; /* Destaca a borda inferior com a cor primária */
}

/* Estilo específico para o campo desabilitado (Tipo de Usuário) */
.card :deep(.input-field:disabled) {
    color: var(--text-secondary);
    cursor: not-allowed;
    border-bottom-color: transparent;
}

/* Ajusta o espaçamento dos botões de ação */
.card :deep(.flex.justify-end) {
    margin-top: 1.5rem; /* Adiciona mais espaço acima dos botões */
    padding-top: 1.5rem;
}

.card :deep(select#role.input-field:disabled) {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    padding-right: 0;
}
</style>
