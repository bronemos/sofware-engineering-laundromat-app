<template class="background">
  <div class="background">
    <div class="container">
      <div class="title-container">
        <h1 class="title fadeInDown animated">
          Terminko
        </h1>
        <h2 class="subtitle fade-in">
          {{ $t('greeting') }}
        </h2>
      </div>
      <div class="info-container">
        <div class="work-hours fade-in delay" >
          <h3>{{ $t('workHours') }}</h3>
          <h5>{{ $t('monToSat')}}: {{laundry.open_time}} - {{laundry.close_time}}</h5>
          <h5>{{ $t('pauses')}}: {{laundry.pause_start}} - {{laundry.pause_end}} | {{laundry.pause2_start}} - {{laundry.pause2_end}}</h5>
          <h5>{{ $t('sundayNotWorking')}}</h5>
        </div>
        <div class=" fade-in delay" >
          <h3>{{ $t('prices') }}:</h3>
          <h5>{{ $t('washing') }}: {{laundry.wash_price}} kn</h5>
          <h5>{{ $t('drying') }}: {{laundry.drying_price}} kn</h5>
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
    this.laundry.open_time = this.laundry.open_time.substring(0, this.laundry.open_time.length - 3);
    this.laundry.close_time = this.laundry.close_time.substring(0, this.laundry.close_time.length - 3);
    this.laundry.pause_start = this.laundry.pause_start.substring(0, this.laundry.pause_start.length - 3);
    this.laundry.pause_end = this.laundry.pause_end.substring(0, this.laundry.pause_end.length - 3);
    this.laundry.pause2_start = this.laundry.pause2_start.substring(0, this.laundry.pause2_start.length - 3);
    this.laundry.pause2_end = this.laundry.pause2_end.substring(0, this.laundry.pause2_end.length - 3);
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;

}

.title-container {
  position: absolute;
  top: 27.5%;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.animated {
/*   padding-top:95px;
 */  /* margin-bottom:60px; */
  -webkit-animation-duration: 5s;
  animation-duration: 5s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.info-container {
  color: #64686c;
  position: absolute;
  top: 50%;
}

.work-hours {
  padding: 50px 50px 20px 50px;
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
