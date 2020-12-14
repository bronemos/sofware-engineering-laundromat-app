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
        <input type="text" class="input-field" placeholder="IBAN (unos nije obavezan)" v-model="registerForm.iban">
        <div class="error" v-if="registerForm.iban.length != 0 && !isValidIBANNumber(registerForm.iban)">Pogrešan IBAN</div>
        
        <input type="email" class="input-field" placeholder="Email" required v-model="registerForm.email">
        <div class="error" v-if="!$v.registerForm.email.email">Email mora sadržavati @ i valjanu domenu</div>

        <input type="password" class="input-field" placeholder="Lozinka" required v-model="registerForm.password">
        <div class="error" v-if="!$v.registerForm.password.verifyPw && registerForm.password.length !== 0">Lozinka mora sadržavati najmanje 8 znakova te slova
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
          iban: '',

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
        if (this.registerForm.iban.length != 0){
          if(!this.isValidIBANNumber(this.registerForm.iban)){
            this.$toast.error('IBAN nije valjan! Ako ga ne želite dodati obrišite sve znakove.', {duration: 5000})
            return
          }
        }
        if (this.$v.$invalid) {
          this.$toast.error('Ispravite greške u formi za registraciju prije ponovnog pokušaja', {duration: 5000})
          return
        }
        try {
          let response = await this.$axios.post('account/', this.registerForm)
          this.$toast.show('Zahtjev uspješno poslan, molim pričekajte potvrdu računa!', {duration: 5000})
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
      },
      isValidIBANNumber(input) {
        var CODE_LENGTHS = {
            AD: 24, AE: 23, AT: 20, AZ: 28, BA: 20, BE: 16, BG: 22, BH: 22, BR: 29,
            CH: 21, CR: 21, CY: 28, CZ: 24, DE: 22, DK: 18, DO: 28, EE: 20, ES: 24,
            FI: 18, FO: 18, FR: 27, GB: 22, GI: 23, GL: 18, GR: 27, GT: 28, HR: 21,
            HU: 28, IE: 22, IL: 23, IS: 26, IT: 27, JO: 30, KW: 30, KZ: 20, LB: 28,
            LI: 21, LT: 20, LU: 20, LV: 21, MC: 27, MD: 24, ME: 22, MK: 19, MR: 27,
            MT: 31, MU: 30, NL: 18, NO: 15, PK: 24, PL: 28, PS: 29, PT: 25, QA: 29,
            RO: 24, RS: 22, SA: 24, SE: 24, SI: 19, SK: 24, SM: 27, TN: 24, TR: 26,   
            AL: 28, BY: 28, CR: 22, EG: 29, GE: 22, IQ: 23, LC: 32, SC: 31, ST: 25,
            SV: 28, TL: 23, UA: 29, VA: 22, VG: 24, XK: 20
        };
        var iban = String(input).toUpperCase().replace(/[^A-Z0-9]/g, ''), // keep only alphanumeric characters
                code = iban.match(/^([A-Z]{2})(\d{2})([A-Z\d]+)$/), // match and capture (1) the country code, (2) the check digits, and (3) the rest
                digits;
        // check syntax and length
        if (!code || iban.length !== CODE_LENGTHS[code[1]]) {
            return false;
        }
        // rearrange country code and check digits, and convert chars to ints
        digits = (code[3] + code[1] + code[2]).replace(/[A-Z]/g, function (letter) {
            return letter.charCodeAt(0) - 55;
        });
        // final check
        return this.mod97(digits);
      },

      mod97(string) {
        var checksum = string.slice(0, 2), fragment;
        for (var offset = 2; offset < string.length; offset += 7) {
            fragment = String(checksum) + string.substring(offset, offset + 7);
            checksum = parseInt(fragment, 10) % 97;
        }
        return checksum;
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
