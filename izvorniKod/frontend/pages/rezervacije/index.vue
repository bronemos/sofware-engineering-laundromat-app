<template class="background">
  <div id="app" data-app app-data="true">
    <div class="background">
      <div class="hero">
        <div class="container emp-profile">
          <client-only>
            <vue-cal ref="vuecal" 
                :time-from="6 * 60" :time-step="60" 
                active-view="day" 
                locale="hr" 
                :disable-views="['years', 'year']" 
                class="vuecal--blue-theme" 
                today-button 
                :selected-date="todayDate" 
                :min-date="minDate" 
                :max-date="maxDate" 
                :hide-weekdays="[7]" 
                :events="events" 
                :split-days="splitDays" 
                :sticky-split-labels="stickySplitLabels" 
                :min-cell-width="minCellWidth" 
                :min-split-width="minSplitWidth" 
                :on-event-click="onEventClick">
              <template v-slot:today-button>
                <!-- Using Vuetify -->
                <v-tooltip>
                  <template v-slot:activator="{ on }">
                    <v-btn v-on="on">
                      <span>Danas</span>
                    </v-btn>
                  </template>
                </v-tooltip>
              </template>
            </vue-cal>
          </client-only>
        </div>
      </div>

      <!-- click on event dialog -->
      <v-dialog v-model="showDialog" width="unset">
        <v-card>
          <v-card-title>
            <v-icon>{{ selectedEvent.icon }}</v-icon>
            <span>{{
                selectedEvent.start && selectedEvent.start.format("DD.MM.YYYY")
              }}
              {{ selectedEvent.label }}</span>
          </v-card-title>

          <!-- reserved appointement -->
          <v-card-text v-if="selectedEvent.class == 'reserved' || selectedEvent.class == 'mine'">
            <span v-if="selectedEvent.user.email != ''"><strong>Email:</strong> {{ selectedEvent.user.email }}<br /></span>
            <span><strong>Plaćanje:</strong> {{ selectedEvent.paid }}</span><br />
            <span><strong>Košara:</strong>
              {{ selectedEvent.basket_taken }}</span><br />
            <span><strong>Cijena:</strong> {{ selectedEvent.price }} kn</span><br />
            <span><strong>Uređaj:</strong> {{ selectedEvent.machine }}</span><br />
            <div v-if="selectedEvent.note != ''">
              <span><strong>Bilješka:</strong></span><br />
              <span>{{ selectedEvent.note }}</span><br />
            </div>
            
            <span v-if="selectedEvent.warning === true"><strong>Ako otkažete termin manje od 3 sata prije početka dobit ćete negativne bodove</strong></span>
            <button 
              @click.prevent="deleteAppointment()" 
              v-if="(user.is_staff || (this.$auth.user.id == user.id && selectedEvent.class == 'mine')) && selectedEvent.past == false" 
              class="btn btn-danger">Obriši
            </button>

            <div v-if="user.is_staff">
              <hr/>
              <span><strong>Pošalji e-mail korisniku:</strong></span>
              <textarea class="form-control" rows="5" id="comment" v-model="selectedEvent.mailText"></textarea>
              <button @click.prevent="sendMail()" class="btn btn-warning">Pošalji</button>
            </div>

            <div v-if="selectedEvent.past === true && selectedEvent.user.id === this.$auth.user.id">
              <hr/>
              <button @click.prevent="terminPropusten()" v-if="user.is_staff && selectedEvent.past == true && selectedEvent.missed === false" class="btn btn-danger">Termin propušten</button><br/>
              <div v-if="selectedEvent.rating == null && user.is_staff == false">
                <strong>Odaberi i pritisni ocjenu za zaposlenika:</strong>
                <select class="custom-select" v-model="selectedEvent.selectedEmployee">
                  <option required v-for="worker in selectedEvent.workers_list" v-bind:key="worker.id" v-bind:value="worker.id">
                    {{ worker.last_name }} {{ worker.first_name }}
                  </option>
                </select>
                <textarea class="form-control" rows="5" id="comment" v-model="selectedEvent.ratingText"></textarea>
                <client-only>
                  <star-rating v-model="selectedEvent.ratingNumber" @rating-selected="setCurrentSelectedRating"></star-rating>
                </client-only>
              </div>
            </div>

            <div v-if="selectedEvent.rating != null">
                <span>{{ selectedEvent.employee[selectedEvent.rating.employee].first_name }}</span><br/>
                <span>{{ selectedEvent.employee[selectedEvent.rating.employee].last_name }}</span><br/>
                <client-only>
                  <star-rating v-model="selectedEvent.rating.grade" read-only></star-rating>
                </client-only>
                <span>{{ selectedEvent.rating.text }}</span><br/>
            </div>
          </v-card-text>

          <!-- free appointement -->
          <v-card-text v-if="selectedEvent.class == 'free'">
            <form id="addAppointment" @submit.prevent="addAppointment">
              <span><strong>Plaćanje: </strong>{{ selectedEvent.price }} kn</span>
              <span v-if="selectedEvent.paid !== true"> na blagajni.</span>
              <span v-if="selectedEvent.paid === true"> putem kartice.</span>
              <br />
              <div class="checkbox">
                <label><input type="checkbox" v-model="selectedEvent.basket_taken" />
                  Posudi košaru</label>
              </div>
              <div class="checkbox" v-if="this.user.card != null">
                <label><input type="checkbox" v-model="selectedEvent.paid" />
                  Kartično plaćanje</label>
              </div>
              <div class="form-group">
                <label for="comment">Bilješka:</label>
                <textarea class="form-control" rows="5" id="comment" v-model="selectedEvent.note"></textarea>
              </div>
              <button type="submit" class="btn btn-success">Rezerviraj</button>
            </form>
          </v-card-text>
        </v-card>
      </v-dialog>

      <!-- loading dialog -->
      <v-dialog v-model="loadingDialog" width="unset" v-if="loadingDialog">
        <v-card>
          <v-card-title class="d-flex justify-content-center">
            <strong>Učitavanje rezervacija....</strong>
          </v-card-title>
          <v-card-text class="d-flex justify-content-center">
            <img src="https://media2.giphy.com/media/10etb2jVqCZYWc/giphy.gif" />
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
export default {
  middleware: "auth",
  data: () => ({
    prices: {
      washing: 0,
      drying: 0,
    },
    appointmentForm: {
      machine: "",
      start: "",
      price: "",
      note: "",
      paid: false,
      basket_taken: false,
      employee: "",
    },
    loadingDialog: true,
    todayDate: new Date(),
    stickySplitLabels: false,
    minCellWidth: 30,
    minSplitWidth: 200,
    selectedEvent: {},
    showDialog: false,
    splitDays: [
      { id: 1, class: "washer", label: "Perilica 1" },
      { id: 2, class: "dryer", label: "Sušilica 1" },
      { id: 3, class: "washer", label: "Perilica 2" },
      { id: 4, class: "dryer", label: "Sušilica 2" },
      { id: 5, class: "washer", label: "Perilica 3" },
      { id: 6, class: "dryer", label: "Sušilica 3" },
      { id: 7, class: "washer", label: "Perilica 4" },
      { id: 8, class: "dryer", label: "Sušilica 4" },
      { id: 9, class: "washer", label: "Perilica 5" },
      { id: 10, class: "dryer", label: "Sušilica 5" },
    ],
    events: [],
  }),

  async fetch() {
    let res = await this.$axios.get(`laundry`); 
    let res2 = await this.$axios.get(`laundry/future_laundry`);

    var laundries = {};
    laundries[res.data.date_changed] = res.data;
    laundries[res.data.date_changed].open_time_value = parseInt(
      res.data.open_time.substring(0, res.data.open_time.length - 6)
    );
    laundries[res.data.date_changed].close_time_value = 
      parseInt(res.data.close_time.substring(0, res.data.close_time.length - 6));
    laundries[res.data.date_changed].pause_start_value = 
      res.data.pause_start.substring(0, res.data.pause_start.length - 3);
    laundries[res.data.date_changed].pause_end_value = 
      res.data.pause_end.substring(0,res.data.close_time.length - 3);

    for (var entry in res2.data) {
      let obj = Object.assign({}, res2.data[entry]);
      if (new Date(obj.date_changed) < new Date().addDays(14)) {
        obj.open_time_value = 
          parseInt(obj.open_time.substring(0, obj.open_time.length - 6));
        obj.close_time_value = 
          parseInt(obj.close_time.substring(0, obj.close_time.length - 6));
        obj.pause_start_value = obj.pause_start.substring(0,obj.pause_start.length - 3);
        obj.pause_end_value = obj.pause_end.substring(0,obj.close_time.length - 3);
        laundries[obj.date_changed] = obj;
      }
    }

    var pause = {
      start: "",
      end: "",
      class: "break",
      title: "PAUZA",
      label: "PAUZA",
      background: true,
    };

    let appointments = await this.$axios.get(`appointment`);
    let workers_list = await this.$axios.get("admin/list_workers");
    let workers = {}
    for(var work in workers_list.data) {
      workers[workers_list.data[work].id] = workers_list.data[work];
    }

    var that = this;
    var reserved = [];
    appointments.data.forEach(function (app) {
      var event = {
        id: app.id,
        user: app.user_obj,
        note: app.note,
        machine: app.title,
        price: app.price,
        paid: app.paid ? "karticom" : "na blagajni",
        basket_taken: app.basket_taken ? "posuđena" : "nije posuđena",
        employee: workers,
        workers_list: workers_list.data,
        missed: app.missed,
        rating: app.review
      };
      event.start = new Date(app.start);
      event.end = new Date(app.end);
      if (that.$auth.user.id == event.user.id) {
        event.class = "mine";
      } else {
        event.class = "reserved";
      }
      event.title = `${event.user.first_name} ${event.user.last_name}`;
      event.label = `${event.start.getHours()}:00 - ${event.end.getHours()}:00`;
      event.split =
        app.machine.id < 5 ? 2 * app.machine.id - 1 : 2 * app.machine.id - 10;
      if (event.end < that.todayDate) {
        event.past = true;
      } else {
        event.past = false;
      }
      that.events.push(event);
      reserved.push(event.split + "" + event.start.toString());
    });

    var last = this.todayDate.addDays(14);

    for(var d = this.todayDate; d < last; d = d.addDays(1)) {
      //  skip sunday
      if(d.getDay() === 0)
        continue;
      
      //  choose most recent work hours
      let laundry = null;
      for (var entry in laundries)
        if (d >= new Date(entry))
          laundry = laundries[entry];
        else 
          break;

      var tmpDate = new Date(d);
      tmpDate.setHours(laundry.open_time_value,0,0,0);
      const toHours = tmpDate.addHours(laundry.close_time_value - laundry.open_time_value);
      for (; tmpDate < toHours; tmpDate = tmpDate.addHours(1)) {
        if (d == this.todayDate && tmpDate.getHours() <= d.getHours()) 
          continue;
        var event = {};
        event.start = tmpDate.toString();
        event.end = tmpDate.addHours(1).toString();
        event.class = "free";
        event.title = `${tmpDate.getHours()}:00 - ${tmpDate.addHours(1).getHours()}:00`;
        event.label = `${tmpDate.getHours()}:00 - ${tmpDate.addHours(1).getHours()}:00`;
        for (var k = 1; k <= 10; k++) {
          if (reserved.includes(k + "" + event.start.toString())) 
            continue;
          let tmp = Object.assign({}, event);
          if (tmpDate.getHours() == parseInt(laundry.pause_start.substring(0, laundry.pause_start.length - 3))) {
            let pauseEvent = Object.assign({}, pause);
            let pauseDate = new Date(d);
            pauseDate.setHours(
              parseInt(laundry.pause_start_value.substring(0, 2)), 
              parseInt(laundry.pause_start_value.substring(3, 5))
            );
            pauseEvent.start = pauseDate.toString();
            pauseDate.setHours(
              parseInt(laundry.pause_end_value.substring(0, 2)), 
              parseInt(laundry.pause_end_value.substring(3, 5))
            );
            pauseEvent.end = pauseDate.toString();
            pauseEvent.split = k;
            this.events.push(pauseEvent);
          }
          tmp.split = k;
          tmp.price = k % 2 ? laundry.wash_price : laundry.drying_price;
          tmp.machine_id = k % 2 ? k / 2 + 0.5 : k / 2 + 5;
          this.events.push(tmp);
        }
      }
    }
    this.loadingDialog = false;
  },
  methods: {
    onEventClick(event, e) {
      if (new Date() > new Date(event.start) && event.class === "free") {
        location.reload();
      }
      if (new Date().addHours(3) >= new Date(event.start) 
            && event.class === "mine" && event.past == false) {
        event.warning = true;
      }
      this.selectedEvent = event;
      this.showDialog = true;
      this.appointmentForm.start = event.start.toISOString();
      this.appointmentForm.end = event.end.toISOString();
      this.appointmentForm.machine = event.machine_id;
      this.appointmentForm.price = event.price;
      this.appointmentForm.user = event.user;
      this.appointmentForm.id = event.id;
      e.stopPropagation();
    },
    async addAppointment() {
      this.showDialog = false;
      try {
        let response = await this.$axios.post(
          "appointment/",
          this.appointmentForm
        );
        this.$toast.show("Zahtjev uspješno poslan, molim pričekajte!", {
          duration: 5000,
        });
        location.reload();
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 5000,
        });
        if (e.response.data) {
          for (let key in e.response.data) {
            if (key == "non_field_errors") {
              let nonFieldErrors = e.response.data[key][0];
              nonFieldErrors = nonFieldErrors.substring(
                1,
                nonFieldErrors.length - 1
              );
              this.$toast.error(`${nonFieldErrors}`, { duration: 5000 });
            } else
              this.$toast.error(`${key}: ${e.response.data[key]}`, {
                duration: 5000,
              });
          }
        }
      }
    },
    async deleteAppointment() {
      this.showDialog = false;
      try {
        let response = await this.$axios.delete(
          "appointment/" + this.selectedEvent.id
        );
        this.$toast.show("Termin otkazan!", {
          duration: 5000,
        });
        location.reload();
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 5000,
        });
        if (e.response.data) {
          for (let key in e.response.data) {
            if (key == "non_field_errors") {
              let nonFieldErrors = e.response.data[key][0];
              nonFieldErrors = nonFieldErrors.substring(
                1,
                nonFieldErrors.length - 1
              );
              this.$toast.error(`${nonFieldErrors}`, { duration: 5000 });
            } else
              this.$toast.error(`${key}: ${e.response.data[key]}`, {
                duration: 5000,
              });
          }
        }
      }
    },
    async setCurrentSelectedRating(rating) {
      this.showDialog = false;
      try {
        let response = await this.$axios.post("review/", {
          grade: rating,
          user: this.user.id,
          employee: this.selectedEvent.selectedEmployee,
          appointment: this.selectedEvent.id,
          text: this.selectedEvent.ratingText
        });
        this.$toast.show("Poslana ocjena za zaposlenika!", {
          duration: 5000,
        });
        location.reload();
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 5000,
        });
        if (e.response.data) {
          for (let key in e.response.data) {
            if (key == "non_field_errors") {
              let nonFieldErrors = e.response.data[key][0];
              nonFieldErrors = nonFieldErrors.substring(
                1,
                nonFieldErrors.length - 1
              );
              this.$toast.error(`${nonFieldErrors}`, { duration: 5000 });
            } else
              this.$toast.error(`${key}: ${e.response.data[key]}`, {
                duration: 5000,
              });
          }
        }
      }
    },
    async terminPropusten() {
       try {
        let response = await this.$axios.get(`appointment/${this.selectedEvent.id}/missed/`);
        this.$toast.show("Poslan propušteni termin!", {
          duration: 5000,
        });
        location.reload();
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 5000,
        });
        if (e.response.data) {
          for (let key in e.response.data) {
            if (key == "non_field_errors") {
              let nonFieldErrors = e.response.data[key][0];
              nonFieldErrors = nonFieldErrors.substring(
                1,
                nonFieldErrors.length - 1
              );
              this.$toast.error(`${nonFieldErrors}`, { duration: 5000 });
            } else
              this.$toast.error(`${key}: ${e.response.data[key]}`, {
                duration: 5000,
              });
          }
        }
      }
    },
    async sendMail() {
       try {
        let response = await this.$axios.post(`appointment/${this.selectedEvent.id}/send_email/`, {text: this.selectedEvent.mailText});
        this.$toast.show("Poslan email korisniku!", {
          duration: 5000,
        });
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 5000,
        });
        if (e.response.data) {
          for (let key in e.response.data) {
            if (key == "non_field_errors") {
              let nonFieldErrors = e.response.data[key][0];
              nonFieldErrors = nonFieldErrors.substring(
                1,
                nonFieldErrors.length - 1
              );
              this.$toast.error(`${nonFieldErrors}`, { duration: 5000 });
            } else
              this.$toast.error(`${key}: ${e.response.data[key]}`, {
                duration: 5000,
              });
          }
        }
      }
    }
  },
  computed: {
    user() {
      if (this.$auth.loggedIn) {
        return this.$auth.user;
      }
      return null;
    },
    minDate() {
      return new Date();
    },
    maxDate() {
      return new Date().addDays(14);
    },
  },
};
</script>

<style lan="scss">
.vuecal__cell-split.washer {
  background-color: rgba(227, 239, 252, 0.5);
}
.vuecal__cell-split.dryer {
  background-color: rgba(238, 252, 241, 0.5);
}
.vuecal__cell-split .split-label {
  color: rgba(0, 0, 0, 0.5);
  font-size: 24px;
}

.vuecal__event.free {
  background-color: rgba(179, 228, 213, 0.9);
  border: 1px solid rgba(162, 202, 190, 0.9);
  color: rgb(0, 0, 0, 0.5);
}
.vuecal__event.reserved {
  background-color: rgba(216, 226, 223, 0.9);
  border: 1px solid rgb(144, 210, 190);
  color: rgb(0, 0, 0, 0.3);
}

.vuecal__event.mine {
  background-color: rgba(173, 192, 235, 0.9);
  border: 1px solid rgb(144, 210, 190);
  color: rgb(0, 0, 0, 0.3);
}

.vuecal__cell--disabled {
  text-decoration: line-through;
}
.vuecal__cell--before-min {
  color: #b6d6c7;
}
.vuecal__cell--after-max {
  color: #008b8b;
}

.vuecal__now-line {
  color: #06c;
  border-bottom: 5px;
}

.vuecal__event {
  cursor: pointer;
}

.vuecal__event-title {
  font-size: 1.2em;
  font-weight: bold;
  margin: 4px 0 8px;
}

.vuecal__event-time {
  display: inline-block;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.vuecal__event-content {
  font-style: italic;
}

.vuecal__event.break {
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    #610606 10px,
    #610606 20px
  ); /* IE 10+ */
  color: rgb(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}
.vuecal__event.break .vuecal__event-time {
  display: none;
  align-items: center;
}
</style>

<style scoped>
button:focus {
  outline: none !important;
}

input:focus {
  outline: none !important;
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

.profile-head h5 {
  color: #333;
}

.profile-head h6 {
  color: #0062cc;
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
</style>
