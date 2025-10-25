<template>
    <AuthLayout>
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />

        <div class="card max-w-md mx-auto">
            <div class="text-center mb-6">
                <h1 class="card-title">Crie sua nova senha</h1>
                <p class="card-subtitle mt-2">Olá, {{ authStore.user?.first_name }}! Por segurança, seu primeiro acesso requer a definição de uma senha pessoal.</p>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- New Password -->
                <div>
                    <label for="new_password" class="input-label">Nova Senha</label>
                    <div class="relative">
                        <input id="new_password" v-model="form.new_password" :type="showPassword ? 'text' : 'password'" class="input-field pr-12" :class="{ error: errors.new_password }" placeholder="Mínimo de 8 caracteres" required :disabled="authStore.isLoading" />
                        <button type="button" @click="togglePassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted hover:text-secondary">
                            <span v-if="showPassword"><i class="fa-solid fa-eye-slash"></i></span>
                            <span v-else><i class="fa-solid fa-eye"></i></span>
                        </button>
                    </div>
                    <p v-if="errors.new_password" class="input-error">{{ errors.new_password }}</p>
                </div>

                <!-- Confirm new password -->
                <div>
                    <label for="confirm_password" class="input-label">Confirmar Nova Senha</label>
                    <div class="relative">
                        <input id="confirm_password" v-model="form.confirm_password" :type="showConfirmPassword ? 'text' : 'password'" class="input-field pr-12" :class="{ error: errors.confirm_password }" placeholder="Confirme sua nova senha" required :disabled="authStore.isLoading" />
                        <button type="button" @click="toggleConfirmPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted hover:text-secondary">
                            <span v-if="showConfirmPassword"><i class="fa-solid fa-eye-slash"></i></span>
                            <span v-else><i class="fa-solid fa-eye"></i></span>
                        </button>
                    </div>
                    <p v-if="errors.confirm_password" class="input-error">{{ errors.confirm_password }}</p>
                </div>

                <!-- Save button -->
                <button type="submit" class="btn-primary w-full flex items-center justify-center" :disabled="authStore.isLoading || !isFormValid">
                    <div v-if="authStore.isLoading" class="loading-spinner w-4 h-4 mr-2"></div>
                    {{ authStore.isLoading ? 'Salvando...' : 'Salvar e Acessar' }}
                </button>
            </form>
            <div class="mt-6 text-center text-sm text-muted">
                <p>Precisa de ajuda? Entre em contato com o administrador.</p>
            </div>
        </div>
    </AuthLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useAlertStore } from '@/stores/alertStore';
import AuthLayout from '@/components/layouts/AuthLayout.vue';

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();

const form = ref({
    new_password: '',
    confirm_password: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const errors = ref({});

const isFormValid = computed(() => {
    return form.value.new_password && form.value.confirm_password && !authStore.isLoading;
});

const togglePassword = () => (showPassword.value = !showPassword.value);
const toggleConfirmPassword = () => (showConfirmPassword.value = !showConfirmPassword.value);

const validateForm = () => {
    errors.value = {};
    if (!form.value.new_password) {
        errors.value.new_password = 'A nova senha é obrigatória.';
    } else if (form.value.new_password.length < 8) {
        errors.value.new_password = 'A senha deve ter pelo menos 8 caracteres.';
    }

    if (form.value.new_password !== form.value.confirm_password) {
        errors.value.confirm_password = 'As senhas não coincidem.';
    }

    if (Object.keys(errors.value).length > 0) {
        alertStore.triggerAlert({ message: 'Por favor, corrija os erros no formulário.', type: 'warning', title: 'Atenção' });
        return false;
    }

    return true;
};

const handleSubmit = async () => {
    authStore.clearError();
    if (!validateForm()) {
        return;
    }

    try {
        await authStore.setPassword({
            new_password: form.value.new_password,
            confirm_password: form.value.confirm_password,
        });

        alertStore.triggerAlert({ message: 'Senha definida com sucesso!', type: 'success' });

        const role = authStore.userRole;
        setTimeout(() => {
            if (role === 'admin') router.push({ name: 'admin-dashboard' });
            else if (role === 'manager') router.push({ name: 'manager-dashboard' });
            else if (role === 'health_prof') router.push({ name: 'health-dashboard' });
            else router.push('/login');
        }, 1500);
    } catch (error) {
        alertStore.triggerAlert({ message: authStore.error, type: 'error', title: 'Falha ao salvar' });
        console.error('Falha ao definir a senha:', error);
    }
};

onMounted(() => {
    authStore.clearError();
});
</script>

<style scoped>
.loading-spinner {
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>
