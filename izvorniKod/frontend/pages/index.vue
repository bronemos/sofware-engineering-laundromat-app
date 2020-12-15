<template class="background">
  <div class="background">
    <div class="container">
      <div>
        <h1 class="title fadeInDown animated">
          Terminko
        </h1>
        <h2 class="subtitle fade-in">
          Aplikacija za praonicu rublja
        </h2>
        <div class="work-hours fade-in delay">
          <h3>Radno vrijeme:</h3>
          <h5>Pon-Sub: od {{laundry.open_time}} do {{laundry.close_time}}</h5>
          <h5>Pauza: od {{laundry.pause_start}} do {{laundry.pause_end}}</h5>
          <h5>Ned: Ne radimo!</h5>
        </div>
        <div class="work-hours fade-in delay">
          <h3>Cijene:</h3>
          <h5>Pranje: {{laundry.wash_price}} kn</h5>
          <h5>Sušenje: {{laundry.drying_price}} kn</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data(){
    return {
      laundry: {},
    }
  },
  methods: {
    async logout() {
      this.$auth.logout()
    }
  },
  created: async function() {
    let response = await this.$axios.get(`laundry/`);
    this.laundry = response.data;
    // this.laundry.open_time = this.laundry.open_time.substring(0, this.laundry.open_time.length - 3);
    // this.laundry.close_time = this.laundry.close_time.substring(0, this.laundry.close_time.length - 3);
    // this.laundry.pause_start = this.laundry.pause_start.substring(0, this.laundry.pause_start.length - 3);
    // this.laundry.pause_end = this.laundry.pause_end.substring(0, this.laundry.pause_end.length - 3);
  }
}
</script>

<style scoped>
.background {
  height: 100%;
  width: 100%;
  background-position: center;
  background-size: cover;
  background-image: url('~@/static/images/clothes-line.jpg');
}

.container {
  margin: 0 auto;
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  /* padding: 0 0 48px 0; */  /* padding je samo dodano radi štrika */
/*   color: white;
 */  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
/*   color: white;
 */  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.animated {
  padding-top:95px;
  margin-bottom:60px;
  -webkit-animation-duration: 5s;
  animation-duration: 5s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.work-hours {
  color: #aeb6be;
  padding: 50px;
}

.fade-in {
  animation: fadeIn ease 5s;
  -webkit-animation: fadeIn ease 5s;
  -moz-animation: fadeIn ease 5s;
  -o-animation: fadeIn ease 5s;
  -ms-animation: fadeIn ease 5s;
}

@-webkit-keyframes fadeInDown {
   0% {
      opacity: 0;
      -webkit-transform: translateY(-20px);
   }
   100% {
      opacity: 1;
      -webkit-transform: translateY(0);
   }
}

@keyframes fadeInDown {
   0% {
      opacity: 0;
      transform: translateY(-20px);
   }
   100% {
      opacity: 1;
      transform: translateY(0);
   }
}

.fadeInDown {
   -webkit-animation-name: fadeInDown;
   animation-name: fadeInDown;
}

.delay {
  animation-fill-mode: backwards;
  -webkit-animation-fill-mode: backwards;
  animation-delay: 2s;
}

@keyframes fadeIn {
  0% {
    opacity:0;
  }
  100% {
    opacity:1;
  }
}

@-moz-keyframes fadeIn {
  0% {
    opacity:0;
  }
  100% {
    opacity:1;
  }
}

@-webkit-keyframes fadeIn {
  0% {
    opacity:0;
  }
  100% {
    opacity:1;
  }
}

@-o-keyframes fadeIn {
  0% {
    opacity:0;
  }
  100% {
    opacity:1;
  }
}

@-ms-keyframes fadeIn {
  0% {
    opacity:0;
  }
  100% {
    opacity:1;
  }
}
</style>
