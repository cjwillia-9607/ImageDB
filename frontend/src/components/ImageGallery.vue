<template>
  <div>
    <h1>Image Database</h1>
    <p>created by Charles Williams</p>
    <button @click="toggleSearchMode">Change Search Mode</button>
    <!-- Search and Add Feature -->
    <div v-if="searchTagToggle">
      <SearchBar @search="handleSearch"/>
      <FilterTable @filter="handleFilter" />
    </div>
    <!-- Search by list of Tags -->
    <div v-if="!searchTagToggle">
      <TagList @taglist="handleTags" />
    </div>
    <!-- Add New Image Button -->
    <div class="upload-button">
      <button @click="openUploadModal">Add New Image</button>
    </div>
    <!-- Image Grid/Gallery/Results -->
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
        <img 
          :src="modal_image.url" 
          :alt="modal_image.title"
          ref="imageElement"
          @load="adjustContainerSize"
          v-if="modal_image"/>
        <p>{{ modal_image.description }}</p>
        <!-- tags of the image (want to add option to add tags) -->
        <div 
          class="tag-container"
          :style="{ maxWidth: containerWidth + 'px', maxHeight: containerHeight + 'px' }">
        <!-- all tags -->
          <div 
            v-for="tag in modalImgTags" 
            :key="tag" 
            :class="['tag', {'tag-selected': selectedTags.includes(tag)}]">
              <a class="modal-button" 
              @click="deleteMode ? toggleTagForDeletion(tag) : handleSearch(`$${tag}`)">
                {{ tag }}
              </a>
          </div>
          <div class="tag-input" v-if="!deleteMode">
            <input v-model="newTag" @keydown.enter.prevent="addTag" placeholder="Add tag..." />
          </div>
          <div class="add-button" v-if="!deleteMode">
            <a class="modal-button" @click="deleteMode ? null : addTag()">+</a>
          </div>
          <div :class="['delete-button', {'delete-mode-active': deleteMode}]">
            <a class="modal-button" @click="deleteMode ? deleteSelectedTags() : toggleDeleteMode()">X</a>
          </div>
        </div>
      </template>
      <template #footer>
        <div :class="['delete-button', {'delete-mode-active': deleteImage}]">
          <a :class="['modal-button', {'delete-mode-active': deleteImage}]" @click="deleteModalImage()">
            {{ deleteImage ? "Are you sure?" : "Delete Image"}}
          </a>
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
  import TagList from "./TagList.vue";
  export default {
    components: {
      SearchBar,
      FilterTable,
      ModalComponent,
      UploadImage,
      TagList
    },
    data() {
      return {
        backendURL: 'http://localhost:8000',
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
        newTag: '',
        selectedTags: [],
        deleteMode: false,
        searchTagToggle: true,
        deleteImage: false,
        containerWidth: 0,
        containerHeight: 0,
      };
    },
    created() {
      this.fetchImages();
    },
    methods: {
      fetchImages(query = '', skip = 0, limit = 100) {
        axios.get(backendURL + `/images/`, {
          params: {
            skip: skip,
            limit: limit,
            title: query,
          }
        })
        .then(response => {
          this.images = response.data;
        })
        .catch(error => {
          console.error('Error fetching images:', error);
        });
      },handleSearch(query) {
        this.isImgModalOpen = false;
        if (query === '') {
          this.fetchImages();
          return;
        }else if (query.startsWith('$')) {
          query = query.slice(1);
          axios.get(backendURL + `/tags/name/` + query)
          .then(response => {
            var tag_id = response.data.id;
            axios.get(backendURL + `/tags/` + tag_id + `/images`)
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
          axios.get(backendURL + `/images/title/` + query)
          .then(response => {
            this.images = response.data;
          })
          .catch(error => {
            console.error('Error fetching images:', error);
          });
        }
      },handleFilter({ skip, limit }) {
        this.skip = skip;
        this.limit = limit;
      },closeImgModal(){
        this.isImgModalOpen = false;
      },openImgModal(){
        this.isImgModalOpen = true;
      },showImage(image){
        this.modal_image = image;
        axios.get(backendURL + `/images/` + image.id + `/tags`)
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
        axios.post(backendURL + `/images/`, {
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
          axios.post(backendURL + `/tags/`, {
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
        axios.post(backendURL + `/image_tags/`, {
          image_id: image_id,
          tag_name: tag_name
        })
        .then(response => {
          console.log('Tag added to image:', response.data);
        })
        .catch(error => {
          console.error('Error adding tag to image:', error);
        });
      },addTag(){
        console.log("called addTag")
        var tag_name = this.newTag.trim();
        if (tag_name && !this.modalImgTags.includes(tag_name)) {
          this.createTags([tag_name], this.modal_image.id);
          this.modalImgTags.push(tag_name);
          // this.showImage(this.modal_image);
          this.newTag = '';
        }
      },deleteTag(tag_name){
        axios.get(backendURL + `/tags/name/` + tag_name)
        .then(response => {
          var tag_id = response.data.id;
          axios.delete(backendURL + `/image_tags/` + this.modal_image.id + `/` + tag_id)
          .then(response => {
            console.log('Tag deleted from image:', response.data);
          })
          .catch(error => {
            console.error('Error deleting tag from image:', error);
          });
        })
        .catch(error => {
          console.error('Error fetching tag:', error);
        });
      },toggleDeleteMode(){
        this.deleteMode = !this.deleteMode;
      },toggleTagForDeletion(tag_name){
        if (this.selectedTags.includes(tag_name)) {
          this.selectedTags = this.selectedTags.filter(tag => tag !== tag_name);
        }else{
          this.selectedTags.push(tag_name);
        }
      },deleteSelectedTags(){

        for (let tag of this.selectedTags) {
          this.deleteTag(tag);
          this.modalImgTags = this.modalImgTags.filter(t => t !== tag);
        }
        this.selectedTags = [];
        this.toggleDeleteMode();
      },toggleSearchMode(){
        this.searchTagToggle = !this.searchTagToggle;
      },handleTags({ images }) {
        this.images = images;
      },deleteModalImage(){
        if (this.deleteImage){
          axios.delete(backendURL + `/images/` + this.modal_image.id)
        .then(response => {
          console.log('Image deleted:', response.data);
          this.images = this.images.filter(image => image.id !== this.modal_image.id);
          this.closeImgModal();
        })
        .catch(error => {
          console.error('Error deleting image:', error);
        });
        }
        this.deleteImage = !this.deleteImage;
      },adjustContainerSize() {
        const imgElement = this.$refs.imageElement;
        if (imgElement) {
          // Set container size based on image size
          this.containerWidth = imgElement.naturalWidth;
          this.containerHeight = imgElement.naturalHeight;
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

  .upload-button button {
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

  .modal-content img {
    max-width: 100%;
    width: auto;
    height: auto;
  }
  
  .tag-container {
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto; /* Adds scroll if the content exceeds the container's height */
    justify-content: center;
    margin-top: 1em;
    width: 100%;
  }

  /* .tag {
    display: flex;
    padding: 0.5em;
    margin-top: 1em;
    margin-right: 0.25em;
    margin-bottom: 1em;
    margin-left: 0.25em;
    background-color: #e0e0e0;
    border-radius: 5px;
  } */
  .tag{
    display: flex;
    /* padding: 0.5em; */
    margin-top: 1em;
    margin-right: 0.75em;
    margin-bottom: 1em;
    color: white;
    background-color: darkgrey;
    border-radius: 5px;
    border: none;
  }

  .tag-selected{
    background-color: rgb(255, 117, 117);
  }
   
  .tag-input {
    display: flex;
    align-items: center;
    padding-right: 0.5em;
  }
  .delete-button{
    display: flex;
    /* padding: 0.5em; */
    margin-top: 1em;
    margin-right: 0.25em;
    margin-bottom: 1em;
    margin-left: 0.25em;
    color: white;
    background-color: rgb(70, 70, 70);
    border-radius: 5px;
    border: none;
  }
  .delete-mode-active{
    background-color: red;
  }
  .add-button{
    display: flex;
    /* padding: 0.5em; */
    margin-top: 1em;
    margin-right: 0.25em;
    margin-bottom: 1em;
    margin-left: 0.25em;
    color: white;
    background-color: #007bff;
    border-radius: 5px;
    border: none;
  }
  .add-delete-active{
    background-color: #6386ac;
  }
  
  .modal-button{
    padding: 0.5em;
    background-color: transparent;
    border: none;
    color: white;
    cursor: pointer;
  }
</style>