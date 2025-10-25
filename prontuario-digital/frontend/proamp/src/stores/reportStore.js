import { defineStore } from 'pinia';
import reportService from '../services/api/reportService';
import { useAlertStore } from './alertStore';

export const useReportStore = defineStore('report', {
    state: () => ({
        isLoading: false,
        error: null,
        logEntries: [],
    }),

    actions: {
        /**
         * Blob logic for download.
         * @private
         */
        _handleBlobDownload(response) {
            let filename = 'relatorio.xlsx';

            const contentDisposition = response.headers['content-disposition'];

            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                console.log(filenameMatch);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }

            const blob = new Blob([response.data], {
                type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            });

            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        },

        /**
         * Logic for error handle.
         * @private
         */
        async _handleApiError(err, alertStore) {
            if (err.response && err.response.data) {
                try {
                    const errorText = await err.response.data.text();
                    const errorData = JSON.parse(errorText);
                    this.error = errorData.detail || 'Erro ao gerar o relatório';
                } catch {
                    this.error = 'Não foi possível gerar o relatório. Tente novamente mais tarde.';
                }
            } else {
                this.error = 'Não foi possível gerar o relatório. Tente novamente mais tarde.';
            }
            console.error('Erro ao gerar relatório:', err);
            alertStore.triggerAlert(this.error, 'error');
        },

        /**
         * Export monthly report.
         * @returns {boolean}
         */
        async exportMonthlyReport(params) {
            this.isLoading = true;
            this.error = null;
            const alertStore = useAlertStore();

            try {
                const cleanParams = {
                    year: params.year || undefined,
                    month: params.month || undefined,
                };

                const response = await reportService.getMonthlyReport(cleanParams);
                this._handleBlobDownload(response);
                alertStore.triggerAlert('Relatório gerado com sucesso!', 'success');
                return true;
            } catch (err) {
                await this._handleApiError(err, alertStore);
                return false;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Export student interval report.
         * @returns {boolean}
         */
        async exportStudentReport(data) {
            this.isLoading = true;
            this.error = null;
            const alertStore = useAlertStore();

            try {
                const cleanParams = {
                    start_date: data.startDate || undefined,
                    end_date: data.endDate || undefined,
                };

                const response = await reportService.getStudentReport(data.id, cleanParams);
                this._handleBlobDownload(response);
                alertStore.triggerAlert('Relatório gerado com sucesso!', 'success');
                return true;
            } catch (err) {
                await this._handleApiError(err, alertStore);
                return false;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Report Log.
         */
        async fetchAllLogEntries() {
            this.isLoading = true;
            this.error = null;
            this.logEntries = [];
            const alertStore = useAlertStore();

            try {
                const response = await reportService.getReportLog();
                this.logEntries = Array.isArray(response.data) ? response.data : [];
            } catch (error) {
                console.error('Erro ao buscar entradas de log:', error);
                this.error = 'Erro ao buscar histórico de relatórios.';
                alertStore.triggerAlert(this.error, 'error');
                this.logEntries = [];
            } finally {
                this.isLoading = false;
            }
        },
    },
});
