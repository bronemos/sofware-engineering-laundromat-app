<template>
  <div>
    <div class="form-box">
      <form class="input-group"></form>
      {{user.email}}
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

  .btn_0 {
    left: 0px
  }

  .btn_110 {
    right: 110px;
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
    margin: 20px 200px 30px 0px;
  }
</style>
