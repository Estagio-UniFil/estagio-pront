import { defineStore } from 'pinia';
import reportService from '../services/api/reportService';

export const useReportStore = defineStore('report', {
    state: () => ({
        isLoading: false,
        error: null,
    }),

    actions: {
        async exportMonthlyReport() {
            this.isLoading = true;
            this.error = null;

            try {
                // 1. Aguarde a resposta do service
                const response = await reportService.getMonthlyReport();

                // 2. Extraia o nome do arquivo do cabeçalho 'content-disposition'
                let filename = 'relatorio-mensal.xlsx'; // Nome padrão caso não consiga extrair

                const contentDisposition = response.headers['content-disposition'];
                if (contentDisposition) {
                    // Extrai o nome do arquivo do header content-disposition
                    const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                    if (filenameMatch && filenameMatch[1]) {
                        filename = filenameMatch[1].replace(/['"]/g, '');
                    }
                }

                // 3. Crie um Blob com os dados e o tipo de conteúdo
                const blob = new Blob([response.data], {
                    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                });

                // 4. Crie um link temporário, atribua o Blob e clique nele para baixar
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);

                // Adicione o link ao DOM temporariamente
                document.body.appendChild(link);
                link.click();

                // Limpe o link e a URL do objeto após o download
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            } catch (err) {
                // Melhor tratamento de erro
                if (err.response && err.response.data) {
                    // Se a resposta de erro contém dados JSON
                    try {
                        const errorText = await err.response.data.text();
                        const errorData = JSON.parse(errorText);
                        this.error = errorData.message || 'Erro ao gerar o relatório';
                    } catch {
                        this.error = 'Não foi possível gerar o relatório. Tente novamente mais tarde.';
                    }
                } else {
                    this.error = 'Não foi possível gerar o relatório. Tente novamente mais tarde.';
                }
                console.error('Erro ao gerar relatório:', err);
            } finally {
                this.isLoading = false;
            }
        },
    },
});
