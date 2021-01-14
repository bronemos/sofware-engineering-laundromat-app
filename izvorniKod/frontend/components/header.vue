<template>
  <div>
    <b-navbar toggleable="lg" style="background: linear-gradient(to right, #4e43e2, #4fdee6);" type="dark" variant="info">
      <b-navbar-brand href="/">Terminko</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="localePath('prijava')" v-if="user === null">{{ $t('signIn') }}</b-nav-item>
          <b-nav-item :to="localePath('rezervacije')"  v-if="user !== null">{{ $t('reservation') }}</b-nav-item>
          <b-nav-item :to="localePath('profil')" v-if="user !== null">{{ $t('profile') }}</b-nav-item>
          <b-nav-item :to="localePath('zaboravljeno')" v-if="user !== null">{{ $t('lostAndFound') }}</b-nav-item>
          <b-nav-item :to="localePath('poslovi')">{{ $t('jobs') }}</b-nav-item>
          <b-nav-item :to="localePath('zaposlenik')" v-if="user !== null && (user.is_superuser || user.is_staff)">{{ $t('worker') }}</b-nav-item>
          <b-nav-item :to="localePath('admin')" v-if="user !== null && user.is_superuser">Admin</b-nav-item>
          <b-nav-item @click="logout" v-if="user !== null">{{ $t('signOut') }}</b-nav-item>
          <b-nav-item :to="switchLocalePath('hr')">🇭🇷</b-nav-item>
          <b-nav-item :to="switchLocalePath('en')">🇺🇸</b-nav-item>
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
