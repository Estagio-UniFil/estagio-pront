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
         * Trigger alert.
         * @param {object} payload - Content.
         * @param {string} payload.message - Message.
         * @param {string} [payload.type='success'] - Type.
         * @param {string} [payload.title=''] - Title.
         * @param {number} [duration=5000] - Duration in miliseconds.
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
