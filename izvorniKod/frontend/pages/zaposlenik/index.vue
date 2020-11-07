<template>
  <div class="root">
      <div>
          <NuxtLink to="/">Home</NuxtLink>
      </div>
      <table>
        <thead>
          <tr>
            <th>Ime Studenta</th>
            <!-- <th>Prezime Studenta</th> -->
            <th>JMBAG</th>
            <th>Akcije</th>
          </tr>
        </thead>
        <tbody>
          <!-- za našu bazu promijeniti isActive u aktivan -->
          <tr v-for="user in pendingUsers" :key="user" class="show_bt'">
            <td>{{user.first_name}}</td>
            <!-- <td>{{user.last_name}}</td> -->
            <td>{{user.JMBAG}}</td>
            <td><button id="myBtn"  @click="activate(user.id)">Activate</button></td>
          </tr>
        </tbody>
      </table>
   </div>
</template>

<!-- maknuti hardkodirani json u pendingUsers -->
<script>
export default {
  middleware: 'auth-staff',
  data() {
    return {
        pendingUsers: []
    }
  },

  head() {
    return {
      title: "Registracije u tijeku"
    };
  },

  methods: {
    async activate(userId) {
      try {
        let response = await this.$axios.post(`/account/${userId}/confirm/`)
        this.$toast.show('Korisnik uspješno potvrđen!', {duration: 4000});
        window.location.reload(true)
      } catch (error) {
        this.$toast.error(error, {duration: 8000});
      }
    }
  },

  mounted() {
    this.$axios.get('account/pending_users/')
    .then(response => {this.pendingUsers = response.data.pending})
  }
}
</script>

<style>
  .root {
    height: 100%;
    width: 100%;
    margin: auto;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
    position: absolute;
    box-sizing: border-box;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  table {
    display: grid;
    grid-template-columns: minmax(150px, 2fr) minmax(150px, 1fr) minmax(150px, 2fr);
    grid-template-rows: 50px;
    margin: 6% 20%;
    background: #fff;
    height: 480px;
    /* padding: 15px; */
    overflow: hidden;
    border-collapse: collapse;
    /* min-width: 100%; */
  }

  thead, tbody, tr {
    display: contents;
  }
  
  th, td {
    padding: 15px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th {
    position: sticky;
    top: 0;
    background: #4e43e2;
    /* text-align: left; */
    font-weight: normal;
    font-size: 1.1rem;
    color: white;
  }


  td {
    padding-top: 10px;
    padding-bottom: 10px;
    color: #262626 ;
  }

  tr:nth-child(even) td {
    background: #f8f6ff;
  }
  
  #myBtn {
    width: 120px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
    border: 0;
    outline: none;
    color: #262626 ;
  }
  .show_btn {
    display: contents;
  }
  .hide_btn {
    display: none;
  }
</style>