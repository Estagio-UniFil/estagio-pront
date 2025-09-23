import { createRouter, createWebHistory } from 'vue-router';
import TestPage from '../views/Tests/TestPage.vue';
import { requireAuth, requireGuest, requireAdmin, initializeAuth } from './guards';
import LoginView from '@/views/auth/LoginView.vue';
import AdminDashboard from '@/views/admin/AdminDashboard.vue';
import UsersView from '@/views/admin/UsersView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        // Login Routes
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            beforeEnter: requireGuest,
        },
        {
            path: '/',
            name: 'default',
            redirect: '/login',
        },
        {
            path: '/modals',
            name: 'ModalShowcase',
            component: () => import('@/views/Tests/ModalShowcase.vue'),
        },
        // Admin Routes
        {
            path: '/admin',
            redirect: '/admin/dashboard',
            beforeEnter: requireAdmin,
        },
        {
            path: '/admin/dashboard',
            name: 'admin-dashboard',
            component: AdminDashboard,
            beforeEnter: requireAdmin,
        },
        {
            path: '/admin/users',
            name: 'admin-users',
            component: UsersView,
            beforeEnter: requireAdmin,
        },
        // Placeholder routes
        {
            path: '/admin/students',
            name: 'admin-students',
            component: () => import('@/views/common/StudentsView.vue'),
            beforeEnter: requireAdmin,
        },
        {
            path: '/admin/reports',
            name: 'admin-reports',
            component: () => import('@/views/common/MedEntriesView.vue'),
            beforeEnter: requireAdmin,
        },
        {
            path: '/admin/settings',
            name: 'admin-settings',
            component: () => import('@/views/common/SettingsView.vue'),
            beforeEnter: requireAdmin,
        },
        {
            path: '/admin/profile',
            name: 'admin-profile',
            component: () => import('@/views/common/ProfileView.vue'),
            beforeEnter: requireAdmin,
        },
        // Unauthorized route
        {
            path: '/unauthorized',
            name: 'unauthorized',
            component: () => import('@/views/base/UnauthorizedView.vue'),
        },
        // 404 route
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('@/views/base/NotFoundView.vue'),
        },
    ],
});

router.beforeEach(initializeAuth);

export default router;
