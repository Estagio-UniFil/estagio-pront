// composables/useTheme.js
import { ref, watch, onMounted, readonly } from 'vue';

export function useTheme() {
    // Estado reativo do tema
    const isDark = ref(false);

    // Função para alternar o tema
    const toggleTheme = () => {
        isDark.value = !isDark.value;
    };

    // Função para definir tema específico
    const setTheme = (theme) => {
        isDark.value = theme === 'dark';
    };

    // Função para obter o tema atual
    const getCurrentTheme = () => {
        return isDark.value ? 'dark' : 'light';
    };

    // Aplicar o tema no HTML
    const applyTheme = (dark) => {
        const html = document.documentElement;

        if (dark) {
            html.setAttribute('data-theme', 'dark');
        } else {
            html.removeAttribute('data-theme');
        }
    };

    // Salvar preferência no localStorage
    const saveThemePreference = (dark) => {
        try {
            localStorage.setItem('theme-preference', dark ? 'dark' : 'light');
        } catch (error) {
            console.warn('Não foi possível salvar a preferência de tema:', error);
        }
    };

    // Carregar preferência do localStorage
    const loadThemePreference = () => {
        try {
            const saved = localStorage.getItem('theme-preference');
            if (saved) {
                return saved === 'dark';
            }
        } catch (error) {
            console.warn('Não foi possível carregar a preferência de tema:', error);
        }

        // Fallback: detectar preferência do sistema
        if (window.matchMedia) {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }

        return false;
    };

    // Detectar mudanças na preferência do sistema
    const setupSystemThemeListener = () => {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

            const handleChange = (e) => {
                // Só atualiza se não há preferência salva
                const savedPreference = localStorage.getItem('theme-preference');
                if (!savedPreference) {
                    isDark.value = e.matches;
                }
            };

            // Listener para mudanças
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', handleChange);
            } else {
                // Fallback para navegadores mais antigos
                mediaQuery.addListener(handleChange);
            }

            // Retorna função para remover o listener se necessário
            return () => {
                if (mediaQuery.removeEventListener) {
                    mediaQuery.removeEventListener('change', handleChange);
                } else {
                    mediaQuery.removeListener(handleChange);
                }
            };
        }
    };

    // Watcher para aplicar mudanças do tema
    watch(
        isDark,
        (newValue) => {
            applyTheme(newValue);
            saveThemePreference(newValue);
        },
        { immediate: false },
    );

    // Inicialização
    onMounted(() => {
        // Carregar tema salvo ou preferência do sistema
        const savedTheme = loadThemePreference();
        isDark.value = savedTheme;

        // Aplicar tema imediatamente
        applyTheme(savedTheme);

        // Configurar listener do sistema
        setupSystemThemeListener();
    });

    return {
        isDark: readonly(isDark),
        toggleTheme,
        setTheme,
        getCurrentTheme,
    };
}

// Para uso global (opcional)
// Você pode criar uma instância global se preferir
let globalTheme = null;

export function useGlobalTheme() {
    if (!globalTheme) {
        globalTheme = useTheme();
    }
    return globalTheme;
}
