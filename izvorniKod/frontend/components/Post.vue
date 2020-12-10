<template>

  <div >
    <div class="media-body post-theme p-5">
      <h5 class="lead">
        <span class="three-dots"><strong>...</strong></span>
      </h5>

      <hr class="mt-2 post-separator-theme" />

      <p class="lead">
        {{ post.text }}
      </p>

      <div class="post-image">
        <img :src="post.photo" />
      </div>

      <div class="container-fluid">
        <span> Posted on: {{ date }} </span>
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
  }
};
</script>
<style>
 
    .submit-btn {
    width: 20%;
    padding: 10px 30px;
    cursor: pointer;
    display: block;
    margin: 20px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border: 0;
    outline: none;
    border-radius: 30px;
    color: white;
  }
   
</style>
