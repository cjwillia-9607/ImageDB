<template>
    <div class="tag-box">
        <div v-for="tag in tags" :key="tag" 
        :class="['tag', {'tag-selected': selectedTags.includes(tag)}]">
            <a class="tag-anchor"
            @click="toggleTag(tag)">
            {{ tag.name + ' (' + tag.count + ')'}}
            </a>
        </div>
        <div :class="['delete-button', {'delete-mode-active': deleteMode}]">
            <a class="tag-anchor" @click="deleteMode ? deleteSelectedTags() : toggleDeleteMode()">X</a>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            images: [],
            tags: [],
            selectedTags: [],
            deleteMode: false
        };
    },
    created(){
        this.getAllTags();
    },
    methods: {
        applyTags() {
            this.$emit('taglist', { images: this.images});
        },getAllTags(){
            axios.get('http://localhost:8000/tags/with_count')
            .then(response => {
                this.tags = response.data;
            })
            .catch(error => {
                console.log(error);
            });
        },toggleTag(tag){
            if(this.selectedTags.includes(tag)){
                this.selectedTags = this.selectedTags.filter(t => t !== tag);
            }else{
                this.selectedTags.push(tag);
            }
            if (!this.deleteMode){
                this.searchImages();
            }

        },searchImages(){
            const tag_ids = this.selectedTags.map(tag => tag.id);
            axios.get('http://localhost:8000/images/by_tags', {
                params: {
                    tag_ids: tag_ids
                },
                paramsSerializer: params => {
                    return Object.keys(params).map(key => {
                    return params[key].map(value => `${key}=${value}`).join('&');
                    }).join('&');
                }
            })
            .then(response => {
                this.images = response.data;
                this.applyTags();
            })
            .catch(error => {
                console.log(error);
            });
        },deleteSelectedTags(){
            for (let tag of this.selectedTags) {
                this.deleteTag(tag);
                this.tags = this.tags.filter(t => t !== tag);
            }
            this.selectedTags = [];
            this.toggleDeleteMode();
            this.searchImages();
        },toggleDeleteMode(){
            this.deleteMode = !this.deleteMode;
        },deleteTag(tag){
        axios.get(`http://localhost:8000/tags/name/` + tag.name)
        .then(response => {
          var tag_id = response.data.id;
          axios.delete(`http://localhost:8000/tags/` + tag_id)
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
      }
    }
};

</script>
<style scoped>
  .tag-box {
    margin: 0.5em auto; /* Center the box with vertical margin */
    padding: 1em; /* Add padding inside the box */
    border: 2px solid #ccc; /* Add a border around the box */
    border-radius: 10px; /* Make the corners rounded */
    background-color: #f9f9f9; /* Optionally, add a background color */
    max-width: calc(100% - 2em); /* Ensure the box is not wider than the viewport minus padding */
    max-height: 20vh;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    overflow-y: auto;
  }
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
    background-color: rgb(100, 100, 100);
  }
  .tag-anchor{
    padding: 0.5em;
    background-color: transparent;
    border: none;
    color: white;
    cursor: pointer;
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
</style>