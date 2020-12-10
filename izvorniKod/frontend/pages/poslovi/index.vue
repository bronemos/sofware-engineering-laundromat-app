<template>
  <div class="hero">
  <div style="display: flex; flex-direction: column;">
   
    <div v-if="user.is_staff || user.is_superuser">
      <PostForm @post="setPost" type="job"/>
    </div>
    <div style="display: flex; flex-direction: column;" v-for="post in posts" :key="post.id">
      <Post :post="post" />
    </div>

  </div>
    </div>
</template>

<script>

import Post from "@/components/Post";
import PostForm from "@/components/PostForm";

export default {
  name: "Izgubljeno/nadeno",
  components: {Post, PostForm },
 
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
    this.posts = response.data.filter(post => post.type == 'job');
  }
};
</script>

<style>
 .hero {
    height: 100%;
    width: 100%;
    background-position: center;
    background-size: cover;
    background-color: #fff;
    position: absolute;
  }</style>
