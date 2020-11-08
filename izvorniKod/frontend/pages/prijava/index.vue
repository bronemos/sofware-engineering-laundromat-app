<template>
  <div class="hero">
    <div class="form-box">
      <div class="button-box">
        <div id="btn" v-bind:class="login ? 'btn_0' : 'btn_110'"></div>
        <button type="button" class="toggle-btn" @click="login=true">Prijava</button>
        <button type="button" class="toggle-btn" @click="login=false">Registracija</button>

      </div>
      <form id="login" class="input-group-login" :class="login ? 'login_50' : 'login_n400'" @submit.prevent="loginUser">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model="loginForm.username">
        <input type="password" class="input-field" placeholder="Lozinka" required v-model="loginForm.password">
        <!--- <input type="checkbox" class="check-box"><span>&nbsp;&nbsp;&nbsp;&nbsp;Zapamti zaporku</span>--->
        <button type="submit" class="submit-btn">Prijava</button>
      </form>

      <form id="register" class="input-group" :class="login ? 'register_450' : 'register_50'"
            @submit.prevent="registerUser" autocomplete="off">
        <input type="text" class="input-field" placeholder="Korisničko ime" required v-model="registerForm.username">
        <input type="text" class="input-field" placeholder="Ime" required v-model="registerForm.first_name">
        <input type="text" class="input-field" placeholder="Prezime" required v-model="registerForm.last_name">
        <input type="text" class="input-field" placeholder="JMBAG" required v-model="registerForm.JMBAG">
        <div class="error" v-if="!$v.registerForm.JMBAG.numeric">JMBAG mora biti broj</div>
        <div class="error" v-if="!$v.registerForm.JMBAG.minLength">JMBAG mora imati točno 10 znamenaka</div>
        <div class="error" v-if="!$v.registerForm.JMBAG.maxLength">JMBAG mora imati točno 10 znamenaka</div>

        <input type="email" class="input-field" placeholder="Email" required v-model="registerForm.email">
        <div class="error" v-if="!$v.registerForm.email.email">Email mora sadržavati @ i valjanu domenu</div>

        <input type="password" class="input-field" placeholder="Lozinka" required v-model="registerForm.password">
        <div class="error" v-if="!$v.registerForm.password.verifyPw">Lozinka mora sadržavati najmanje 8 znakova te slova
          i brojeve.
        </div>
        <input type="password" class="input-field" placeholder="Ponovite lozinku" required
               v-model="registerForm.passwordAgain">
        <div class="error" v-if="!$v.registerForm.passwordAgain.sameAs">Lozinka nije ista</div>

        <!---  <input type="checkbox" class="check-box">
        <span> &nbsp;&nbsp;&nbsp;&nbsp; Slažem se s uvjetima & odredbama</span>--->
        <button type="submit" class="submit-btn">Registracija</button>
      </form>
    </div>
  </div>
</template>

<script>
  import {validationMixin} from "vuelidate";

  const {
    required,
    sameAs,
    email,
    maxLength,
    minLength,
    alphaNum,
    numeric
  } = require("vuelidate/lib/validators");
  const verifyPw = (password) => {
    if (password == '') return true
    const pwRegExp = RegExp('^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$')
    return pwRegExp.test(password)
  }
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
          first_name: '',
          last_name: '',
          JMBAG: '',
          email: '',
          password: '',
          passwordAgain: '',

        },
      };
    },

    mixins: [validationMixin],
    validations: {
      registerForm: {
        JMBAG: {
          minLength: minLength(10),
          maxLength: maxLength(10),
          numeric: numeric,
        },
        email: {
          email: email
        },
        password: {
          verifyPw: verifyPw
        },
        passwordAgain: {
          sameAs: sameAs('password'),
        },
        $invalid: false,
      },
    },
    methods: {

      loginUser: async function () {
        try {
          await this.$auth.loginWith('local', {
            data: this.loginForm
          })
          // redirect to user profil
          await this.$router.push('/profil')

        } catch (e) {
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {duration: 5000});
        }
      },
      async registerUser() {
        if (this.$v.$invalid) {
          this.$toast.error('Ispravite greške u formi za registraciju prije ponovnog pokušaja', {duration: 5000})
          return
        }
        try {
          let response = await this.$axios.post('account/', this.registerForm)
        } catch (e) {
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {duration: 5000});
          if (e.response.data) {
            for (let key in e.response.data) {
              if (key == 'non_field_errors') {
                let nonFieldErrors = e.response.data[key][0]
                nonFieldErrors = nonFieldErrors.substring(1, nonFieldErrors.length - 1)
                this.$toast.error(`${nonFieldErrors}`, {duration: 5000});
              } else
                this.$toast.error(`${key}: ${e.response.data[key]}`, {duration: 5000});
            }
          }
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
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
    position: absolute;
  }

  .form-box {
    height: 550px;
    width: 380px;
    position: relative;
    margin: 6% auto;
    background: #fff;
    padding: 5px;
    overflow: hidden;
    border-radius: 0.5rem
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
    color: black;
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
    margin: 2.5px 0;
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
    color: white;


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

  .error {
    color: red;
    font-size: 12px;
  }
</style>
