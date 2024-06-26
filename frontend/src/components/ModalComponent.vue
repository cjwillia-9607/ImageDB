<script setup>
import { defineProps, defineEmits, ref } from "vue";
import {onClickOutside} from '@vueuse/core'

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["modal-close"]);

const target = ref(null)
onClickOutside(target, ()=>emit('modal-close'))

</script>

<template>
  <div v-if="props.isOpen" class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container" ref="target">
        <div class="modal-header">
          <slot name="header">default header</slot>
          <button @click.stop="emit('modal-close')" aria-label="Close">X</button>
        </div>
        <div class="modal-content">
          <slot name="content">default content</slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <button @click.stop="emit('modal-close')">Close</button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
  }

  .modal-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .modal-container {
    max-width: 90vw;
    max-height: 95vh;
    width: auto;
    overflow-y: auto;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    display: flex;
    flex-direction: column;
  }

  .modal-content {
    display: block;
    justify-content: center;
    align-items: center;
    padding: 10px;
    flex-grow: 1;
  }

  .modal-header, .modal-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }

  .modal-footer {
    border-top: 1px solid #e5e5e5;
  }

  button {
    margin-left: auto;
  }
</style>