<template>
    <div>
      <input v-model="query" @keyup.enter="search" placeholder="Search images..." />
      <button @click="search">Search</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        query: ''
      };
    },
    methods: {
      search() {
        this.$emit('search', this.query);
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