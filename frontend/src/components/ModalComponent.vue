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

<!-- <template>
  <div v-if="props.isOpen" class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container" ref="target">
        <div class="modal-header">
          <slot name="header"> default header </slot>
        </div>
        <div class="modal-body">
          <slot name="content"> default content </slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <div>
              <button @click.stop="emit('modal-close')">Submit</button>
            </div>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template> -->

<!-- <style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-container {
  width: 300px;
  margin: 150px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

</style> -->
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
    width: 100%;
    height: 100%;
    overflow: auto;
  }

  .modal-container {
    max-width: 90vw;
    max-height: 95vh;
    /* overflow: hidden; */
    overflow-y: auto;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    display: flex;
    flex-direction: column;
  }

  .modal-content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    flex-grow: 1;
    /* background-color: yellow; */
  }

  /* .modal-content img {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    display: block;
    border: 5px solid red;
  } */

  .modal-header, .modal-footer {
    display: flex;
    justify-content: space-between;
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