// src/stores/userStore.js
import { defineStore } from 'pinia';
import { studentService } from '@/services/api/studentService';

export const useStudentStore = defineStore('student', {
    state: () => ({
        students: [],
        loading: false,
        error: null,
        pagination: {
            currentPage: 1,
            totalPages: 1,
            total: 0,
            from: 0,
            to: 0,
        },
    }),

    getters: {
        getStudentById: (state) => (id) => {
            return state.students.find((student) => student.id === id);
        },
        getStudentsByStatus: (state) => (active) => {
            return state.students.filter((students) => students.active === active);
        },
    },

    actions: {
        async fetchStudents(status) {
            this.loading = true;
            this.error = null;
            var response = null;

            try {
                if (status) {
                    response = await studentService.getStudents();
                } else {
                    response = await studentService.getInactiveStudents();
                }

                // No pagination
                if (Array.isArray(response)) {
                    this.students = response;
                    this.pagination = {
                        currentPage: 1,
                        totalPages: 1,
                        total: response.length,
                        from: 1,
                        to: response.length,
                    };
                } else {
                    // DRF paginations
                    this.students = response.results || response;
                    this.pagination = {
                        currentPage: 1,
                        totalPages: Math.ceil((response.count || response.length) / 10),
                        total: response.count || response.length,
                        from: 1,
                        to: response.results?.length || response.length,
                    };
                }
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao carregar estudantes';
                console.error('Erro ao buscar estudantes:', error);
            } finally {
                this.loading = false;
            }
        },

        async createStudent(userData) {
            this.loading = true;
            this.error = null;

            try {
                const newStudent = await studentService.createStudent(userData);
                this.students.unshift(newStudent);
                return newStudent;
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao criar estudante';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async updateStudent(id, studentData) {
            this.loading = true;
            this.error = null;

            try {
                const updatedStudent = await studentService.updateStudent(id, studentData);
                const index = this.students.findIndex((student) => student.id === id);
                if (index !== -1) {
                    this.students[index] = updatedStudent;
                }
                return updatedStudent;
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao atualizar estudante';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async deleteStudent(id) {
            this.loading = true;
            this.error = null;

            try {
                await studentService.deleteStudent(id);
                this.students = this.students.filter((student) => student.id !== id);
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao desativar estudante';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async restoreStudent(id) {
            this.loading = true;
            this.error = null;

            try {
                await studentService.restoreStudent(id);
            } catch (error) {
                this.error = error.response?.data?.message || 'Erro ao restaurar estudante';
            } finally {
                this.loading = false;
            }
        },

        clearError() {
            this.error = null;
        },
    },
});
