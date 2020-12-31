<template>
  <div class="root">
    <div class="row">
      <div class="table-container pendingUsers">
        <table v-if="pendingUsers.length != 0">
          <thead>
          <tr>
            <th>{{ $t('nameStudent') }}</th>
            <th>{{ $t('surnameStudent') }}</th>
            <th>JMBAG</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="user in pendingUsers" :key="user.id" class="show_bt'">
            <td>{{user.first_name}}</td>
            <td>{{user.last_name}}</td>
            <td>{{user.JMBAG}}</td>
            <td>
              <button id="myBtn" @click="activate(user.id)">{{ $t('activate') }}</button>
            </td>
          </tr>
          </tbody>
        </table>
        <div v-if="pendingUsers.length == 0" class="inner-body">
          <div class="title">
            <h2>{{$t('unconfReg')}}</h2>
          </div>
          <div>
            <span style='font-size:100px;'>&#128526;</span>
            <div style="color:#707070; padding: 10px;">{{$t('unconfRegInfo')}}</div>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="inner-body">
          <div class="title">
            <h2>{{ $t('changeBreakTime') }} <span v-if="user !== null && user.is_superuser"> {{ $t('andPrices') }}</span></h2>
          </div>
          <div class="form-body">
            <!-- <div class="inline-display" >Početak radnog vremena:</div>
            <input type="time" v-model="newHoursPrice.open_time" placeholder="10:00">
            <div class="inline-display">Kraj radnog vremena:</div>
            <input type="time" v-model="newHoursPrice.close_time" placeholder="22:00"> -->
            <div class="inline-display">{{ $t('start') }} {{ $t('first') }} {{ $t('break') }}:</div>
            <input type="time" v-model="newHoursPrice.pause_start" @change="calculatePauseEnd('pause_start')">
            <div class="inline-display">{{ $t('end') }} {{ $t('first') }} {{ $t('break') }}:</div>
            <input type="time" v-model="newHoursPrice.pause_end" readonly>
            <div class="inline-display">{{ $t('start') }} {{ $t('second') }} {{ $t('break') }}:</div>
            <input type="time" v-model="newHoursPrice.pause2_start" @change="calculatePauseEnd('pause2_start')">
            <div class="inline-display">{{ $t('end') }} {{ $t('second') }} {{ $t('break') }}:</div>
            <input type="time" v-model="newHoursPrice.pause2_end" readonly>
            <div class="inline-display" v-if="user !== null && user.is_superuser">{{ $t('price') }} {{ $t('washingLowercase') }}:</div>
            <input type="number" v-if="user !== null && user.is_superuser" v-model="newHoursPrice.wash_price"
                   placeholder="10.00">
            <div class="inline-display" v-if="user !== null && user.is_superuser">{{ $t('price') }} {{ $t('dryingLowercase') }}:</div>
            <input type="number" v-if="user !== null && user.is_superuser" v-model="newHoursPrice.drying_price"
                   placeholder="10.00">
          </div>
          <div class="padd-15">
            <button id="myBtn" @click.prevent="changeTimePrice()">{{ $t('change') }}</button>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="table-container rentedBaskets">
        <div v-if="baskets.length != 0" class="inner-body">
          <div class="title">
            <h2>{{$t('borrowedBaskets')}}</h2>
          </div>
          <table v-if="baskets.length != 0">
            <tbody>
            <tr v-for="user in baskets" :key="user.id" class="show_bt'">
              <td>{{user.first_name}} {{user.last_name}}</td>
              <td>{{user.baskets}}</td>
              <td>
                <button id="myBtn" @click="returnBasket(user.id)">{{$t('returnBtn')}}</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
         <div v-if="baskets.length == 0" class="inner-body">
          <div class="title">
            <h2>{{$t('borrowedBaskets')}}</h2>
          </div>
          <div>
            <span style='font-size:100px;'>&#129447;</span>
            <div style="color:#707070; padding: 10px;">{{$t('borrowedBasketsInfo')}}</div>
          </div>
        </div>
      </div>
      <div class="column">
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    nuxtI18n: {
    paths: {
      hr: "/zaposlenik",
      en: "/worker",
    },
  },
    middleware: 'auth-staff',
    data() {
      return {
        pendingUsers: [],
        baskets: [],
        laundryId: null,
        newHoursPrice: {
          "pause_start": null,
          "pause_end": null,
          "pause2_start": null,
          "pause2_end": null,
          "wash_price": null,
          "drying_price": null
        },
        changed: false,
      }
    },

    methods: {
      async activate(userId) {
        try {
          let response = await this.$axios.post(`/account/${userId}/confirm/`)
          this.$toast.show('Korisnik uspješno potvrđen!', {duration: 4000});
          await this.$axios.get('account/pending_users/')
            .then(response => {
              this.pendingUsers = response.data.pending
            })
        } catch (error) {
          this.$toast.error(error, {duration: 8000});
        }
      },
      async returnBasket(userId) {
        try {
          let response = await this.$axios.post(`/admin/${userId}/return_basket/`)
          await this.$axios.get('admin/baskets')
            .then(response => {
              this.baskets = response.data
            })
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
              "pause2_start": null,
              "pause2_end": null,
              "wash_price": null,
              "drying_price": null
            };
          } catch (error) {
            this.$toast.error(error, {duration: 8000});
          }
        }
      },
      async calculatePauseEnd(pauseStart) {
        let date = new Date();
        const options = {
          timeZone: "Europe/Zagreb",
          hour12: false,
          hour: "2-digit",
          minute: "2-digit"
        };
        let hrs = parseInt(this.newHoursPrice[pauseStart].substring(0, 3));
        let mins = parseInt(this.newHoursPrice[pauseStart].substring(3, 5));
        if (mins >= 30) {
          mins = 29;
          date.setHours(hrs, mins);
          this.newHoursPrice[pauseStart] = date.toLocaleTimeString("hr-HR", options);
        }
        if (mins + 30 >= 60) {
          hrs = (hrs + 1) % 24;
        }
        mins = (mins + 30) % 60;
        date.setHours(hrs, mins);

        let pauseEnd = pauseStart.slice(0, pauseStart.indexOf('_') + 1) + 'end';
        this.newHoursPrice[pauseEnd] = date.toLocaleTimeString("hr-HR", options);
      },
    },

    mounted() {
      this.$axios.get('account/pending_users/')
        .then(response => {
          this.pendingUsers = response.data.pending
        })
      this.$axios.get('laundry/')
        .then(response => {
          this.laundryId = response.data.id
        })
      this.$axios.get('admin/baskets')
        .then(response => {
          console.log(response.data);
          this.baskets = response.data;
        })
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

  .pendingUsers table {
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

  .rentedBaskets table {
    display: grid;
    grid-template-columns: minmax(150px, 1fr) minmax(150px, 0.8fr) minmax(150px, 1fr);
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
    color: #fff;
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
    grid-template-columns: 1fr 0.5fr;
    padding: 5px;
  }

  /* @media only screen and (min-width: 1280px) {
    .form-body {
      display: grid;
      grid-template-columns: 1fr 0.5fr 1fr 0.5fr;
      padding: 5px;
    }
  } */

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
    font-size: 1.3rem;
  }

  .row:after {
    content: '';
    display: table;
    clear: both;
  }
</style>
