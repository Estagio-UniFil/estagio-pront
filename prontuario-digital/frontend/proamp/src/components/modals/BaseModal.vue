<template>
    <Transition name="modal-fade">
        <div v-if="show" class="modal-overlay" @click.self="close">
            <div class="modal-content" :style="{ maxWidth: maxWidth }">
                <div class="modal-header">
                    <slot name="header">
                        <h3 class="modal-title">{{ title }}</h3>
                    </slot>
                    <button v-if="closable" @click="close" class="p-2 rounded-full hover:bg-gray-100 transition-colors">
                        <i class="fas fa-times text-gray-500"></i>
                    </button>
                </div>

                <div class="modal-body">
                    <slot></slot>
                </div>

                <div v-if="$slots.footer" class="modal-footer">
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
    show: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: 'Título do Modal',
    },
    maxWidth: {
        type: String,
        default: '48rem', // max-w-lg
    },
    closable: {
        type: Boolean,
        default: true,
    },
});

const emit = defineEmits(['close']);

const close = () => {
    if (props.closable) {
        emit('close');
    }
};

// Fechar com a tecla ESC
const handleKeydown = (e) => {
    if (props.show && props.closable && e.key === 'Escape') {
        close();
    }
};

watch(
    () => props.show,
    (newValue) => {
        if (newValue) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = null;
        }
    },
);

onMounted(() => {
    document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
/* Transição simples para o modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
    transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
    opacity: 0;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
    transition: transform 0.3s ease;
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
    transform: scale(0.9);
}
</style>
