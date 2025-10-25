import { useAuthStore } from '@/stores/authStore';

async function checkAuthenticationAndRedirect(authStore, to) {
    if (!authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();
        if (!isAuthenticated) {
            return { name: 'login', query: { redirect: to.fullPath } };
        }
    }

    if (authStore.mustChangePassword && to.name !== 'force-password-change') {
        return { name: 'force-password-change' };
    }

    if (!authStore.mustChangePassword && to.name === 'force-password-change') {
        if (authStore.isAdmin) return { name: 'admin-dashboard' };
        if (authStore.isManager) return { name: 'manager-dashboard' };
        if (authStore.isProfessional) return { name: 'health-dashboard' };
        return { name: 'login' };
    }

    return null;
}

// Admin Guard
export const requireAdmin = async (to, from, next) => {
    const authStore = useAuthStore();
    const redirect = await checkAuthenticationAndRedirect(authStore, to);
    if (redirect) return next(redirect);

    if (!authStore.isAdmin) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Manager Guard
export const requireManager = async (to, from, next) => {
    const authStore = useAuthStore();
    const redirect = await checkAuthenticationAndRedirect(authStore, to);
    if (redirect) return next(redirect);

    if (!authStore.isManager) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

// Health Pro Guard
export const requireHealthProfessional = async (to, from, next) => {
    const authStore = useAuthStore();
    const redirect = await checkAuthenticationAndRedirect(authStore, to);
    if (redirect) return next(redirect);

    if (!authStore.isProfessional) {
        next({ name: 'unauthorized' });
    } else {
        next();
    }
};

export const requirePasswordChange = async (to, from, next) => {
    const authStore = useAuthStore();
    const redirect = await checkAuthenticationAndRedirect(authStore, to);
    if (redirect) {
        return next(redirect);
    }
    next();
};

export const requireGuest = async (to, from, next) => {
    const authStore = useAuthStore();
    if (authStore.isAuthenticated) {
        const isAuthenticated = await authStore.checkAuthStatus();
        if (isAuthenticated) {
            if (authStore.isAdmin) return next({ name: 'admin-dashboard' });
            if (authStore.isManager) return next({ name: 'manager-dashboard' });
            if (authStore.isProfessional) return next({ name: 'health-dashboard' });
            return next({ name: 'unauthorized' });
        }
    }
    next();
};

export const initializeAuth = async (to, from, next) => {
    const authStore = useAuthStore();
    if (!authStore._initialized) {
        await authStore.initializeAuth();
        authStore._initialized = true;
    }
    next();
};
