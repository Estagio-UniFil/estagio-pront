<template>
    <AuthLayout>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css" integrity="sha512-DxV+EoADOkOygM4IR9yXP8Sb2qwgidEmeqAEmDKIOfPRQZOWbXCzLC6vjbZyy0vPisbH2SyW27+ddLVCN+OMzQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <div class="card max-w-md mx-auto">
            <!-- Mensagem de erro -->
            <div v-if="authStore.error" class="alert alert-error mb-6">
                {{ authStore.error }}
            </div>

            <form @submit.prevent="handleLogin" class="space-y-6">
                <!-- Email -->
                <div>
                    <label class="input-label">E-mail</label>
                    <input v-model="form.email" type="email" class="input-field" :class="{ 'border-red-500': errors.email }" placeholder="seu@email.com" required :disabled="authStore.isLoading" />
                    <p v-if="errors.email" class="input-error">{{ errors.email }}</p>
                </div>

                <!-- Senha -->
                <div>
                    <label class="input-label">Senha</label>
                    <div class="relative">
                        <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input-field pr-12" :class="{ 'border-red-500': errors.password }" placeholder="Sua senha" required :disabled="authStore.isLoading" />
                        <button type="button" @click="togglePassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700" :disabled="authStore.isLoading">
                            <span v-if="showPassword"><i class="fa-solid fa-eye-slash"></i></span>
                            <span v-else><i class="fa-solid fa-eye"></i></span>
                        </button>
                    </div>
                    <p v-if="errors.password" class="input-error">{{ errors.password }}</p>
                </div>

                <!-- Lembrar de mim -->
                <div class="flex items-center">
                    <input v-model="form.rememberMe" type="checkbox" id="remember" class="mr-2" :disabled="authStore.isLoading" />
                    <label for="remember" class="text-sm text-gray-600"> Lembrar de mim </label>
                </div>

                <!-- Botão de login -->
                <button type="submit" class="btn-primary w-full" :disabled="authStore.isLoading || !isFormValid">
                    <div v-if="authStore.isLoading" class="loading-spinner w-4 h-4 mr-2"></div>
                    {{ authStore.isLoading ? 'Entrando...' : 'Entrar' }}
                </button>
            </form>

            <!-- Links adicionais -->
            <div class="mt-6 text-center text-sm text-gray-600">
                <p>Esqueceu sua senha? Entre em contato com o administrador.</p>
            </div>
        </div>
    </AuthLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import AuthLayout from '@/components/layouts/AuthLayout.vue';

const router = useRouter();
const authStore = useAuthStore();

// Estado do formulário
const form = ref({
    email: '',
    password: '',
    rememberMe: false,
});

// Estado da UI
const showPassword = ref(false);
const errors = ref({});

// Computed
const isFormValid = computed(() => {
    return form.value.email && form.value.password && !authStore.isLoading;
});

// Métodos
const togglePassword = () => {
    showPassword.value = !showPassword.value;
};

const validateForm = () => {
    errors.value = {};

    if (!form.value.email) {
        errors.value.email = 'E-mail é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
        errors.value.email = 'E-mail inválido';
    }

    if (!form.value.password) {
        errors.value.password = 'Senha é obrigatória';
    } else if (form.value.password.length < 3) {
        errors.value.password = 'Senha deve ter pelo menos 3 caracteres';
    }

    return Object.keys(errors.value).length === 0;
};

const handleLogin = async () => {
    // Limpa erros anteriores
    authStore.clearError();

    // Valida formulário
    if (!validateForm()) {
        return;
    }

    try {
        await authStore.login(form.value.email, form.value.password);

        // Redireciona baseado no role do usuário
        const redirectTo = getDefaultRoute();
        router.push(redirectTo);
    } catch (error) {
        // Erro já está sendo tratado no store
        console.error('Erro no login:', error);
    }
};

const getDefaultRoute = () => {
    if (authStore.isAdmin) {
        return '/admin/dashboard';
    } else if (authStore.isManager) {
        return '/manager/dashboard';
    } else {
        return '/professional/dashboard';
    }
};

// Lifecycle
onMounted(() => {
    // Limpa erros ao montar o componente
    authStore.clearError();

    // Foco no campo de email
    const emailInput = document.querySelector('input[type="email"]');
    if (emailInput) {
        emailInput.focus();
    }
});
</script>
