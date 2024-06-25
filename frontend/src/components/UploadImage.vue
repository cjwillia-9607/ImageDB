<template>
    <div>
      <input v-model="title" placeholder="Title..." />
      <input v-model="description" placeholder="Img Description..." />
      <input v-model="url" placeholder="Public Image URL..." />
      <!-- Tag input and display area -->
      <div class="tag-container">
        <div v-for="tag in tags" :key="tag" class="tag">
          {{ tag }}
        </div>
        <div class="tag-input">
          <input v-model="newTag" @keydown.enter.prevent="addTag" placeholder="Add tag..." />
          <button @click="addTag">+</button>
        </div>
      </div>

      <button @click="upload">Upload</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        description: '',
        url: '',
        tags: [],
        newTag: ''
      };
    },
    methods: {
      upload() {
        this.$emit('upload', this.title, this.description, this.url, this.tags);
      },
      addTag() {
      if (this.newTag.trim() && !this.tags.includes(this.newTag.trim())) {
        this.tags.push(this.newTag.trim());
        this.newTag = '';
        }
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
  .tag-container {
    display: flex;
    flex-wrap: wrap;
    margin-top: 1em;
  }
  .tag {
    padding: 0.5em;
    margin: 0.5em;
    background-color: #e0e0e0;
    border-radius: 5px;
  }
  .tag-input {
    display: flex;
    align-items: center;
  }
  .tag-input input {
    padding: 0.5em;
    margin-right: 0.5em;
  }
  </style>