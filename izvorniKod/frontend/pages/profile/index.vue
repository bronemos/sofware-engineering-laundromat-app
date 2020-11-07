<template>
  <div class="hero">
    <div class="header">
          <NuxtLink to="/">Home</NuxtLink>
          <NuxtLink to="/login">Login</NuxtLink>
          <NuxtLink to="/zaposlenik/pending">Zaposlenik</NuxtLink>
    </div>
    <div class="form-box">
      <nuxt-link to="/">Home</nuxt-link>
      <fieldset>
        <legend>Detalji korisnika</legend>
        <div class="form-group">
          <label for="first_name">Ime</label>
          <input type="text" id="first_name" :value="user.first_name">
        </div>
        <div class="form-group">
          <label for="last_name">Prezime</label>
          <input type="text" id="last_name" :value="user.last_name">
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="text" id="email" :value="user.email">
        </div>
      </fieldset>
    </div>

  </div>
</template>

<script>
  export default {
    middleware: 'auth',

    computed: {
      user() {
        return this.$auth.user
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

  #btn {
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
    text-align: center;
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

  label {
    float: left;
  }

  span {
    color: #777;
    font-size: 12px;
    bottom: 68px;
    position: absolute;
  }

  #form {
    background-color: #FFF;
    height: 600px;
    width: 600px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 0px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 0px;
    text-align: center;
  }

  label {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 18px;
    color: #333;
    height: 20px;
    width: 200px;
    margin-top: 10px;
    margin-left: 10px;
    text-align: right;
    margin-right: 15px;
    float: left;
  }

  input {
    height: 20px;
    width: 300px;
    border: 1px solid #000;
    margin-top: 10px;
  }

  .check-box {
    margin: 20px 200px 30px 0px;
  }
</style>
