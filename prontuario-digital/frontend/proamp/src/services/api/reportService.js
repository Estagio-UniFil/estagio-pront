import api from './baseService';

export const reportService = {
    /**
     * Monthly report, optional month and year.
     * @param {object} params - Object { year, month } (optional).
     */
    async getMonthlyReport(params) {
        const response = await api.get('api/reports/medical-entries/monthly/', {
            responseType: 'blob',
            params: params,
        });
        return response;
    },

    async getReportLog() {
        const response = await api.get('api/reports/report-logs');
        return response;
    },

    /**
     * Student report by interval, dates are optional.
     * @param {string} id - ID do estudante.
     * @param {object} params - Objeto { start_date, end_date } (optional).
     */
    async getStudentReport(id, params) {
        const response = await api.get(`api/reports/medical-entries/interval/${id}/`, {
            responseType: 'blob',
            params: params,
        });
        return response;
    },
};

export default reportService;
