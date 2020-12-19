<template>
  <div class="hero">
    <div class="container emp-profile">
      <form>
        <div class="row">
          <div class="col-md-6">
            <div class="profile-head">
              <h5>Admin {{ user.first_name }} {{ user.last_name }}</h5>
              <ul class="nav nav-tabs" id="myTab">
                <li class="nav-item">
                  <button
                    class="nav-link"
                    v-bind:class="tabSelected === 'hours' ? 'active' : ''"
                    id="details"
                    @click.prevent="
                      tabSelected = 'hours';
                    "
                  >
                    Radno vrijeme
                  </button>
                </li>
                <!---li class="nav-item">
                  <button class="nav-link" v-bind:class="tabSelected === 'prices' ? 'active' : ''" id="prices"
                          @click.prevent="tabSelected='prices'; editProfile=false">Cijene
                  </button>
                </li--->
                <li class="nav-item">
                  <button
                    class="nav-link"
                    v-bind:class="tabSelected === 'users' ? 'active' : ''"
                    id="users"
                    @click.prevent="
                      tabSelected = 'users';
                    "
                  >
                    Korisnici
                  </button>
                </li>
                <li class="nav-item">
                  <button
                    class="nav-link"
                    v-bind:class="tabSelected === 'employees' ? 'active' : ''"
                    id="employees"
                    @click.prevent="
                      tabSelected = 'employees';
                    "
                  >
                    Zaposlenici
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-md-2" v-if="tabSelected === 'hours'">
            <input type="button" class="profile-edit-btn" name="btnAddMore"
                   :value="(tabSelected === 'payment') && user.card === null ? 'Pohrani' : 'Uredi'"
                   @click.prevent="submitUpdate"/>
          </div>
        </div>
        <div class="row" v-if="tabSelected === 'hours'">
          <div class="col-md-8">
            <div class="tab-content profile-tab" id="myTabContent">
              <div
                class="tab-pane fade show active"
                id="details-tab"
              >
                <div class="row">
                  <div class="col-md-4">
                    <label>Početak radnog vremena</label>
                  </div>
                  <div class="col-md-3">
                    <input type="time" class="input-field" v-model="start"/>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Kraj radnog vremena</label>
                  </div>
                  <div class="col-md-3">
                    <input type="time" class="input-field" v-model="end"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row" v-if="tabSelected === 'users' && listUsers.length > 0">
          <table>
            <thead>
            <tr>
              <th>Ime Studenta</th>
              <th>Prezime Studenta</th>
              <th>JMBAG</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="user in listUsers" :key="user" class="show_bt'">
              <td>{{user.first_name}}</td>
              <td>{{user.last_name}}</td>
              <td>{{user.JMBAG}}</td>
              <td>
                <button type="button" id="myBtn-user" class="myBtn" @click="deleteUser(user.id)">Blokiraj</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="row" v-if="tabSelected === 'employees' && listWorkers.length > 0">
          <table>
            <thead>
            <tr>
              <th>Ime Zaposlenika</th>
              <th>Prezime Zaposlenika</th>
              <th>JMBAG</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <!-- za našu bazu promijeniti isActive u aktivan -->
            <tr v-for="user in listWorkers" :key="user" class="show_bt'">
              <td>{{user.first_name}}</td>
              <td>{{user.last_name}}</td>
              <td>{{user.JMBAG}}</td>
              <td>
                <button type="button" id="myBtn-worker" class="myBtn" @click="deleteUser(user.id)">Blokiraj</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    middleware: "auth-admin",

    data() {
      return {
        tabSelected: "hours",
        edit: false,
        start: "",
        end: "",
        username: this.$auth.user.username,
      };
    },

    computed: {
      user() {
        return this.$auth.user;
      },
    },
    mounted() {
      this.$axios.get('admin/list_users/')
        .then(response => {
          this.listUsers = response.data
        })

      this.$axios.get('admin/list_workers/')
        .then(response => {
          this.listWorkers = response.data
        })
    },

    methods: {
      async deleteUser(userId) {
        try {
          let response = await this.$axios.delete(`admin/${userId}/delete_user/`)
          window.location.reload()
          this.$toast.show('Korisnik je blokiran!', {duration: 4000});
        } catch (error) {
          this.$toast.error(error, {duration: 4000});
        }
      },
      async updateHours() {

      }
    },
  };
</script>

<style scoped>
  button:focus {
    outline: none !important;
  }

  input:focus {
    outline: none !important;
  }

  .input-field {
    width: 100%;
    border: 1px solid #999;
    outline: none;
    background: transparent;
  }

  .hero {
    height: 100%;
    width: 100%;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
    url("~@/static/images/terminko1.jpg");
    position: absolute;
  }

  .emp-profile {
    padding: 3%;
    margin-top: 3%;
    margin-bottom: 3%;
    border-radius: 0.5rem;
    background: #fff;
  }

  .profile-img {
    text-align: center;
  }

  .profile-img img {
    width: 70%;
    height: 100%;
  }

  .profile-img .file {
    position: relative;
    overflow: hidden;
    margin-top: -20%;
    width: 70%;
    border: none;
    border-radius: 0;
    font-size: 15px;
    background: #212529b8;
  }

  .profile-img .file input {
    position: absolute;
    opacity: 0;
    right: 0;
    top: 0;
  }

  .profile-head h5 {
    color: #333;
  }

  .profile-head h6 {
    color: #0062cc;
  }

  .profile-edit-btn {
    border: none;
    border-radius: 1.5rem;
    width: 70%;
    padding: 2%;
    cursor: pointer;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    transition: 0.5s;
    color: white;
  }

  .proile-rating {
    font-size: 12px;
    color: #818182;
    margin-top: 5%;
  }

  .proile-rating span {
    color: #495057;
    font-size: 15px;
    font-weight: 600;
  }

  .profile-head .nav-tabs {
    margin-bottom: 5%;
  }

  .profile-head .nav-tabs .nav-link {
    font-weight: 600;
    border: none;
  }

  .profile-head .nav-tabs .nav-link.active {
    border: none;
    border-bottom: 2px solid #0062cc;
  }

  .profile-work {
    padding: 14%;
    margin-top: -15%;
  }

  .profile-work p {
    font-size: 12px;
    color: #818182;
    font-weight: 600;
    margin-top: 10%;
  }

  .profile-work a {
    text-decoration: none;
    color: #495057;
    font-weight: 600;
    font-size: 14px;
  }

  .profile-work ul {
    list-style: none;
  }

  .profile-tab label {
    font-weight: 600;
  }

  .profile-tab p {
    font-weight: 600;
    color: #0062cc;
  }

  .error {
    color: red;
    font-size: 12px;
  }

  .myBtn {
    width: 120px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
    border: 0;
    outline: none;
    color: #fff;
  }

  .show_btn {
    display: contents;
  }

  table {
    display: grid;
    grid-template-columns: minmax(150px, 1fr) minmax(150px, 1.2fr) minmax(150px, 1fr) minmax(150px, 1fr);
    grid-template-rows: 50px;
    background: #fff;
    /* height: 480px; */
    max-height: 450px;
    border-radius: 0.5rem;
    /* padding: 15px; */
    overflow: auto;
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
    background: #17a2b8;
    /* text-align: left; */
    font-weight: normal;
    font-size: 1.1rem;
    color: white;
  }

  td {
    padding-top: 10px;
    padding-bottom: 10px;
    color: #262626;
    max-height: 44px;
  }

  tr:nth-child(even) td {
    background: #f8f6ff;
  }
</style>

