import api from './baseService';

export const reportService = {
    async getMonthlyReport() {
        const response = await api.get('api/reports/medical-entries/monthly/', {
            responseType: 'blob',
        });
        return response;
    },

    async getReportLog() {
        const response = await api.get('api/reports/report-logs');
        return response;
    },
};

export default reportService;
