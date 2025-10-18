import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/',
    withCredentials: true, // IMPORTANTE: Envia cookies automaticamente
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Função auxiliar para pegar cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Interceptor para adicionar CSRF token
api.interceptors.request.use(
    async (config) => {
        // Pega o CSRF token do cookie
        const csrfToken = getCookie('csrftoken');

        // Adiciona o token em métodos que modificam dados
        if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
            config.headers['X-CSRFToken'] = csrfToken;
        }

        // NÃO adiciona mais o Authorization header com Token
        // Remova qualquer código que adicione: config.headers.Authorization = `Token ${authToken}`;

        return config;
    },
    (error) => Promise.reject(error),
);

// Interceptor de resposta para tratar erros
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Session expirou ou usuário não autenticado
            console.warn('Sessão expirada - redirecionando para login');

            // Limpa dados locais
            localStorage.removeItem('user');

            // Se não estiver na página de login, redireciona
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }

        if (error.response?.status === 403) {
            console.error('Acesso negado - sem permissão');
        }

        if (error.response?.status === 500) {
            console.error('Erro no servidor:', error.response.data);
        }

        return Promise.reject(error);
    },
);

export default api;
