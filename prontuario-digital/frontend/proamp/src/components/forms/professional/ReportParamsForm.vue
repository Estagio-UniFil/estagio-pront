<template>
    <div class="form-container">
        <div class="form-group">
            <label for="report-type" class="input-label">Tipo de Relatório*</label>
            <select id="report-type" class="input-field bg-tertiary" :value="params.reportType" @change="emitUpdate('reportType', $event.target.value)">
                <option value="general_monthly">Relatório Mensal Geral</option>
                <option value="student_interval">Relatório de Aluno</option>
            </select>
        </div>

        <template v-if="params.reportType === 'general_monthly'">
            <p class="text-sm text-gray-600 -mt-2 mb-2">Deixe os campos em branco para gerar o relatório do mês atual.</p>
            <div class="grid grid-cols-2 gap-4">
                <div class="form-group">
                    <label for="report-year" class="input-label">Ano (Opcional)</label>
                    <input id="report-year" type="number" class="input-field bg-tertiary" placeholder="Ex: 2024" :value="params.year" @input="emitUpdate('year', $event.target.value)" />
                </div>
                <div class="form-group">
                    <label for="report-month" class="input-label">Mês (Opcional)</label>
                    <input id="report-month" type="number" class="input-field bg-tertiary" placeholder="Ex: 10" min="1" max="12" :value="params.month" @input="emitUpdate('month', $event.target.value)" />
                </div>
            </div>
        </template>

        <template v-if="params.reportType === 'student_interval'">
            <div class="form-group">
                <label for="student-select" class="input-label">Selecionar Estudante*</label>
                <select id="student-select" class="input-field bg-tertiary" required :value="params.studentId" @change="emitUpdate('studentId', $event.target.value)">
                    <option :value="null" disabled>Selecione um estudante</option>
                    <option v-for="student in students" :key="student.id" :value="student.id">{{ student.name }} - CGM: {{ student.cgm }}</option>
                </select>
            </div>

            <p class="text-sm text-gray-600 -mt-2 mb-2">Deixe as datas em branco para gerar o relatório do mês atual.</p>
            <div class="grid grid-cols-2 gap-4">
                <div class="form-group">
                    <label for="report-start-date" class="input-label">Data de Início (Opcional)</label>
                    <input id="report-start-date" type="date" class="input-field bg-tertiary" :value="params.startDate" @input="emitUpdate('startDate', $event.target.value)" />
                </div>
                <div class="form-group">
                    <label for="report-end-date" class="input-label">Data de Fim (Opcional)</label>
                    <input id="report-end-date" type="date" class="input-field bg-tertiary" :value="params.endDate" @input="emitUpdate('endDate', $event.target.value)" />
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    params: {
        type: Object,
        required: true,
    },
    students: {
        type: Array,
        default: () => [],
    },
});

const emit = defineEmits(['update']);

const emitUpdate = (key, value) => {
    emit('update', { key, value });
};
</script>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.form-group {
    display: flex;
    flex-direction: column;
}
.form-group label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}
</style>
