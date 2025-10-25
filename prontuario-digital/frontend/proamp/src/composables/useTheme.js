// composables/useTheme.js
import { ref, watch, onMounted, readonly } from 'vue';

export function useTheme() {
    // Reactive theme state
    const isDark = ref(false);

    const toggleTheme = () => {
        isDark.value = !isDark.value;
    };

    const setTheme = (theme) => {
        isDark.value = theme === 'dark';
    };

    const getCurrentTheme = () => {
        return isDark.value ? 'dark' : 'light';
    };

    const applyTheme = (dark) => {
        const html = document.documentElement;

        if (dark) {
            html.setAttribute('data-theme', 'dark');
        } else {
            html.removeAttribute('data-theme');
        }
    };

    const saveThemePreference = (dark) => {
        try {
            localStorage.setItem('theme-preference', dark ? 'dark' : 'light');
        } catch (error) {
            console.warn('Não foi possível salvar a preferência de tema:', error);
        }
    };

    const loadThemePreference = () => {
        try {
            const saved = localStorage.getItem('theme-preference');
            if (saved) {
                return saved === 'dark';
            }
        } catch (error) {
            console.warn('Não foi possível carregar a preferência de tema:', error);
        }

        // Fallback
        if (window.matchMedia) {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }

        return false;
    };

    const setupSystemThemeListener = () => {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

            const handleChange = (e) => {
                const savedPreference = localStorage.getItem('theme-preference');
                if (!savedPreference) {
                    isDark.value = e.matches;
                }
            };

            // Listener
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', handleChange);
            } else {
                // Fallback
                mediaQuery.addListener(handleChange);
            }

            return () => {
                if (mediaQuery.removeEventListener) {
                    mediaQuery.removeEventListener('change', handleChange);
                } else {
                    mediaQuery.removeListener(handleChange);
                }
            };
        }
    };

    // Watcher to apply theme
    watch(
        isDark,
        (newValue) => {
            applyTheme(newValue);
            saveThemePreference(newValue);
        },
        { immediate: false },
    );

    // Initialization
    onMounted(() => {
        const savedTheme = loadThemePreference();
        isDark.value = savedTheme;

        applyTheme(savedTheme);

        setupSystemThemeListener();
    });

    return {
        isDark: readonly(isDark),
        toggleTheme,
        setTheme,
        getCurrentTheme,
    };
}

let globalTheme = null;

export function useGlobalTheme() {
    if (!globalTheme) {
        globalTheme = useTheme();
    }
    return globalTheme;
}
