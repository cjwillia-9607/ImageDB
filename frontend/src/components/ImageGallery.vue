<template>
  <div>
    <h1>Image Gallery</h1>
    <SearchBar @search="handleSearch" />
    <FilterTable @filter="handleFilter" />
    <div class="image-grid" v-if="images.length">
      <div class="image-item" v-for="image in images" :key="image.id" @click="showImage(image)">
        <img :src="image.url" :alt="image.title" />
        <p>{{ image.title }}</p>
      </div>
    </div>
    <div v-else>
      <p>No images available</p>
    </div>
    <!-- EXPERIMENTING WITH MODALS -->
    <div>
    <button @click="openModal">Open generic modal</button>
    </div>
    <ModalComponent :isOpen="isModalOpened" @modal-close="closeModal" @submit="submitHandler" name="first-modal">
      <template #header>Custom header</template>
      <template #content>Custom content</template>
      <template #footer>Custom content</template>
    </ModalComponent>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  import SearchBar from './SearchBar.vue';
  import FilterTable from './FilterTable.vue';
  import ModalComponent from "./ModalComponent.vue";
  import { ref } from "vue";
  // import { is } from 'core-js/core/object';
  const isModalOpened = ref(false);

  const openModal = () => {
    isModalOpened.value = true;
  };
  const closeModal = () => {
    isModalOpened.value = false;
  };

  const submitHandler = ()=>{
    //here you do whatever
  }
  export default {
    components: {
      SearchBar,
      FilterTable,
      ModalComponent
    },
    data() {
      return {
        images: [],
        query: '',
        skip: 0,
        limit: 10,
        isModalOpened
      };
    },
    created() {
      this.fetchImages();
    },
    methods: {
      fetchImages(query = '', skip = 0, limit = 10) {
        axios.get(`http://localhost:8000/images`, {
          params: {
            search: query,
            skip: skip,
            limit: limit
          }
        })
        .then(response => {
          this.images = response.data;
        })
        .catch(error => {
          console.error('Error fetching images:', error);
        });
      },
      handleSearch(query) {
        this.query = query;
        this.fetchImages(query, this.skip, this.limit);
      },
      handleFilter({ skip, limit }) {
        this.skip = skip;
        this.limit = limit;
        // this.fetchImages(this.query, skip, limit);
      },closeModal,openModal,submitHandler
    }
  };
  </script>
  
  <style scoped>
  .image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }
  
  .image-item {
    position: relative;
    padding-top: 100%; /* 1:1 Aspect Ratio */
    overflow: hidden;
  }
  
  .image-item img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .image-item p {
    text-align: center;
    margin-top: 8px;
  }

  </style>