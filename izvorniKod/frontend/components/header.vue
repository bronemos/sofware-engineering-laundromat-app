<template>
  <div>
    <b-navbar toggleable="lg" style="background: linear-gradient(to right, #4e43e2, #4fdee6);" type="dark" variant="info">
      <b-navbar-brand href="/">Terminko</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/prijava/" v-if="user === null">Prijavi se</b-nav-item>
          <b-nav-item href="/profil/" v-if="user !== null">Profil</b-nav-item>
          <b-nav-item href="/zaboravljeno/" v-if="user !== null">Zaboravljeno</b-nav-item>
          <b-nav-item href="/rezervacije/" disabled v-if="user !== null"
            >Rezervacije</b-nav-item
          >
          <b-nav-item
            href="/zaposlenik/"
            v-if="user !== null && (user.is_superuser || user.is_staff)"
            >Zaposlenik</b-nav-item
          >
          <b-nav-item
            href="/admin/"
            disabled
            v-if="user !== null && user.is_superuser"
            >Admin</b-nav-item
          >
          <b-nav-item @click="logout" v-if="user !== null"
            >Odjavite se</b-nav-item
          >
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  methods: {
    async logout() {
      this.$auth.logout();
    },
  },
  computed: {
    user() {
      if (this.$auth.loggedIn) {
        return this.$auth.user;
      }
      return null;
    },
  },
};
</script>
