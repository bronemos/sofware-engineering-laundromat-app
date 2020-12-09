<template>
  <div class="media p-2 font-theme">
    <div class="media-body post-theme p-5">
      <h5 class="lead">
        <b-avatar class="mb-2"></b-avatar>
        <strong
          ><nuxt-link
            class="text-theme"
            :to="{ name: 'users-id', params: { id: post.posted_by.id } }"
          >
            {{ post.posted_by.username }}
          </nuxt-link></strong
        >
        <span class="three-dots"><strong>...</strong></span>
      </h5>

      <hr class="mt-2 post-separator-theme" />

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="post-image">
        <img :src="post.image" />
      </div>

      <div class="container-fluid">
        <span> Posted on: {{ date }} </span>
        <div class="d-inline float-right">
          <div :id="post.id" class="like-img" @click="likePost"></div>
          <!-- <button class="btn-sm btn-warning" @click="likePost">
            -->
          <!-- <span v-if="!liked">Like this!</span> -->
          <!-- <span v-else>Dislike this!</span> -->
          <!-- </button> -->
          <!-- <button class="btn-sm btn-warning">Comment!</button> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "Post",
  props: {
    post: Object
  },
  data() {
    return {
      username: "",
    };
  },
  computed: {
    date() {
      let date = new Date(this.post.time);
      let string =
        (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) +
        "/" +
        (date.getMonth() < 10 ? "0" + date.getMonth() : date.getMonth()) +
        "/" +
        date.getFullYear() +
        " at " +
        (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) +
        ":" +
        (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes());
      // debugger;
      return string;
    },
  },
  mounted() {
    var classname = this.post.id;
    //document.getElementById(this.post.id).classList.toggle(classname);
  }
};
</script>
