<template>
    <form @submit.prevent="handleSubmit">
        <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-x-6 gap-y-4">
                <div>
                    <label for="first_name" class="input-label">Nome</label>
                    <input type="text" id="first_name" v-model="formData.first_name" class="input-field" :class="{ error: errors.first_name }" :disabled="!isEditing" required />
                    <p v-if="errors.first_name" class="input-error">{{ errors.first_name }}</p>
                </div>
                <div class="md:col-span-2">
                    <label for="last_name" class="input-label">Sobrenome</label>
                    <input type="text" id="last_name" v-model="formData.last_name" class="input-field" :class="{ error: errors.last_name }" :disabled="!isEditing" required />
                    <p v-if="errors.last_name" class="input-error">{{ errors.last_name }}</p>
                </div>
                <div class="md:col-span-3">
                    <label for="email" class="input-label">E-mail</label>
                    <input type="email" id="email" v-model="formData.email" class="input-field" :class="{ error: errors.email }" :disabled="!isEditing" required />
                    <p v-if="errors.email" class="input-error">{{ errors.email }}</p>
                </div>
            </div>

            <div v-if="!user.id" class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="password" class="input-label">Senha</label>
                    <input type="password" id="password" v-model="formData.password" class="input-field" :class="{ error: errors.password }" :disabled="!isEditing" required />
                    <p v-if="errors.password" class="input-error">{{ errors.password }}</p>
                </div>
                <div>
                    <label for="password_confirm" class="input-label">Repita a Senha</label>
                    <input type="password" id="password_confirm" v-model="passwordConfirm" class="input-field" :class="{ error: errors.password_confirm }" :disabled="!isEditing" required />
                    <p v-if="errors.password_confirm" class="input-error">{{ errors.password_confirm }}</p>
                </div>
            </div>

            <div>
                <label for="role" class="input-label">Tipo de Usuário</label>
                <select id="role" v-model="formData.role" class="input-field" :class="{ error: errors.role }" :disabled="!isEditing || disableRoleField" required>
                    <option value="" disabled>Selecione um tipo</option>
                    <option value="admin">Administrador</option>
                    <option value="manager">Gestor</option>
                    <option value="health_prof">Profissional da Saúde</option>
                </select>
                <p v-if="errors.role" class="input-error">{{ errors.role }}</p>
            </div>

            <div v-if="formData.role === 'health_prof'">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                    <div>
                        <label for="specialty" class="input-label">Especialidade</label>
                        <select id="specialty" v-model="formData.health_profile.specialty" class="input-field" :class="{ error: errors.specialty }" :disabled="!isEditing" required>
                            <option value="" disabled>Selecione um tipo</option>
                            <option value="psychologist">Psicologia</option>
                            <option value="physiotherapist">Fisioterapia</option>
                            <option value="social_worker">Assistência Social</option>
                            <option value="speech_therapist">Fonoaudiologia</option>
                        </select>
                        <p v-if="errors.specialty" class="input-error">{{ errors.specialty }}</p>
                    </div>
                    <div>
                        <label for="council_number" class="input-label">Número do Conselho</label>
                        <input type="text" id="council_number" v-model="formData.health_profile.council_number" class="input-field" :class="{ error: errors.council_number }" :disabled="!isEditing" required />
                        <p v-if="errors.council_number" class="input-error">{{ errors.council_number }}</p>
                    </div>
                </div>
            </div>

            <div v-if="isEditing" class="flex justify-end space-x-4 pt-6">
                <button v-if="showCancelButton" type="button" @click="emit('cancel')" class="btn-secondary">Cancelar</button>
                <button type="submit" class="btn-primary" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Salvando...' : 'Salvar' }}
                </button>
            </div>
            <div v-if="!isEditing" class="pb-2"></div>
        </div>
    </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useAlertStore } from '@/stores/alertStore';

const alertStore = useAlertStore();

const props = defineProps({
    user: {
        type: Object,
        default: () => ({
            email: '',
            first_name: '',
            last_name: '',
            role: '',
            password: '',
            health_profile: {
                specialty: '',
                council_number: '',
            },
        }),
    },
    isEditing: {
        type: Boolean,
        default: false,
    },
    isSubmitting: {
        type: Boolean,
        default: false,
    },
    disableRoleField: {
        type: Boolean,
        default: false,
    },
    showCancelButton: {
        type: Boolean,
        default: true,
    },
});

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({});
const passwordConfirm = ref('');
const errors = ref({});

// Computed para validações
const isFormValid = computed(() => {
    return Object.keys(errors.value).length === 0 && formData.value.first_name && formData.value.last_name && formData.value.email && formData.value.role;
});

// Função de validação
const validateForm = () => {
    errors.value = {};

    // Validar nome
    if (!formData.value.first_name?.trim()) {
        errors.value.first_name = 'Nome é obrigatório';
    }

    // Validar sobrenome
    if (!formData.value.last_name?.trim()) {
        errors.value.last_name = 'Sobrenome é obrigatório';
    }

    // Validar email
    if (!formData.value.email?.trim()) {
        errors.value.email = 'E-mail é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
        errors.value.email = 'E-mail inválido';
    }

    // Validar role
    if (!formData.value.role) {
        errors.value.role = 'Tipo de usuário é obrigatório';
    }

    // Validar senha (apenas para novos usuários)
    if (!props.user.id) {
        if (!formData.value.password) {
            errors.value.password = 'Senha é obrigatória';
        } else if (formData.value.password.length < 6) {
            errors.value.password = 'Senha deve ter pelo menos 6 caracteres';
        }

        if (!passwordConfirm.value) {
            errors.value.password_confirm = 'Confirmação de senha é obrigatória';
        } else if (formData.value.password !== passwordConfirm.value) {
            errors.value.password_confirm = 'As senhas não coincidem';
        }
    }

    // Validar campos específicos do profissional de saúde
    if (formData.value.role === 'health_prof') {
        if (!formData.value.health_profile?.specialty) {
            errors.value.specialty = 'Especialidade é obrigatória';
        }
        if (!formData.value.health_profile?.council_number?.trim()) {
            errors.value.council_number = 'Número do conselho é obrigatório';
        }
    }

    return Object.keys(errors.value).length === 0;
};

// Limpar erros quando o usuário começar a digitar
watch(
    () => formData.value.first_name,
    () => {
        if (errors.value.first_name) delete errors.value.first_name;
    },
);

watch(
    () => formData.value.last_name,
    () => {
        if (errors.value.last_name) delete errors.value.last_name;
    },
);

watch(
    () => formData.value.email,
    () => {
        if (errors.value.email) delete errors.value.email;
    },
);

watch(
    () => formData.value.role,
    () => {
        if (errors.value.role) delete errors.value.role;
    },
);

watch(
    () => formData.value.password,
    () => {
        if (errors.value.password) delete errors.value.password;
    },
);

watch(
    () => passwordConfirm.value,
    () => {
        if (errors.value.password_confirm) delete errors.value.password_confirm;
    },
);

watch(
    () => formData.value.health_profile?.specialty,
    () => {
        if (errors.value.specialty) delete errors.value.specialty;
    },
);

watch(
    () => formData.value.health_profile?.council_number,
    () => {
        if (errors.value.council_number) delete errors.value.council_number;
    },
);

watch(
    () => props.user,
    (newUserData) => {
        formData.value = JSON.parse(JSON.stringify(newUserData));

        if (formData.value.role === 'health_prof' && !formData.value.health_profile) {
            formData.value.health_profile = { specialty: '', council_number: '' };
        }

        // Limpar erros quando os dados mudarem
        errors.value = {};
        passwordConfirm.value = '';
    },
    { immediate: true, deep: true },
);

watch(
    () => formData.value.role,
    (newRole) => {
        if (newRole !== 'health_prof') {
            delete formData.value.health_profile;
        } else if (!formData.value.health_profile) {
            formData.value.health_profile = { specialty: '', council_number: '' };
        }
    },
);

const handleSubmit = () => {
    // Validar formulário
    if (!validateForm()) {
        return;
    }

    if (!props.user.id && formData.value.password !== passwordConfirm.value) {
        alertStore.triggerAlert({ message: 'As senhas não coincidem!', type: 'error', title: 'Erro' });
        return;
    }

    const payload = { ...formData.value };

    if (payload.role !== 'health_prof') {
        delete payload.health_profile;
    }
    if (!payload.password) {
        delete payload.password;
    }

    emit('submit', payload);
};
</script>
