import { defineStore } from 'pinia';

export const useAlertStore = defineStore('alert', {
    state: () => ({
        show: false,
        message: '',
        title: '',
        type: 'success',
        timeoutId: null,
    }),
    actions: {
        /**
         * Dispara um alerta na tela.
         * @param {object} payload - O conteúdo do alerta.
         * @param {string} payload.message - A mensagem principal.
         * @param {string} [payload.type='success'] - O tipo do alerta.
         * @param {string} [payload.title=''] - O título do alerta.
         * @param {number} [duration=5000] - Duração em milissegundos.
         */
        triggerAlert({ message, type = 'success', title = '' }, duration = 5000) {
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }

            this.message = message;
            this.type = type;
            this.title = title || (type === 'success' ? 'Sucesso!' : 'Erro!');
            this.show = true;

            this.timeoutId = setTimeout(() => {
                this.hideAlert();
            }, duration);
        },

        hideAlert() {
            this.show = false;
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }
            this.timeoutId = null;
        },
    },
});
