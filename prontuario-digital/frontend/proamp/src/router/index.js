// index.js
import { createRouter, createWebHistory } from 'vue-router';
import { requireGuest, requireAdmin, requireManager, requireHealthProfessional, initializeAuth } from './guards';

// Views
import LoginView from '@/views/auth/LoginView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        // Auth Routes
        {
            path: '/',
            redirect: '/login',
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            beforeEnter: requireGuest,
        },

        // Admin Routes - AdminLayout
        {
            path: '/admin',
            component: () => import('@/components/layouts/AdminLayout.vue'),
            beforeEnter: requireAdmin,
            children: [
                {
                    path: '',
                    redirect: 'dashboard',
                },
                {
                    path: 'dashboard',
                    name: 'admin-dashboard',
                    component: () => import('@/views/admin/AdminDashboard.vue'),
                },
                {
                    path: 'users',
                    name: 'admin-users',
                    component: () => import('@/views/admin/UsersView.vue'),
                },
                {
                    path: 'students',
                    name: 'admin-students',
                    component: () => import('@/views/admin/StudentsView.vue'),
                },
                {
                    path: 'reports',
                    name: 'admin-reports',
                    component: () => import('@/views/common/ReportsView.vue'),
                },
                {
                    path: 'profile',
                    name: 'admin-profile',
                    component: () => import('@/views/common/ProfileView.vue'),
                },
            ],
        },

        // Manager Routes - ManagerLayout
        {
            path: '/manager',
            component: () => import('@/components/layouts/ManagerLayout.vue'),
            beforeEnter: requireManager,
            children: [
                {
                    path: '',
                    redirect: 'dashboard',
                },
                {
                    path: 'dashboard',
                    name: 'manager-dashboard',
                    component: () => import('@/views/manager/ManagerDashboardView.vue'),
                },
                {
                    path: 'team',
                    name: 'manager-team',
                    component: () => import('@/views/manager/TeamListView.vue'),
                },
                {
                    path: 'reports',
                    name: 'manager-reports',
                    component: () => import('@/views/common/ReportsView.vue'),
                },
                {
                    path: 'profile',
                    name: 'manager-profile',
                    component: () => import('@/views/common/ProfileView.vue'),
                },
            ],
        },

        // Health Professional Routes - HealthProfessionalLayout
        {
            path: '/professional',
            component: () => import('@/components/layouts/HealthProfessionalLayout.vue'),
            beforeEnter: requireHealthProfessional,
            children: [
                {
                    path: '',
                    redirect: 'dashboard',
                },
                {
                    path: 'dashboard',
                    name: 'health-dashboard',
                    component: () => import('@/views/professional/HealthProfessionalDashboard.vue'),
                },
                {
                    path: 'students',
                    name: 'health-students',
                    component: () => import('@/views/professional/StudentsHealthProView.vue'),
                },
                {
                    path: 'records',
                    name: 'health-records',
                    component: () => import('@/views/professional/MedEntriesView.vue'),
                },
                {
                    path: 'reports',
                    name: 'health-reports',
                    component: () => import('@/views/common/ReportsView.vue'),
                },
                {
                    path: 'profile',
                    name: 'health-professional-profile',
                    component: () => import('@/views/common/ProfileView.vue'),
                },
            ],
        },

        // Utility Routes
        {
            path: '/unauthorized',
            name: 'unauthorized',
            component: () => import('@/views/base/UnauthorizedView.vue'),
        },
        {
            path: '/modals',
            name: 'ModalShowcase',
            component: () => import('@/views/Tests/ModalShowcase.vue'),
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('@/views/base/NotFoundView.vue'),
        },
    ],
});

router.beforeEach(initializeAuth);

export default router;
