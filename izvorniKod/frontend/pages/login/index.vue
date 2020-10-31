<template>
  <div>
    Login page
    <input type="text" v-model="form.username">
    <input type="text" v-model="form.password">
    <button @click="loginUser">Prijavi se</button>
  </div>
</template>

<script>

export default {

  data() {
    return {
      form: {
        username: 'janez',
        password: '12345678',
      }
    };
  },
  methods: {
   async loginUser() {
      try {
        let response = await this.$axios.post(`/account/login/`, this.form);
        this.$toast.show("Zahtjev uspješno poslan!", { duration: 8000 });
        // this.$store.commit('User/SET_LOGGED_USER', response.data.user); spremi usera u store

        // redirect to user profile
        this.$router.push('/')

      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, { duration: 8000 });
      }
    },
  }
}
</script>