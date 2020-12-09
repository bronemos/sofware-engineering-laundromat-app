<template>
  <b-form id="form">
    <div class="form-group ">
      <label for=""></label>
      <textarea
        class="form-control"
        rows="4"
        v-model="newPost.content"
        placeholder="Write a new post"
      ></textarea>
      <div v-if="!canUploadImage" class="image-upload">
        <label for="file">
          <h5 class="font-theme lead">
            <strong>Upload photo</strong>
          </h5>
        </label>
        <input id="file" name="image" type="file" accept="image/*" ref="file" v-on:change="handleFileUpload()">
      </div>
    </div>

    <div v-if="canUploadImage" class="small-img-preview">
       <img :src="imgUrl">
    </div>

    <button
      @click.prevent="postForm"
      type="submit"
      class="btn btn-purple btn-fill mt-2 text-align btn-post"
      :disabled="disableSubmit"
    >
      Post
    </button>
    <div v-if="openPreview">
        <ImagePreview :post="this.newPost" @post="setImage" />
    </div>
  </b-form>
</template>

<script>
import ImagePreview from './ImagePreview.vue';

export default {
  components: { ImagePreview },
  name: "PostForm",
  data() {
    return {
      openPreview: false,
      newPost: {
        content: "",
        image: null,
      },
      canUploadImage: false
    };
  },
  methods: {
    handleFileUpload(){
      this.newPost.image = this.$refs.file.files[0];
      this.openPreview = true;
    },

    setImage(canUploadImage) {
      this.openPreview = false,
      this.canUploadImage = canUploadImage
      if(!canUploadImage)
        this.newPost.image = null
    },

    async postForm() {
      // console.log(
      //   this.newPost.posted_by +
      //     " " +
      //     this.newPost.content +
      //     " " +
      //     this.newPost.likes_num
      // );
      try {
        let formData = new FormData();
        formData.append("content", this.newPost.content)
        if(this.newPost.image)
          formData.append("image", this.newPost.image)
        let response = await this.$axios.post(
          `post/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        );

        if (response.status == 201) {
          this.$toast.show("Post uspješno objavljen!", { duration: 8000 });
          //Ovaj response ne vraca sliku prvi put!!
          let createdPost = response.data;
          document.getElementById("form").reset();
          this.canUploadImage = false;
          this.$emit("post", createdPost);
        }
      } catch (e) {
        console.log(e)
      }
    },
    
  },
  computed: {
    disableSubmit() {
        return this.newPost.content == ""
    },

    imgUrl() {
      return URL.createObjectURL(this.newPost.image);
    }
  }
};
</script>

<style>
</style>