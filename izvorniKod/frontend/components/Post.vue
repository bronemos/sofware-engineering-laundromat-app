<template>
  <div class="card-container">
    <div class="card u-clearfix">
      <section>
        <button class="button-delete">x</button>
        <div class="card-body">
          <!--span class="card-number card-circle subtle"></span-->
          <label>
            <span> Posted on: {{ date }} </span>
          </label>
          <!---span class="card-author subtle">John Smith</span--->
          <h2 v-if="type == 'job'" class="card-title">Oglas za posao</h2>
          <h2 v-if="type == 'lost'" class="card-title">Zaboravljen odjevni predmet</h2>
          <span class="card-description">
            <p>
              {{ post.text }}
            </p></span
          >

          <div class="card-read"></div>
        </div>
        <div class="post-image">
          <img :src="post.photo" class="card-media" />
        </div>
      </section>
    </div>
    <div class="card-shadow"></div>
  </div>

  <!---div>
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
  </div--->
</template>

<script>
export default {
  name: "Post",
  props: {
    post: Object,
    type: String,
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
html {
  background: #faf7f2;
  box-sizing: border-box;
  font-family: sans-serif;
  font-size: 14px;
  font-weight: 400;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}

.u-clearfix:before,
.u-clearfix:after {
  content: " ";
  display: table;
}

.u-clearfix:after {
  clear: both;
}

.u-clearfix {
  *zoom: 1;
}

.subtle {
  color: #aaa;
}

.card-container {
  margin: 25px auto 0;
  position: relative;
  width: 1000px;
}

.card {
  background-color: #fff;
  padding: 30px;
  position: relative;
  box-shadow: 0 0 5px rgba(75, 75, 75, 0.07);
  z-index: 1;
}

.card-body {
  float: left;
  width: 450px;
}

.card-number {
  margin-top: 15px;
}

.card-circle {
  border: 1px solid #aaa;
  border-radius: 50%;
  display: inline-block;
  line-height: 22px;
  font-size: 12px;
  height: 25px;
  text-align: center;
  width: 25px;
}

.card-author {
  display: block;
  font-size: 12px;
  letter-spacing: 0.5px;
  margin: 15px 0 0;
  text-transform: uppercase;
}

.card-title {
  font-family: sans-serif;
  font-size: 40px;
  font-weight: 300;
  line-height: 60px;
  margin: 10px 0;
}

.card-description {
  display: inline-block;
  font-weight: 300;
  line-height: 22px;
  margin: 10px 0;
}

.card-read {
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 6px;
  margin: 5px 0 20px;
  position: relative;
  text-align: right;
  text-transform: uppercase;
}

.card-read:after {
  background-color: #b8bddd;
  content: "        ";
  display: block;
  height: 1px;
  position: absolute;
  top: 9px;
  width: 75%;
}

.card-tag {
  float: right;
  margin: 5px 0 0;
}

.card-media {
  float: right;
  width: 310px;
  height: 100%;
  border-radius: 10px;
}

.card-shadow {
  background-color: #fff;
  box-shadow: 0 2px 25px 2px rgba(0, 0, 0, 1), 0 2px 50px 2px rgba(0, 0, 0, 1),
    0 0 100px 3px rgba(0, 0, 0, 0.25);
  height: 1px;
  margin: -1px auto 0;
  width: 80%;
  z-index: -1;
}
section {
  width: 100%;
  float: left;
}
  .button-delete {
  border: 2px solid;
  border-color: grey;
  color: gray;
  background-color: white;
  border-radius: 5px;
  padding: 0px 5px;
  text-align: center;
  font-size: 12px;
  margin: 4px 2px;
  cursor: pointer;
position:absolute; top:0; right:0;
  }

</style>
