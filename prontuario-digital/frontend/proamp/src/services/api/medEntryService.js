import api from './baseService';

export const medEntryService = {
    // Buscar todas as entradas (com filtro opcional por estudante)
    async getAllEntries(params = {}) {
        try {
            console.log('Parâmetros enviados para a API:', params);
            const response = await api.get('api/medical-entry/', { params });
            console.log('Resposta da API:', response.data);
            return response.data;
        } catch (error) {
            console.error('Erro na requisição de entradas:', error);
            throw error;
        }
    },

    // Medical Esntries of a Student
    async getStudentEntries(studentId) {
        try {
            console.log('Buscando entradas (endpoint /student/) para estudante:', studentId);
            const response = await api.get(`api/medical-entry/student/${studentId}/`);
            return response.data;
        } catch (error) {
            console.error('Erro ao buscar entradas do estudante:', error);
            throw error;
        }
    },

    // Fetch student by query params (alternative)
    async getStudentEntriesWithQuery(studentId) {
        try {
            const params = { student_id: studentId };
            console.log('Buscando entradas para estudante (query):', studentId);
            const response = await api.get('api/medical-entry/', { params });
            return response.data;
        } catch (error) {
            console.error('Erro ao buscar entradas do estudante:', error);
            throw error;
        }
    },

    // Get a entry (full details)
    async getEntryById(entryId) {
        try {
            const response = await api.get(`api/medical-entry/${entryId}/`);
            return response.data;
        } catch (error) {
            console.error('Erro ao buscar entrada específica:', error);
            throw error;
        }
    },

    // Criar nova entrada
    async createEntry(entryData) {
        try {
            console.log('Criando entrada com dados:', entryData);

            // Garantir que student_id está no payload
            if (!entryData.student_id) {
                throw new Error('student_id é obrigatório para criar uma entrada');
            }

            const response = await api.post('api/medical-entry/', entryData);
            return response.data;
        } catch (error) {
            console.error('Erro ao criar entrada:', error);
            throw error;
        }
    },

    // Deletar entrada (soft delete) - apenas profissionais de saúde
    async deleteEntry(entryId, deleteReason) {
        try {
            if (!deleteReason || deleteReason.trim() === '') {
                throw new Error('Razão para exclusão é obrigatória');
            }

            const response = await api.delete(`api/medical-entry/${entryId}/`, {
                data: { delete_reason: deleteReason.trim() },
            });
            return response.data;
        } catch (error) {
            console.error('Erro ao deletar entrada:', error);
            throw error;
        }
    },

    // Buscar entradas com filtros avançados
    async getEntriesWithFilters(filters = {}) {
        try {
            const params = {};

            // Filtro por estudante
            if (filters.studentId) {
                params.student_id = filters.studentId;
            }

            // Outros filtros podem ser adicionados aqui no futuro

            console.log('Buscando entradas com filtros:', params);
            const response = await api.get('api/medical-entry/', { params });
            return response.data;
        } catch (error) {
            console.error('Erro ao buscar entradas com filtros:', error);
            throw error;
        }
    },
};

export default medEntryService;
