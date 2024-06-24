<template>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  </head>
  <img alt="Vue logo" src="./assets/logo.png">
  <ImageGallery />
</template>

<script>
import ImageGallery from './components/ImageGallery.vue';

export default {
  name: 'App',
  components: {
    ImageGallery,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
