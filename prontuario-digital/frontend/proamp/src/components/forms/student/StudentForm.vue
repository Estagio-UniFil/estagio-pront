<template>
    <form @submit.prevent="handleSubmit">
        <div class="space-y-4 pb-2">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="name" class="input-label">Nome Completo*</label>
                    <input type="text" class="input-field" id="name" v-model="formData.name" :disabled="!isEditing" required />
                </div>
                <div>
                    <label for="cgm" class="input-label">CGM*</label>
                    <input type="text" class="input-field" id="cgm" v-model="formData.cgm" :disabled="!isEditing" required />
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="dob" class="input-label">Data de Nascimento*</label>
                    <input type="date" class="input-field" id="dob" v-model="formData.dob" :disabled="!isEditing" required />
                </div>
                <div>
                    <label for="gender" class="input-label">Gênero*</label>
                    <select id="gender" class="input-field" v-model="formData.gender" :disabled="!isEditing" required>
                        <option value="M">Masculino</option>
                        <option value="F">Feminino</option>
                        <option value="O">Outro</option>
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="guardian" class="input-label">Nome do Responsável*</label>
                    <input type="text" class="input-field" id="guardian" v-model="formData.guardian" :disabled="!isEditing" required />
                </div>
                <div>
                    <label for="guardian_cpf" class="input-label">CPF do Responsável*</label>
                    <input type="text" class="input-field" id="guardian_cpf" v-model="formData.guardian_cpf" placeholder="000.000.000-00" maxlength="14" :disabled="!isEditing" required />
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-1 gap-x-6 gap-y-4">
                <div>
                    <label for="address" class="input-label">Endereço*</label>
                    <input type="text" class="input-field" id="address" v-model="formData.address" required />
                </div>
            </div>

            <div class="grid grid-cols-3 md:grid-cols-3 gap-x-6 gap-y-4">
                <div>
                    <label for="cep" class="input-label">CEP*</label>
                    <input type="text" class="input-field" id="cep" v-model="formData.cep" maxlength="9" placeholder="00000-000" required />
                </div>
                <div>
                    <label for="city" class="input-label">Cidade*</label>
                    <input type="text" class="input-field" id="city" v-model="formData.city" required />
                </div>
                <div>
                    <label for="state" class="input-label">Estado*</label>
                    <input type="text" class="input-field" id="state" v-model="formData.state" required maxlength="2" />
                </div>
            </div>

            <div v-if="isEditing" class="flex justify-end space-x-4 pt-6">
                <button type="button" @click="emit('cancel')" class="btn-secondary">Cancelar</button>
                <button type="submit" class="btn-primary" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Salvando...' : 'Salvar' }}
                </button>
            </div>
            <div v-if="!isEditing" class="pb-2"></div>
        </div>
    </form>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
    student: {
        type: Object,
        default: () => ({
            name: '',
            cgm: '',
            dob: '',
            gender: '',
            guardian: '',
            guardian_cpf: '',
            address: '',
            cep: '',
            city: '',
            state: '',
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
});

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({ ...props.student });

watch(
    () => props.student,
    (newStudentData) => {
        formData.value = { ...newStudentData };
        formData.value.guardian_cpf = formatCpf(formData.value.guardian_cpf);
        formData.value.cep = formatCep(formData.value.cep);
    },
    { immediate: true, deep: true },
);

const handleSubmit = () => {
    const unformatValue = (value) => (value && typeof value === 'string' ? value.replace(/\D/g, '') : value);

    const payload = { ...formData.value };
    payload.guardian_cpf = unformatValue(payload.guardian_cpf);
    payload.cep = unformatValue(payload.cep);

    emit('submit', payload);
};

function formatCep(value) {
    if (!value) return '';
    const digitsOnly = value.replace(/\D/g, '');
    const truncatedValue = digitsOnly.slice(0, 8);

    if (truncatedValue.length > 5) {
        return `${truncatedValue.slice(0, 5)}-${truncatedValue.slice(5)}`;
    }
    return truncatedValue;
}
function formatCpf(value) {
    if (!value) return '';
    const digitsOnly = value.replace(/\D/g, '');
    const truncatedValue = digitsOnly.slice(0, 11);
    let formattedValue = truncatedValue;
    if (truncatedValue.length > 3) {
        formattedValue = `${truncatedValue.slice(0, 3)}.${truncatedValue.slice(3)}`;
    }
    if (truncatedValue.length > 6) {
        formattedValue = `${formattedValue.slice(0, 7)}.${formattedValue.slice(7)}`;
    }
    if (truncatedValue.length > 9) {
        formattedValue = `${formattedValue.slice(0, 11)}-${formattedValue.slice(11)}`;
    }
    return formattedValue;
}

watch(
    () => formData.value.guardian_cpf,
    (newValue) => {
        formData.value.guardian_cpf = formatCpf(newValue);
    },
);
watch(
    () => formData.value.cep,
    (newValue) => {
        formData.value.cep = formatCep(newValue);
    },
);
</script>
