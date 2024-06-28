<template>
    <div class="tag-box">
        <div v-for="tag in tags" :key="tag" 
        :class="['tag', {'tag-selected': selectedTags.includes(tag)}]">
            <a class="tag-anchor"
            @click="toggleTag(tag)">
            {{ tag.name + ' (' + tag.count + ')'}}
            </a>
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
            selectedTags: []
        };
    },
    created(){
        this.getAllTags();
    },
    methods: {
        applyTags() {
            this.$emit('taglist', { images: this.images});
        },getAllTags(){
            axios.get('http://localhost:8000/tags/with_count/')
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
            this.searchImages();

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
        }
        // ,getImageCount(tag_id){
        //     axios.get('http://localhost:8000/tags/' + tag_id + '/count')
        //     .then(response => {
        //         return response.data;
        //     }).catch(error => {
        //         console.log(error);
        //     });
        // }
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
</style>