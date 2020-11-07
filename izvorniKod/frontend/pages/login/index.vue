<template>
  <div class="hero">
    <div class="form-box">
      <div class="button-box">
        <div id="btn" v-bind:class="login ? 'btn_0' : 'btn_110'"></div>
        <button type="button" class=" toggle-btn" @click="login=true">Prijava</button>
        <button type="button" class=" toggle-btn" @click="login=false">Registracija</button>

      </div>
      <form id="login" class="input-group" :class="login ? 'login_50' : 'login_n400'" @submit.prevent="loginUser">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model="form.username">
        <input type="password" class="input-field" placeholder="Lozinka" required v-model="form.password">
        <input type="checkbox" id="remember_pw" class="check-box"><label for="remember_pw">Zapamti zaporku</label>
        <input type="submit" class="submit-btn" value="Log in">
      </form>

      <form id="register" class="input-group" :class="login ? 'register_450' : 'register_50'" @submit.prevent="registerUser">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model="r_form.username">
        <input type="text" class="input-field" placeholder="JMBAG" required v-model="r_form.JMBAG">
        <input type="email" class="input-field" placeholder="Email" required v-model="r_form.email">
        <input type="password" class="input-field" placeholder="Lozinka" required v-model="r_form.password">
        <input type="password" class="input-field" placeholder="Ponovite lozinku" required
               v-model="r_form.password_again">
        <input type="checkbox" id="agree_terms" class="check-box">
        <label for="agree_terms">Slažem se s uvjetima i odredbama</label>
        <button type="submit" class="submit-btn">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          username: '',
          password: '',
        },
        login: true,
        r_form: {
          username: '',
          email: '',
          password: '',
          password_again: '',
          JMBAG: '',
        }

      };
    },

    methods: {
      loginUser: async function() {
        try {
          await this.$auth.loginWith('local', {
            data: this.form
          })
          console.log('here')
          // redirect to user profil
          await this.$router.push('/profil')

        } catch (e) {
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {duration: 8000});
        }
      },
      async registerUser() {
        try {
          let resoonse = this.$axios.post('account/', this.r_form)
        } catch (error) {
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {duration: 8000});
        }
      }
    },
  }
</script>

<style scoped>
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

  button:focus {
    outline: none !important;
  }

  .btn_0 {
    top: 0;
    left: 0;
    position: absolute;
    width: 120px;
    height: 100%;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
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
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
    position: absolute;
  }

  .form-box {
    height: 480px;
    width: 380px;
    position: relative;
    margin: 6% auto;
    background: #fff;
    border-radius: 0.5rem;
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
    top: 120px;
    position: absolute;
    width: 280px;
    transition: .5s;
  }

  .input-field {
    width: 100%;
    padding: 10px 0;
    margin: 5px 0;
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
    margin: auto;
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
    margin: 5px 10px 30px 0px;
  }
</style>
