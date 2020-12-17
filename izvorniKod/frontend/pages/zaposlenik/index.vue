<template>
  <div class="root">
      <div class="row">
        <div class="table-container">
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
              <!-- za našu bazu promijeniti isActive u aktivan -->
              <tr v-for="user in pendingUsers" :key="user" class="show_bt'">
                <td>{{user.first_name}}</td>
                <td>{{user.last_name}}</td>
                <td>{{user.JMBAG}}</td>
                <td><button id="myBtn"  @click="activate(user.id)">Aktiviraj</button></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="column">
          <div class="inner-body">
            <div class="title">
              <h2>Promjena radnog vremena</h2>
            </div>
            <div class="form-body">
              <!-- <div class="inline-display" >Početak radnog vremena:</div>
              <input type="time" v-model="newHoursPrice.open_time" placeholder="10:00">
              <div class="inline-display">Kraj radnog vremena:</div>
              <input type="time" v-model="newHoursPrice.close_time" placeholder="22:00"> -->
              <div class="inline-display">Početak pauze:</div>
              <input type="time" v-model="newHoursPrice.pause_start" @change="calculatePauseEnd()">
              <div class="inline-display">Kraj pauze:</div>
              <input type="time" v-model="newHoursPrice.pause_end" readonly>
              <div class="inline-display" v-if="user !== null && user.is_superuser">Cijena pranja:</div>
              <input type="number" v-if="user !== null && user.is_superuser" v-model="newHoursPrice.wash_price" placeholder="10.00">
              <div class="inline-display" v-if="user !== null && user.is_superuser">Cijena sušenja:</div>
              <input type="number" v-if="user !== null && user.is_superuser" v-model="newHoursPrice.drying_price" placeholder="10.00">
            </div>
            <div class="padd-15">
              <button id="myBtn" @click.prevent="changeTimePrice()">Promijeni</button>
            </div>
          </div>
        </div>
      </div>
   </div>
</template>

<!-- maknuti hardkodirani json u pendingUsers -->
<script>
export default {
  middleware: 'auth-staff',
  data() {
    return {
      pendingUsers: [],
      laundryId: null,
      newHoursPrice: {
        "pause_start": null,
        "pause_end": null,
        "wash_price": null,
        "drying_price": null
      },
      changed: false,
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
    },
    async changeTimePrice() {
      let formData = new FormData();

      for (let key in this.newHoursPrice) {
        if (this.newHoursPrice[key] != null) {
          this.changed = true;
          formData.append(key, this.newHoursPrice[key]);
        }
      }
      if (this.changed) {
        try {
          let response = await this.$axios.patch(`laundry/${this.laundryId}/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          this.$toast.success("Promjene uspješno pohranjene!", {duration: 5000});
          this.changed = false;
          this.newHoursPrice = {
            "pause_start": null,
            "pause_end": null,
            "wash_price": null,
            "drying_price": null
          };
        } catch (error) {
          this.$toast.error(error, {duration: 8000});
        }
      }
    },
    async calculatePauseEnd() {
      let date = new Date();
      const options = {
        timeZone: "Europe/Zagreb",
        hour12: false,
        hour: "2-digit",
        minute: "2-digit"
      };
      let hrs = parseInt(this.newHoursPrice['pause_start'].substring(0, 3));
      let mins = parseInt(this.newHoursPrice['pause_start'].substring(3, 5));
      if (mins >= 30) {
        mins = 29;
        date.setHours(hrs, mins);
        this.newHoursPrice['pause_start'] = date.toLocaleTimeString("hr-HR", options);
      }
      console.log('hrs, mins: ' + hrs + ', ' + mins);
      if (mins + 30 >= 60) {
        hrs = (hrs + 1) % 24;
      }
      mins = (mins + 30) % 60;
      date.setHours(hrs, mins);
      
      console.log('pause_start: ' + this.newHoursPrice['pause_start']);
      console.log('calc hrs, mins: ' + hrs + ', ' + mins);
      console.log('pause_end: ', date.toLocaleTimeString("hr-HR", options))
      this.newHoursPrice["pause_end"] =  date.toLocaleTimeString("hr-HR", options);
    },
  },

  mounted() {
    this.$axios.get('account/pending_users/')
    .then(response => {this.pendingUsers = response.data.pending})
    this.$axios.get('laundry/')
    .then(response => {this.laundryId = response.data.id})
  },

  computed: {
    user() {
      if (this.$auth.loggedIn) {
        return this.$auth.user;
      }
      return null;
    },
  },
}
</script>

<style scoped>
  .root {
    box-sizing: border-box;
    height: 100%;
    width: 100%;
    margin: 0;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
    position: absolute;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  table {
    display: grid;
    grid-template-columns: minmax(150px, 1fr) minmax(150px,1.2fr) minmax(150px, 1fr) minmax(150px, 1fr);
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

  #myBtn {
    width: 120px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
    border: 0;
    outline: none;
    color: #fff ;
  }
  
  .padd-15 {
    padding: 15px;
  }

  .show_btn {
    display: contents;
  }
  .hide_btn {
    display: none;
  }

  .table-container {
    width: 60%;
    display: inline-block;
    padding: 10px;
  }

  .column {
    float: left;
    width: 39%;
    padding: 10px;
  }

  .inner-body {
    background: #fff;
    border-radius: 0.5rem;
  }

  .inline-display {
    display: inline;
  }

  .form-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 5px;
  }

  .row {
    width: 100%;
    margin: auto;
    justify-content: center;
  }

  .inner-body .title {
    display: flex;
    background: #17a2b8;
    color: white;
    border-radius: 0.5rem 0.5rem 0 0;
    height: 50px;
    text-align: center;
    align-items: center;
    justify-content: center;
  }

  .title h2 {
    margin: 0;
  }

  .row:after {
    content: '';
    display: table;
    clear: both;
  }
</style>
