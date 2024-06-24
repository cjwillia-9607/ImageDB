<template>
    <div>
      <h1>Image Gallery</h1>
      <div v-if="images">
        <div v-for="image in images" :key="image.id">
          <img :src="image.url" :alt="image.title" />
          <p>{{ image.title }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        images: [],
      };
    },
    created() {
    axios.get('http://localhost:8000/images/display/')
      .then(response => {
        console.log(response.data); // Log the response data
        this.images = response.data;
        for (let i = 0; i < this.images.length; i++) {
        //   remove the leading 'http://localhost:8000' from the image URL
          this.images[i].url = this.images[i].url.replace('http://localhost:8000/', '');
        }
      })
      .catch(error => {
        console.error('Error fetching images:', error);
      });
    },
  };
  </script>
  
  <style scoped>
  /* Add any styles specific to your component here */
  </style>