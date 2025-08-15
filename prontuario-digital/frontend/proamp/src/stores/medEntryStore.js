import { defineStore } from 'pinia';
import medEntryService from '../services/api/medEntryService';

export const useMedEntryStore = defineStore('entry', {
    state: () => ({
        entries: [],
        isLoading: false,
        error: null,
    }),

    getters: {
        entryCount: (state) => state.entries.length,
    },

    actions: {
        async fetchAllEntries() {
            this.isLoading = true;
            this.error = null;

            try {
                const data = await medEntryService.getAllEntries();
                this.entries = data;
            } catch (err) {
                this.error = 'Não foi possível carregar as entradas. Tente novamente mais tarde.';
            } finally {
                this.isLoading = false;
            }
        },
    },
});
