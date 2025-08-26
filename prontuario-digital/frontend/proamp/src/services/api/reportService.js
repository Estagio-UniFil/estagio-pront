import api from './baseService';

export const reportService = {
    async getMonthlyReport() {
        const response = await api.get('api/reports/medical-entries/monthly/', {
            responseType: 'blob',
        });
        return response;
    },
};

export default reportService;
