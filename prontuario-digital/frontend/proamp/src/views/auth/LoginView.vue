<template>
    <AuthLayout>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css" integrity="sha512-DxV+EoADOkOygM4IR9yXP8Sb2qwgidEmeqAEmDKIOfPRQZOWbXCzLC6vjbZyy0vPisbH2SyW27+ddLVCN+OMzQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />

        <div class="card max-w-md mx-auto">
            <!-- Error message -->
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

                <!-- Password -->
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

                <!-- Remember me -->
                <div class="flex items-center justify-between">
                    <div class="relative flex items-center">
                        <input v-model="form.rememberMe" type="checkbox" id="remember" class="mr-2" :disabled="authStore.isLoading" />
                        <label for="remember" class="text-sm text-muted select-none cursor-pointer"> Lembrar de mim </label>
                    </div>

                    <div>
                        <ThemeToggle />
                    </div>
                </div>

                <!-- Login -->
                <button type="submit" class="btn-primary w-full flex items-center justify-center" :disabled="authStore.isLoading || !isFormValid">
                    <div v-if="authStore.isLoading" class="loading-spinner w-4 h-4 mr-2"></div>
                    {{ authStore.isLoading ? 'Entrando...' : 'Entrar' }}
                </button>
            </form>

            <!-- Links -->
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
import ThemeToggle from '@/components/common/ThemeToggle.vue';

const router = useRouter();
const authStore = useAuthStore();

// Form state
const form = ref({
    email: '',
    password: '',
    rememberMe: false,
});

// UI state
const showPassword = ref(false);
const errors = ref({});

// Computed
const isFormValid = computed(() => {
    return form.value.email && form.value.password && !authStore.isLoading;
});

// Methods
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
    authStore.clearError();
    errors.value = {};

    if (!validateForm()) {
        return;
    }

    try {
        // Login - remember me
        const userData = await authStore.login(form.value.email, form.value.password, form.value.rememberMe);

        if (userData.must_change_password) {
            router.push('/force-password-change');
        }

        // Redirect by role
        switch (userData.role) {
            case 'admin':
                router.push('/admin/dashboard');
                break;
            case 'manager':
                router.push('/manager/dashboard');
                break;
            case 'health_prof':
                router.push('/professional/dashboard');
                break;
            default:
                router.push('/');
        }
    } catch (error) {
        console.error('Erro no login:', error);

        if (error.response?.data?.errors) {
            errors.value = error.response.data.errors;
        }
    }
};

// Lifecycle
onMounted(() => {
    authStore.clearError();

    // Authenticated redirect
    if (authStore.isAuthenticated) {
        const role = authStore.userRole;
        if (role === 'admin') {
            router.push('/admin/dashboard');
        } else if (role === 'manager') {
            router.push('/manager/dashboard');
        } else if (role === 'health_prof') {
            router.push('/professional/dashboard');
        }
    }

    setTimeout(() => {
        const emailInput = document.querySelector('input[type="email"]');
        if (emailInput) {
            emailInput.focus();
        }
    }, 100);
});
</script>

<style scoped>
.loading-spinner {
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3498db;
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

.input-field:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
}
</style>
