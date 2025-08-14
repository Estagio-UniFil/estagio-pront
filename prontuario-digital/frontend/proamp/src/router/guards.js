import { useAuthStore } from '@/stores/authStore';

export const requireAuth = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        // Redireciona para login se não estiver autenticado
        next({
            name: 'login',
            query: { redirect: to.fullPath }, // Salva para onde estava indo
        });
    } else {
        next(); // Permite acesso
    }
};

// Guard para rotas que só admin pode acessar
export const requireAdmin = (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else if (!authStore.isAdmin) {
        // Redireciona para página não autorizada
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
        // Se já está logado, redireciona para dashboard baseado no role
        if (authStore.isAdmin) {
            next({ name: 'admin-dashboard' });
        } else if (authStore.isManager) {
            next({ name: 'manager-dashboard' });
        } else {
            next({ name: 'professional-dashboard' });
        }
    } else {
        next(); // Permite acesso ao login
    }
};

// Guard global para inicializar autenticação
export const initializeAuth = (to, from, next) => {
    const authStore = useAuthStore();

    // Inicializa dados do localStorage na primeira navegação
    authStore.initializeAuth();

    next();
};
