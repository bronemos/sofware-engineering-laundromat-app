<template>
  <b-form id="form">
    <div class="form-group ">
      <label for=""></label>
      <textarea
        class="form-control"
        rows="4"
        v-model="newPost.text"
        placeholder="Napišite tekst"
      ></textarea>
      <div v-if="!canUploadImage" class="image-upload">
        <label for="file">
          <h5 class="font-theme lead">
            <strong>Priložite fotografiju</strong>
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
  </b-form>
</template>

<script>

export default {
  name: "PostForm",
  props: {
    type: String
  },
  data() {
    return {
      newPost: {
        text: "",
        photo: null,
        posted_by: this.$auth.user.id
      },
      canUploadImage: false
    };
  },
  methods: {
    handleFileUpload(){
      this.newPost.photo = this.$refs.file.files[0];
      this.openPreview = true;
    },
    async postForm() {
      try {
        let formData = new FormData();
        formData.append("text", this.newPost.text)
        formData.append("posted_by", this.newPost.posted_by)
        formData.append("type", this.type)
        if(this.newPost.photo)
          formData.append("photo", this.newPost.photo)
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
          this.newPost.text = "";
          this.newPost.photo = null;
          this.$emit("post", createdPost);
        }
      } catch (e) {
        console.log(e)
      }
    },
    
  },
  computed: {
    disableSubmit() {
        return this.newPost.text == ""
    },

    imgUrl() {
      return URL.createObjectURL(this.newPost.photo);
    }
  }
};
</script>

<style>
</style>