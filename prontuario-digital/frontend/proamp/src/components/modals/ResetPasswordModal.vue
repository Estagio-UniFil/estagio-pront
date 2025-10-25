<template>
    <BaseModal :show="show" title="Redefinir Senha" max-width="500px" @close="close">
        <template #default>
            <form @submit.prevent="handleSubmit" class="px-1">
                <p class="mb-4 font-lato-regular text-primary">
                    Você está redefinindo a senha para o usuário:
                    <strong class="text-primary">{{ userName }}</strong
                    >.
                </p>
                <p class="mb-6 font-lato-regular text-sm text-muted">O usuário será solicitado a alterar esta senha no próximo login.</p>

                <div class="mb-4">
                    <label for="new_password" class="input-label">Nova Senha</label>
                    <input id="new_password" v-model="form.new_password" type="password" class="input-field" required />
                </div>

                <div>
                    <label for="confirm_password" class="input-label">Confirmar Nova Senha</label>
                    <input id="confirm_password" v-model="form.confirm_password" type="password" class="input-field" required />
                    <p v-if="error" class="text-red-500 text-sm mt-1">
                        {{ error }}
                    </p>
                </div>
            </form>
        </template>

        <template #footer>
            <div class="flex justify-end space-x-3">
                <button type="button" class="btn-outline" @click="close">Cancelar</button>
                <button type="button" class="btn-primary" :disabled="isSubmitting" @click="handleSubmit">
                    <span v-if="isSubmitting" class="loading-spinner-white w-4 h-4 mr-2"></span>
                    {{ isSubmitting ? 'Salvando...' : 'Redefinir Senha' }}
                </button>
            </div>
        </template>
    </BaseModal>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import BaseModal from './BaseModal.vue';

const props = defineProps({
    show: {
        type: Boolean,
        default: false,
    },
    user: {
        type: Object,
        default: null,
    },
    isSubmitting: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['close', 'submit']);

const form = ref({
    new_password: '',
    confirm_password: '',
});
const error = ref('');

const userName = computed(() => {
    if (!props.user) return '';
    return props.user.first_name ? `${props.user.first_name} ${props.user.last_name}` : props.user.email;
});

const close = () => {
    emit('close');
};

const handleSubmit = () => {
    error.value = '';
    if (form.value.new_password !== form.value.confirm_password) {
        error.value = 'As senhas não coincidem.';
        return;
    }
    if (!props.user) return;

    emit('submit', {
        userId: props.user.id,
        passwordData: {
            new_password: form.value.new_password,
            confirm_password: form.value.confirm_password,
        },
    });
};

watch(
    () => props.show,
    (newVal) => {
        if (newVal) {
            form.value.new_password = '';
            form.value.confirm_password = '';
            error.value = '';
        }
    },
);
</script>
