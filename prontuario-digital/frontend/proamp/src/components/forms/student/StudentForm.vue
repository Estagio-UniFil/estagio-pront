<template>
    <form @submit.prevent="handleSubmit">
        <div class="space-y-4 pb-2">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="name" class="input-label">Nome Completo{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="name" v-model="formData.name" :disabled="!isEditing" @input="formData.name = formatAsTextOnly($event.target.value)" required />
                    <div v-if="validationErrors.name" class="text-red-600 text-sm mt-1">
                        <p v-for="(error, index) in validationErrors.name" :key="index">
                            {{ error }}
                        </p>
                    </div>
                </div>
                <div>
                    <label for="cgm" class="input-label">CGM{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="cgm" v-model="formData.cgm" :disabled="!isEditing" required />
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="dob" class="input-label">Data de Nascimento{{ isEditing ? '*' : '' }}</label>
                    <input type="date" class="input-field bg-tertiary" id="dob" v-model="formData.dob" :disabled="!isEditing" :max="maxDate" required />
                    <div v-if="localFormErrors.dob" class="text-red-600 text-sm mt-1">
                        {{ localFormErrors.dob }}
                    </div>
                    <div v-if="validationErrors.dob" class="text-red-600 text-sm mt-1">
                        <p v-for="(error, index) in validationErrors.dob" :key="index">
                            {{ error }}
                        </p>
                    </div>
                </div>
                <div>
                    <label for="gender" class="input-label">Gênero{{ isEditing ? '*' : '' }}</label>
                    <select id="gender" class="input-field bg-tertiary" v-model="formData.gender" :disabled="!isEditing" required>
                        <option value="M">Masculino</option>
                        <option value="F">Feminino</option>
                        <option value="O">Outro</option>
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div>
                    <label for="guardian" class="input-label">Nome do Responsável{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="guardian" v-model="formData.guardian" :disabled="!isEditing" @input="formData.guardian = formatAsTextOnly($event.target.value)" required />
                    <div v-if="validationErrors.guardian" class="text-red-600 text-sm mt-1">
                        <p v-for="(error, index) in validationErrors.guardian" :key="index">
                            {{ error }}
                        </p>
                    </div>
                </div>
                <div>
                    <label for="guardian_cpf" class="input-label">CPF do Responsável{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="guardian_cpf" v-model="formData.guardian_cpf" placeholder="000.000.000-00" maxlength="14" :disabled="!isEditing" required />
                    <div v-if="validationErrors.guardian_cpf" class="text-red-600 text-sm mt-1">
                        <p v-for="(error, index) in validationErrors.guardian_cpf" :key="index">
                            {{ error }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-1 gap-x-6 gap-y-4">
                <div>
                    <label for="address" class="input-label">Endereço{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="address" v-model="formData.address" :disabled="!isEditing" required />
                </div>
            </div>

            <div class="grid grid-cols-3 md:grid-cols-3 gap-x-6 gap-y-4">
                <div>
                    <label for="cep" class="input-label">CEP{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="cep" v-model="formData.cep" maxlength="9" placeholder="00000-000" :disabled="!isEditing" required />
                </div>
                <div>
                    <label for="city" class="input-label">Cidade{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="city" v-model="formData.city" :disabled="!isEditing" required />
                </div>
                <div>
                    <label for="state" class="input-label">Estado{{ isEditing ? '*' : '' }}</label>
                    <input type="text" class="input-field bg-tertiary" id="state" v-model="formData.state" :disabled="!isEditing" required maxlength="2" />
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
import { ref, watch, computed } from 'vue';

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
    validationErrors: {
        type: Object,
        default: () => ({}),
    },
});

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({ ...props.student });
const maxDate = computed(() => new Date().toISOString().split('T')[0]);
const localFormErrors = ref({});

const formatAsTextOnly = (value) => {
    if (!value) return '';
    return value.replace(/[\d]/g, '');
};

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
