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
      </div>
    </div>
    <div v-else>
      <p>No images available</p>
    </div>
    <!-- MODAL TO SEE FULL IAMGE -->
    <ModalComponent :isOpen="isImgModalOpen" @modal-close="closeImgModal" name="image-modal">
      <template #header>
        <h3>
          {{ modal_image.title }}
        </h3>
      </template>
      <template #content>
        <!-- The actual image -->
        <img :src="modal_image.url" :alt="modal_image.title" v-if="modal_image"/>
        <p>
          {{ modal_image.description }}
        </p>
        <!-- tags of the image (want to add option to add tags) -->
        <div class="tag-container">
          <div v-for="tag in modalImgTags" :key="tag" class="tag">
            {{ tag }}
          </div>
          <div class="tag-input">
            <input v-model="newTag" @keydown.enter.prevent="addTag" placeholder="Add tag..." />
          </div>
          <button @click="addTag">+</button>
        </div>
        
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
        },
        modalImgTags: [],
        newTag: ''
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
        }else if (query.startsWith('$')) {
          query = query.slice(1);
          axios.get(`http://localhost:8000/tags/name/` + query)
          .then(response => {
            var tag_id = response.data.id;
            axios.get(`http://localhost:8000/tags/` + tag_id + `/images`)
            .then(response => {
              this.images = response.data;
            })
            .catch(error => {
              console.error('Error fetching images:', error);
            });
          })
          .catch(error => {
            console.error('Error fetching images:', error);
          });
        }else{
          axios.get(`http://localhost:8000/images/title/` + query)
          .then(response => {
            this.images = response.data;
          })
          .catch(error => {
            console.error('Error fetching images:', error);
          });
        }
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
        axios.get(`http://localhost:8000/images/` + image.id + `/tags`)
        .then(response => {
          this.modalImgTags = [];
          for (let tag of response.data) {
            this.modalImgTags.push(tag.name);
          }
        })
        .catch(error => {
          console.error('Error fetching tags:', error);
        });
        this.openImgModal();
      },openUploadModal(){
        this.isUploadModalOpen = true;
      },closeUploadModal(){
        this.isUploadModalOpen = false;
      },uploadImage(title, description, url, tags){
        axios.post(`http://localhost:8000/images/`, {
          title: title,
          description: description,
          url: url
        })
        .then(response => {
          this.images.push(response.data);
          this.createTags(tags, response.data.id);
          this.closeUploadModal();
        })
        .catch(error => {
          console.error('Error uploading image:', error);
        });
      },createTags(tags, image_id){
        for (let tag of tags) {
          axios.post(`http://localhost:8000/tags/`, {
            name: tag
          })
          .then(response => {
            this.createImageTags(image_id, response.data.name);
          })
          .catch(error => {
            console.error('Error uploading tags:', error);
          });
        }
      },createImageTags(image_id, tag_name){
        axios.post(`http://localhost:8000/image_tags/`, {
          image_id: image_id,
          tag_name: tag_name
        })
        .then(response => {
          console.log('Tag added to image:', response.data);
        })
        .catch(error => {
          console.error('Error adding tag to image:', error);
        });
      }, addTag(){
        var tag_name = this.newTag.trim();
        if (tag_name && !this.modalImgTags.includes(tag_name)) {
          this.createTags([tag_name], this.modal_image.id);
          this.modalImgTags.push(tag_name);
          // this.showImage(this.modal_image);
          this.newTag = '';
        }
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
    margin-left: 1em;
    padding: 0.5em 1em;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .tag-container {
    display: flex;
    flex-wrap: wrap;
    margin-top: 1em;
    width: 100%;
  }
  .tag-container button{
    margin-top: 1em;
    margin-bottom: 1em;
    margin-left: 0.5em;
    padding: 0.5em;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    align-items: center;
    justify-content: center;
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
    padding-right: 0.5em;
  }
  </style>