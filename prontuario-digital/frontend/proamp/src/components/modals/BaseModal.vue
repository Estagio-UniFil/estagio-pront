<template>
    <Transition name="modal-fade">
        <div v-if="show" class="modal-overlay" @click.self="close">
            <div class="modal-content" :style="{ maxWidth: maxWidth }">
                <div class="relative px-8 pt-4 pb-4 border-b-2 border-secondary">
                    <slot name="header">
                        <h3 class="modal-title text-secondary">{{ title }}</h3>
                    </slot>
                    <button v-if="closable" @click="close" class="absolute top-0 right-0 w-8 h-8 rounded-full hover:bg-gray-100 transition-colors flex items-center justify-center">
                        <i class="fas fa-times text-gray-500 text-lg"></i>
                    </button>
                </div>

                <div class="modal-body pt-4 pb-4">
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
        default: 'Modal title',
    },
    maxWidth: {
        type: String,
        default: '48rem',
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

// Close with ESC
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
