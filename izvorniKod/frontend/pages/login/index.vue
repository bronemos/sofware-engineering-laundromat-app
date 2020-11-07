<template>
  <div class="hero">
    <div class="header">
          <NuxtLink to="/">Home</NuxtLink>
          <NuxtLink to="/login">Login</NuxtLink>
          <NuxtLink to="/zaposlenik/pending">Zaposlenik</NuxtLink>
    </div>
    <div class="form-box">
      <div class="button-box">
        <div id="btn" v-bind:class="login ? 'btn_0' : 'btn_110'"></div>
        <button type="button" class=" toggle-btn" @click="login=true">Prijava</button>
        <button type="button" class=" toggle-btn" @click="login=false">Registracija</button>

      </div>
      <form id="login" class="input-group-login" :class="login ? 'login_50' : 'login_n400'">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model="loginForm.username">
        <input type="password" class="input-field" placeholder="Lozinka" required v-model="loginForm.password">
       <!--- <input type="checkbox" class="check-box"><span>&nbsp;&nbsp;&nbsp;&nbsp;Zapamti zaporku</span>--->
        <button type="button" class="submit-btn" @click="loginUser">Prijava</button>
      </form>

      <form id="register" class="input-group" :class="login ? 'register_450' : 'register_50'">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model=" registerForm.username">
        <input type="text" class="input-field" placeholder="Ime" required v-model=" registerForm.name">
        <input type="text" class="input-field" placeholder="Prezime" required v-model=" registerForm.surname"> 
        <input type="password" class="input-field" placeholder="Datum Rođenja" required
               v-model=" registerForm.birth">
        <input type="email" class="input-field" placeholder="Email" required v-model=" registerForm.email">
        <input type="password" class="input-field" placeholder="Lozinka" required v-model=" registerForm.password">
       
       <!---  <input type="checkbox" class="check-box">
       <span> &nbsp;&nbsp;&nbsp;&nbsp; Slažem se s uvjetima & odredbama</span>--->
        <button type="button" class="submit-btn">Registracija</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
      },
      login: true,
      registerForm: {
        username: '',
        name:'',
        surname:'',  
        birth: '',
        email: '',
        password: '',
      
      }

    };
  },

  methods: {
   async loginUser() {
      try {
        await this.$auth.loginWith('local', {
           data: this.form
         })
        
        // redirect to user profile
        this.$router.push('/profile')

      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, { duration: 8000 });
      }
    },
  },
  
  mounted() {
     if (this.$auth.loggedIn){
        this.$router.push('/profile')
     }
  }
}
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    font-family: sans-serif;
  }

  .login_50 {
    left: 50px;
  }

  .login_n400 {
    left: -400px;
  }

  .register_450 {
    left: 450px;
  }

  .register_50 {
    left: 50px;
  }

  button:focus{
    outline: none !important;
  }

  .btn_0 {
    top: 0;
    left: 0;
    position: absolute;
    width: 120px;
    height: 100%;
    background: linear-gradient(to right, #3a2ee6, #4fdee6);
    border-radius: 30px;
    transition: .5s;
  }

  .btn_110 {
    left: 110px;
    top: 0;
    position: absolute;
    width: 150px;
    height: 100%;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
  }

  .hero {
    height: 100%;
    width: 100%;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/laundry-saloon.jpg');
    position: absolute;
  }

  .form-box {
    height: 500px;
    width: 380px;
    position: relative;
    margin: 6% auto;
    background: #fff;
    padding: 5px;
    overflow: hidden;
  }

  .button-box {
    width: 260px;
    margin: 35px auto;
    position: relative;
    box-shadow: 0 0 20px 9px #1e9aa0b4;
    border-radius: 30px;

  }

  .toggle-btn {
    padding: 10px 30px;
    cursor: pointer;
    background: transparent;
    border: 0;
    outline: none;
    position: relative;
  }

  .btn {
    top: 0;
    left: 0;
    position: absolute;
    width: 120px;
    height: 100%;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
  }

  .input-group {
    top: 100px;
    position: absolute;
    width: 280px;
    transition: .5s;
  }
   .input-group-login {
    top: 120px;
    position: absolute;
    width: 280px;
    transition: .5s;
  }

  .input-field {
    width: 100%;
    padding: 10px 0;
    margin: 4px 0;
    border-left: 0;
    border-top: 0;
    border-right: 0;
    border-bottom: 1px solid #999;
    outline: none;
    background: transparent;
  }

  .submit-btn {
    width: 85%;
    padding: 10px 30px;
    cursor: pointer;
    display: block;
    margin: 20px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border: 0;
    outline: none;
    border-radius: 30px;


  }

  span {
    color: #777;
    font-size: 12px;
    bottom: 68px;
    position: absolute;
  }

  .check-box {
    margin: 20px 200px 30px 0px;
  }
</style>
