<template>
  <div>
    <h1>Image Database</h1>
    <p>created by Charles Williams</p>
    <SearchBar @search="handleSearch"/>
    <FilterTable @filter="handleFilter" />
    <button @click="openUploadModal">Add New Image</button>
    <div class="image-grid" v-if="images.length">
      <div class="image-item" v-for="image in images" :key="image.id" @click="showImage(image)">
        <img :src="image.url" :alt="image.title" />
        <p>{{ image.title }}</p>
      </div>
    </div>
    <div v-else>
      <p>No images available</p>
    </div>
    <!-- MODAL TO SEE FULL IAMGE -->
    <ModalComponent :isOpen="isImgModalOpen" @modal-close="closeImgModal" name="image-modal">
      <template #header>Custom header</template>
      <template #content>
        <img :src="modal_image.url" :alt="modal_image.title" v-if="modal_image"/>
      </template>
    </ModalComponent>
    <!-- MODAL TO UPLOAD IMG TO DB -->
    <ModalComponent :isOpen="isUploadModalOpen" @modal-close="closeUploadModal" name="upload-modal">
        <template #header>Upload Image</template>
        <template #content>
          <UploadImage @upload="uploadImage" />
        </template>
    </ModalComponent>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  import SearchBar from './SearchBar.vue';
  import FilterTable from './FilterTable.vue';
  import ModalComponent from "./ModalComponent.vue";
  import UploadImage from "./UploadImage.vue";
  // import { is } from 'core-js/core/object';
  export default {
    components: {
      SearchBar,
      FilterTable,
      ModalComponent,
      UploadImage
    },
    data() {
      return {
        images: [],
        query: '',
        skip: 0,
        limit: 10,
        isImgModalOpen: false,
        isUploadModalOpen: false,
        modal_image: {
          url: '',
          title: ''
        }
      };
    },
    created() {
      this.fetchImages();
    },
    methods: {
      fetchImages(query = '', skip = 0, limit = 100) {
        axios.get(`http://localhost:8000/images/`, {
          params: {
            skip: skip,
            limit: limit,
            title: query
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
        // this.fetchImages('title/', query, this.skip, this.limit);
        if (query === '') {
          this.fetchImages();
          return;
        }
        axios.get(`http://localhost:8000/images/title/` + query)
        .then(response => {
          this.images = response.data;
        })
        .catch(error => {
          console.error('Error fetching images:', error);
        });
      },
      handleFilter({ skip, limit }) {
        this.skip = skip;
        this.limit = limit;
      },closeImgModal(){
        this.isImgModalOpen = false;
      },openImgModal(){
        this.isImgModalOpen = true;
      },showImage(image){
        this.modal_image = image;
        this.openImgModal();
      },openUploadModal(){
        this.isUploadModalOpen = true;
      },closeUploadModal(){
        this.isUploadModalOpen = false;
      },uploadImage(title, description, url){
        axios.post(`http://localhost:8000/images/`, {
          title: title,
          description: description,
          url: url
        })
        .then(response => {
          this.images.push(response.data);
          this.closeUploadModal();
        })
        .catch(error => {
          console.error('Error uploading image:', error);
        });
      }
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

  .modal-content img {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    display: block;
    /* border: 5px solid red; */
  }
  button {
    margin-top: 0.5em;
    margin-bottom: 1em;
    padding: 0.5em 1em;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>