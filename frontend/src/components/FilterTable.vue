<template>
    <div>
      <label for="skip">Skip:</label>
      <select v-model="skip" @change="applyFilters">
        <option v-for="option in skipOptions" :key="option" :value="option">{{ option }}</option>
      </select>
  
      <label for="limit">Limit:</label>
      <select v-model="limit" @change="applyFilters">
        <option v-for="option in limitOptions" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        skip: 0,
        limit: 10,
        skipOptions: [0, 1, 2, 3, 4, 5],
        limitOptions: [1, 2, 3, 4, 5]
      };
    },
    methods: {
      applyFilters() {
        this.$emit('filter', { skip: this.skip, limit: this.limit });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add any styles specific to your filter component here */
  label {
    margin-right: 0.5em;
  }
  select {
    margin-right: 1em;
    padding: 0.5em;
  }
  </style>