import { defineStore } from 'pinia';
import medEntryService from '../services/api/medEntryService';

export const useMedEntryStore = defineStore('medEntry', {
    state: () => ({
        entries: [],
        currentEntry: null,
        studentEntries: null,
        isLoading: false,
        isCreating: false,
        isDeleting: false,
        error: null,
        lastFetchedStudentId: null,
    }),

    getters: {
        entryCount: (state) => state.entries.length,

        hasEntries: (state) => state.entries.length > 0,

        entriesByDate: (state) => {
            return [...state.entries].sort((a, b) => {
                return new Date(b.entry_date) - new Date(a.entry_date);
            });
        },

        hasStudentEntries: (state) => {
            return state.studentEntries && state.studentEntries.entries && state.studentEntries.entries.length > 0;
        },

        currentStudentEntries: (state) => {
            return state.studentEntries?.entries || [];
        },

        currentStudentInfo: (state) => {
            if (!state.studentEntries) return null;
            return {
                id: state.studentEntries.student_id,
                name: state.studentEntries.student_name,
                entryCount: state.studentEntries.entries?.length || 0,
            };
        },

        isAnyLoading: (state) => state.isLoading || state.isCreating || state.isDeleting,
    },

    actions: {
        clearEntries() {
            this.entries = [];
            this.error = null;
        },

        clearStudentEntries() {
            this.studentEntries = null;
            this.lastFetchedStudentId = null;
            this.error = null;
        },

        clearCurrentEntry() {
            this.currentEntry = null;
            this.error = null;
        },

        async fetchAllEntries() {
            this.isLoading = true;
            this.error = null;

            try {
                const data = await medEntryService.getAllEntries();
                this.entries = Array.isArray(data) ? data : [];
                console.log('Todas as entradas carregadas:', this.entries.length);
            } catch (error) {
                console.error('Erro ao buscar entradas:', error);
                this.error = this._extractErrorMessage(error);
                this.entries = [];
            } finally {
                this.isLoading = false;
            }
        },

        async fetchStudentEntries(studentId) {
            if (!studentId) {
                console.error('ID do estudante é obrigatório');
                this.error = 'ID do estudante não fornecido';
                return;
            }

            this.isLoading = true;
            this.error = null;

            try {
                console.log('Buscando entradas para o estudante ID:', studentId);
                const data = await medEntryService.getStudentEntries(studentId);

                this.studentEntries = data;
                this.entries = data.entries || [];
                console.log('Entradas do estudante carregadas:', this.entries.length);
            } catch (error) {
                console.error('Erro ao buscar entradas do estudante:', error);
                this.error = this._extractErrorMessage(error);
                this.entries = [];
            } finally {
                this.isLoading = false;
            }
        },

        async fetchEntriesWithFilters(filters = {}) {
            this.isLoading = true;
            this.error = null;

            try {
                console.log('Buscando entradas com filtros:', filters);
                const data = await medEntryService.getEntriesWithFilters(filters);
                this.entries = Array.isArray(data) ? data : [];
                console.log('Entradas filtradas carregadas:', this.entries.length);
            } catch (error) {
                console.error('Erro ao buscar entradas com filtros:', error);
                this.error = this._extractErrorMessage(error);
                this.entries = [];
            } finally {
                this.isLoading = false;
            }
        },

        async fetchEntryById(entryId) {
            if (!entryId) {
                console.error('ID da entrada é obrigatório');
                this.error = 'ID da entrada não fornecido';
                return;
            }

            this.isLoading = true;
            this.error = null;

            try {
                console.log('Buscando entrada ID:', entryId);
                const data = await medEntryService.getEntryById(entryId);
                this.currentEntry = data;
                console.log('Entrada carregada:', data);
                return data;
            } catch (error) {
                console.error('Erro ao buscar entrada específica:', error);
                this.error = this._extractErrorMessage(error);
                this.currentEntry = null;
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        async createEntry(entryData) {
            if (!entryData.student_id) {
                this.error = 'ID do estudante é obrigatório';
                throw new Error(this.error);
            }

            this.isCreating = true;
            this.error = null;

            try {
                console.log('Criando entrada:', entryData);
                const data = await medEntryService.createEntry(entryData);

                if (this.entries.length > 0) {
                    this.entries.unshift(data);
                }

                if (this.studentEntries && this.studentEntries.student_id == entryData.student_id) {
                    this.studentEntries.entries.unshift(data);
                }

                console.log('Entrada criada com sucesso:', data);
                return data;
            } catch (error) {
                console.error('Erro ao criar entrada:', error);
                this.error = this._extractErrorMessage(error);
                throw error;
            } finally {
                this.isCreating = false;
            }
        },

        async deleteEntry(entryId, deleteReason) {
            if (!entryId) {
                this.error = 'ID da entrada é obrigatório';
                throw new Error(this.error);
            }

            if (!deleteReason || deleteReason.trim() === '') {
                this.error = 'Razão para exclusão é obrigatória';
                throw new Error(this.error);
            }

            this.isDeleting = true;
            this.error = null;

            try {
                console.log('Deletando entrada ID:', entryId);
                await medEntryService.deleteEntry(entryId, deleteReason);

                this.entries = this.entries.filter((entry) => entry.id !== entryId);

                if (this.studentEntries && this.studentEntries.entries) {
                    this.studentEntries.entries = this.studentEntries.entries.filter((entry) => entry.id !== entryId);
                }

                if (this.currentEntry && this.currentEntry.id === entryId) {
                    this.currentEntry = null;
                }

                console.log('Entrada deletada com sucesso');
                return true;
            } catch (error) {
                console.error('Erro ao deletar entrada:', error);
                this.error = this._extractErrorMessage(error);
                throw error;
            } finally {
                this.isDeleting = false;
            }
        },

        async refreshStudentEntries() {
            if (this.lastFetchedStudentId) {
                await this.fetchStudentEntries(this.lastFetchedStudentId);
            }
        },

        _extractErrorMessage(error) {
            return error.response?.data?.detail || error.response?.data?.message || error.message || 'Ocorreu um erro inesperado. Tente novamente mais tarde.';
        },
    },
});

export default useMedEntryStore;
