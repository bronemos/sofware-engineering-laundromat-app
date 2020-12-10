<template>
  <div>
    <div class="media-body post-theme p-5">
       <label>
          <span> Posted on: {{ date }} </span>
        </label>

      <hr class="mt-2 post-separator-theme" />
      <p>
        {{ post.text }}
      </p>

      <div class="post-image">
        <img :src="post.photo" />
      </div>

      <div class="container-fluid">
       
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Post",
  props: {
    post: Object,
  },
  data() {
    return {
      username: "",
    };
  },
  computed: {
    date() {
      let date = new Date(this.post.date);
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
  },
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}
</style>
