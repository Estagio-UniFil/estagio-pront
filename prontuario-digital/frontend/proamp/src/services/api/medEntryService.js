import api from './baseService';

export const medEntryService = {
    async getAllEntries() {
        const response = await api.get('api/medical-entry/');
        return response.data;
    },

    async createEntry() {
        const response = await api.post('api/medical-entry/');
        return response.data;
    },
};

export default medEntryService;
