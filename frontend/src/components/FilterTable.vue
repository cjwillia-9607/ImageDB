<template>
    <div class="filter-box">
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
        limitOptions: [null, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
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
  .filter-box {
    margin: 0.5em auto; /* Center the box with vertical margin */
    padding: 1em; /* Add padding inside the box */
    border: 2px solid #ccc; /* Add a border around the box */
    border-radius: 10px; /* Make the corners rounded */
    background-color: #f9f9f9; /* Optionally, add a background color */
    max-width: calc(100% - 2em); /* Ensure the box is not wider than the viewport minus padding */
  }
  </style>