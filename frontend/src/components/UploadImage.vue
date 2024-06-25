<template>
    <div>
      <input v-model="title" placeholder="Title..." />
      <input v-model="description" placeholder="Img Description..." />
      <input v-model="url" placeholder="Public Image URL..." />
      <button @click="upload">Upload</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        description: '',
        url: ''
      };
    },
    methods: {
      upload() {
        this.$emit('upload', this.title, this.description, this.url);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add any styles specific to your search bar here */
  input {
    padding: 0.5em;
    margin-right: 0.5em;
  }
  button {
    padding: 0.5em;
  }
  </style>