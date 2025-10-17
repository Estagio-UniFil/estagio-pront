import { useAuthStore } from '@/stores/authStore';

export const requireAuth = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({
            name: 'login',
            query: { redirect: to.fullPath },
        });
    } else {
        next();
    }
};

// Guard para rotas que só admin pode acessar
export const requireAdmin = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else if (!authStore.isAdmin) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para rotas que admin OU manager podem acessar
export const requireAdminOrManager = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else if (!authStore.isAdmin && !authStore.isManager) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para rotas que só usuários NÃO autenticados podem acessar (login)
export const requireGuest = (to, from, next) => {
    const authStore = useAuthStore();

    if (authStore.isAuthenticated) {
        if (authStore.isAdmin) {
            next({ name: 'admin-dashboard' });
        } else if (authStore.isManager) {
            next({ name: 'manager-dashboard' });
        } else if (authStore.isProfessional) {
            next({ name: 'health-dashboard' });
        } else {
            next({ name: 'unauthorized' });
        }
    } else {
        next();
    }
};

// Guard global para inicializar autenticação
export const initializeAuth = (to, from, next) => {
    const authStore = useAuthStore();

    // Inicializa dados do localStorage na primeira navegação
    authStore.initializeAuth();

    next();
};

export const requireManager = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else if (!authStore.isManager) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

export const requireHealthProfessional = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else if (!authStore.isProfessional) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};
