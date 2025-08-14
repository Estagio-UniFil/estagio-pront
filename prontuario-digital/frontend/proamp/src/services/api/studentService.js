import api from './baseService';

export const studentService = {
    async getStudents() {
        const response = await api.get('api/students/');
        return response.data;
    },

    async getStudent(id) {
        const response = await api.get(`api/students/${id}/`);
        return response.data;
    },

    async getInactiveStudents() {
        const response = await api.get(`api/students/inactive/`);
        return response.data;
    },

    async createStudent(userData) {
        const response = await api.post('api/students/', userData);
        return response.data;
    },

    async updateStudent(id, studentData) {
        const response = await api.put(`api/students/${id}/`, studentData);
        return response.data;
    },

    async deleteStudent(id) {
        const response = await api.delete(`api/students/${id}/`);
        return response.data;
    },

    async restoreStudent(id) {
        const response = await api.put(`api/students/inactive/${id}/`);
        return response.data;
    },
};
