import { useAuthStore } from '@/stores/authStore';
import { authService } from '@/services/api/authService';

// Guard genérico para rotas autenticadas
export const requireAuth = async (to, from, next) => {
    const authStore = useAuthStore();

    // Se não tem dados de usuário no store
    if (!authStore.isAuthenticated) {
        // Tenta verificar com o backend se existe sessão ativa
        const isAuthenticated = await authStore.checkAuthStatus();

        if (!isAuthenticated) {
            next({
                name: 'login',
                query: { redirect: to.fullPath },
            });
            return;
        }
    }

    next();
};

// Guard para rotas que só admin pode acessar
export const requireAdmin = async (to, from, next) => {
    const authStore = useAuthStore();

    // Primeiro verifica autenticação
    if (!authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();

        if (!isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } });
            return;
        }
    }

    // Depois verifica se é admin
    if (!authStore.isAdmin) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para rotas que só manager pode acessar
export const requireManager = async (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();

        if (!isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } });
            return;
        }
    }

    if (!authStore.isManager) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para rotas que só profissional de saúde pode acessar
export const requireHealthProfessional = async (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();

        if (!isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } });
            return;
        }
    }

    if (!authStore.isProfessional) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para admin OU manager
export const requireAdminOrManager = async (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();

        if (!isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } });
            return;
        }
    }

    if (!authStore.isAdmin && !authStore.isManager) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Guard para rotas que só usuários NÃO autenticados podem acessar (login)
export const requireGuest = async (to, from, next) => {
    const authStore = useAuthStore();

    // Se tem dados de usuário, verifica se a sessão ainda é válida
    if (authStore.isAuthenticated) {
        // Verifica com o backend
        const isAuthenticated = await authStore.checkAuthStatus();

        if (isAuthenticated) {
            // Redireciona baseado na role
            if (authStore.isAdmin) {
                next({ name: 'admin-dashboard' });
            } else if (authStore.isManager) {
                next({ name: 'manager-dashboard' });
            } else if (authStore.isProfessional) {
                next({ name: 'health-dashboard' });
            } else {
                next({ name: 'unauthorized' });
            }
            return;
        }
    }

    next();
};

// Guard global para inicializar autenticação (roda em TODAS as rotas)
export const initializeAuth = async (to, from, next) => {
    const authStore = useAuthStore();

    // Só inicializa uma vez por sessão da aplicação
    if (!authStore._initialized) {
        await authStore.initializeAuth();
        authStore._initialized = true;
    }

    next();
};
