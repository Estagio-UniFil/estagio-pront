<template>
    <BaseModal :show="show" @close="handleClose" title="Gerar Relatório Parametrizado">
        <ReportParamsForm :params="formData" :students="studentList" @update="handleFormUpdate" />

        <template #footer>
            <button @click="handleClose" class="btn btn-secondary">Cancelar</button>

            <button @click="submitGenerate" class="btn btn-primary" :disabled="isLoading || !isFormValid">
                {{ isLoading ? 'Gerando...' : 'Gerar e Baixar' }}
            </button>
        </template>
    </BaseModal>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import ReportParamsForm from '@/components/forms/professional/ReportParamsForm.vue';
import { useAlertStore } from '@/stores/alertStore';
import { useStudentStore } from '@/stores/studentStore';
import { useReportStore } from '@/stores/reportStore';

const props = defineProps({
    show: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(['close']);

const alertStore = useAlertStore();
const studentStore = useStudentStore();
const reportStore = useReportStore();

const studentList = ref([]);
const formData = ref(getInitialFormData());

const isLoading = computed(() => reportStore.isLoading);

function getInitialFormData() {
    return {
        reportType: 'general_monthly',
        year: null,
        month: null,
        studentId: null,
        startDate: '',
        endDate: '',
    };
}

watch(
    () => props.show,
    async (newValue) => {
        if (newValue) {
            await loadStudents();
        }
    },
    { immediate: true },
);

const loadStudents = async () => {
    if (studentStore.students.length === 0) {
        try {
            await studentStore.fetchStudents('active');
            studentList.value = studentStore.students;
        } catch (error) {
            console.error('Erro ao carregar estudantes:', error);
            alertStore.triggerAlert({ message: 'Erro ao carregar lista de estudantes.', type: 'error' });
        }
    } else {
        studentList.value = studentStore.students;
    }
};

const handleClose = () => {
    // Só permite fechar se não estiver carregando
    if (!isLoading.value) {
        formData.value = getInitialFormData();
        emit('close');
    }
};

const isFormValid = computed(() => {
    if (formData.value.reportType === 'student_interval') {
        return !!formData.value.studentId;
    }
    return true;
});

// 4. Lógica de submit atualizada
const submitGenerate = async () => {
    if (!isFormValid.value) {
        alertStore.triggerAlert('Preencha os campos obrigatórios.', 'warning');
        return;
    }

    let success = false;
    const params = formData.value;

    if (params.reportType === 'general_monthly') {
        success = await reportStore.exportMonthlyReport({
            year: params.year,
            month: params.month,
        });
    } else if (params.reportType === 'student_interval') {
        success = await reportStore.exportStudentReport({
            id: params.studentId,
            startDate: params.startDate,
            endDate: params.endDate,
        });
    }
    if (success) {
        handleClose();
    }
};

const handleFormUpdate = ({ key, value }) => {
    // 1. Atualiza o valor que mudou
    formData.value[key] = value;

    // 2. APLICA A LÓGICA DE RESET AQUI (no pai)
    // Se a mudança foi no 'reportType', resetamos os outros campos.
    if (key === 'reportType') {
        formData.value.year = null;
        formData.value.month = null;
        formData.value.studentId = null;
        formData.value.startDate = '';
        formData.value.endDate = '';
    }
};
</script>
