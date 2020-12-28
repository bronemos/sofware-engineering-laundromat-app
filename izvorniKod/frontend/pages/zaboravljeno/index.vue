<template>
  <div class="hero">

    <div v-if="user.is_staff || user.is_superuser">
      <PostForm @post="setPost" type="lost"/>
    </div>
    <div style="display: flex; flex-direction: column;" v-for="post in posts" :key="post.id">
      <Post :post="post" type="lost"/>
    </div>

  </div>
</template>

<script>

import Post from "@/components/Post";
import PostForm from "@/components/PostForm";

export default {
  name: "Izgubljeno_nadeno",
  components: {Post, PostForm },
  nuxtI18n: {
    paths: {
      hr: "/zaboravljeno",
      en: "/lost",
    },
  },
  computed: {
    user() {
      if (this.$auth.loggedIn) {
        return this.$auth.user;
      }
      return null;
    },
  },
  data() {
    return {
      posts: []
    };
  },
  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    }
  },
  created: async function() {
    let response = await this.$axios.get(`post/`);
    this.posts = response.data.filter(post => post.type == 'lost');
  }
};
</script>

<style>
 .hero {
    height: 100%;
    width: 100%;
    background-position: center;
    background-size: cover;
    background-color: #f8f5f2;
   /*background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');*/
   position: absolute;
  }</style>
