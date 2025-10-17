import api from './baseService';

export const reportService = {
    /**
     * Busca o relatório mensal, opcionalmente com parâmetros de ano e mês.
     * @param {object} params - Objeto contendo { year, month } (opcionais).
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
     * Busca o relatório de um estudante por intervalo, opcionalmente com datas.
     * @param {string} id - ID do estudante.
     * @param {object} params - Objeto contendo { start_date, end_date } (opcionais).
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
