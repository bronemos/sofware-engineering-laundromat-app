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
                      editHours = false;
                      addingWorker = false;
                    "
                  >
                    Radno vrijeme
                  </button>
                </li>
                <li class="nav-item">
                  <button
                    class="nav-link"
                    v-bind:class="tabSelected === 'users' ? 'active' : ''"
                    id="users"
                    @click.prevent="
                      tabSelected = 'users';
                      editHours = false;
                      addingWorker = false;
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
                      editHours = false;
                      addingWorker = false;
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
                   :value="this.editHours ? 'Pohrani' : 'Uredi'"
                   @click.prevent="updateHours"/>
          </div>
          <div class="col-md-2" v-if="tabSelected === 'employees'">
            <input type="button" class="profile-edit-btn" name="btnAddMore"
                   value="Dodaj zaposlenika"
                   @click.prevent="addWorker"/>
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
                    <input type="time" class="input-field" v-model="start" :disabled="!editHours"/>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Kraj radnog vremena</label>
                  </div>
                  <div class="col-md-3">
                    <input type="time" class="input-field" v-model="end" :disabled="!editHours"/>
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
        <div class="row" v-if="tabSelected === 'employees' && listWorkers.length > 0 && !addingWorker">
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
                <button type="button" id="myBtn-worker" class="myBtn" @click="deleteUser(user.id)">Otpusti</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="row" v-if="addingWorker">
          <div class="col-md-8">
            <div class="tab-content profile-tab" id="myTabContentEdit">
              <div class="tab-pane fade show active" id="details-tab-edit">
                <div class="row">
                  <div class="col-md-4">
                    <label>Username</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" v-model="workerUsername">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Ime</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" v-model="workerName">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Prezime</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" v-model="workerSurname">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Email</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" type="email" v-model="workerEMail">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>JMBAG</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" v-model="workerJMBAG">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Lozinka</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" type="password" v-model="workerPassword">
                    <div class="error" v-if="!verifyPw(workerPassword) && workerPassword.length !== 0">Format lozinke
                      nije valjan
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Potvrdi lozinku</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" type="password" v-model="workerRepeatedPassword">
                    <div class="error"
                         v-if="!(workerPassword === workerRepeatedPassword) && workerPassword.length !== 0 && workerRepeatedPassword.length !== 0">
                      Lozinka nije ista
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                  </div>
                  <div class="col-md-4">
                    <button type="button" class="cancel" @click.prevent="addingWorker = !addingWorker">Odustani</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
        editHours: false,
        addingWorker: false,
        workerUsername: '',
        workerName: '',
        workerSurname: '',
        workerEMail: '',
        workerJMBAG: '',
        workerPassword: '',
        workerRepeatedPassword: '',

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

      this.$axios.get('laundry/')
        .then(response => {
          this.currentTimes = response.data
          this.$axios.get('laundry/future_laundry/')
            .then(response => {
              this.futureTimes = response.data
              if (this.futureTimes.length === 0) {
                this.forUpdate = this.currentTimes
                this.start = this.currentTimes.open_time
                this.end = this.currentTimes.close_time
              } else {
                this.forUpdate = this.futureTimes[0]
                this.start = this.futureTimes[0].open_time
                this.end = this.futureTimes[0].close_time
              }
            })
        })
    },

    methods: {
      verifyPw(password) {
        const pwRegExp = RegExp('^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$')
        return pwRegExp.test(password)
      },
      verifyHours(hours) {
        let hoursRegExp = RegExp('^\\d{2}:\\d{2}:\\d{2}$')
        return hoursRegExp.test(hours)
      },
      async deleteUser(userId) {
        try {
          let response = await this.$axios.delete(`admin/${userId}/delete_user/`)
          if (this.tabSelected === 'users')
            this.$toast.show('Korisnik je blokiran!', {duration: 4000});
          else
            this.$toast.show('Zaposlenik je otpušten!', {duration: 4000})
          window.location.reload()
        } catch (error) {
          this.$toast.error(error, {duration: 4000});
        }
      },
      async updateHours() {
        if (!this.editHours)
          this.editHours = !this.editHours
        else {
          if (this.start.length === 5)
            this.start += ':00'
          if (this.end.length === 5)
            this.end += ':00'
          if (this.verifyHours(this.start) && this.verifyHours(this.end)) {
            delete this.forUpdate.id
            delete this.forUpdate.date_changed
            delete this.forUpdate.pause_end
            this.forUpdate.open_time = this.start
            this.forUpdate.close_time = this.end
            try {
              let response = await this.$axios.post('laundry/', this.forUpdate)
              this.$toast.success('Novo radno vrijeme uspješno pohranjeno!', {duration: 5000})
              this.editHours = false
            } catch (e) {
              this.$toast.error('Greška pri pohrani!', {duration: 4000})
            }
          } else {
            this.$toast.error('Krivi format radnog vremena!', {duration: 5000})
          }
        }
      },
      async addWorker() {
        if (!this.addingWorker)
          this.addingWorker = !this.addingWorker
        else {
          let formData = new FormData()

          formData.append('password', this.workerPassword)
          formData.append('username', this.workerUsername)
          formData.append('first_name', this.workerName)
          formData.append('last_name', this.workerSurname)
          formData.append('email', this.workerEMail)
          formData.append('JMBAG', this.workerJMBAG)
          try {
            let response = await this.$axios.post('/admin/create_worker_account/', formData)
            this.$toast.success('Zaposlenik uspješno pohranjen!', {duration: 4000})
            window.location.reload()
            this.addingWorker = false
          } catch (e) {
            this.$toast.error('Neuspjelo dodavanje novog zaposlenika, provjerite podatke!', {duration: 4000})
          }
        }
      },
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

  .input-profile {
    width: 60%;
    border-left: 0;
    border-top: 0;
    border-right: 0;
    border-bottom: 1px solid #999;
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

  .cancel {
    width: 60%;
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

