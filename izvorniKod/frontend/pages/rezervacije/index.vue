<template class="background">
  <div id="app" data-app app-data="true">
    <div class="background">
      <div class="hero">
        <div class="container emp-profile">
          <client-only>
            <vue-cal
              ref="vuecal"
              :time-from="6 * 60"
              :time-step="60"
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
              :on-event-click="onEventClick"
            >
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
            <span
              >{{
                selectedEvent.start && selectedEvent.start.format("DD.MM.YYYY")
              }}
              {{ selectedEvent.label }}</span
            >
          </v-card-title>
          <v-card-text v-if="selectedEvent.class == 'reserved'">
            <span><strong>Plaćeno:</strong> {{ selectedEvent.paid }}</span
            ><br />
            <span
              ><strong>Košara posuđena:</strong>
              {{ selectedEvent.basket_taken }}</span
            ><br />
            <span><strong>Cijena:</strong> {{ selectedEvent.price }} kn</span
            ><br />
            <span><strong>Uređaj:</strong> {{ selectedEvent.machine }}</span
            ><br />
            <span><strong>Bilješka:</strong></span
            ><br /><span>{{ selectedEvent.note }}</span>
            <br />
            <button v-if="user.is_staff" class="btn btn-danger">Obriši</button>
          </v-card-text>
          <v-card-text v-if="selectedEvent.class == 'free'">
            <div class="checkbox">
              <label><input type="checkbox" value=""> Košara</label>
            </div>
            <div class="form-group">
              <label for="comment">Comment:</label>
              <textarea class="form-control" rows="5" id="comment"></textarea>
            </div>
            <button class="btn btn-success">Rezerviraj</button>
            <!-- <button class="btn btn-danger">Obriši</button> -->
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
            <img
              src="https://media2.giphy.com/media/10etb2jVqCZYWc/giphy.gif"
            />
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
    var data = res.data;
    let open_time = parseInt(
      data.open_time.substring(0, data.open_time.length - 6)
    );
    let close_time = parseInt(
      data.close_time.substring(0, data.close_time.length - 6)
    );
    let pause_start = data.pause_start.substring(0, data.close_time.length - 3);
    let pause_end = data.pause_end.substring(0, data.close_time.length - 3);

    var pause = {
      start: pause_start + ":00",
      end: pause_end + ":00",
      class: "break",
      title: "PAUZA",
      label: "PAUZA",
      background: true,
    };

    let appointments = await this.$axios.get(`appointment`);
    var that = this;
    appointments.data.forEach(function (app) {
      // var x = arrayItem.prop1 + 2;
      var event = {
        user_id: app.user_id,
        note: app.note,
        machine: app.title,
        price: app.price,
        paid: app.paid ? "DA" : "NE",
        basket_taken: app.basket_taken ? "DA" : "NE",
        employee: app.employee,
      };
      let date = app.start.substring(0, 10);
      let time = parseInt(app.start.substring(11, 13));

      event.start = date + " " + time + ":00";
      event.end = date + " " + (time + 1) + ":00";
      if(that.$auth.user.id == event.user_id){
        event.class = "mine";
      }
      else{
        event.class = "reserved"
      }
      event.title = `${time}:00 - ${time + 1}:00`;
      event.label = `${time}:00 - ${time + 1}:00`;
      if (app.machine.type == "washer") {
        event.split = app.machine.id * 2 - 1;
      } else {
        if (app.machine.id % 2 == 0) {
          event.split = app.machine.id / 2 - 1;
        } else {
          event.split = app.machine.id / 2 + 1;
        }
      }
      that.events.push(event);
    });

    var last = this.todayDate.addDays(14);
    var d = this.todayDate;
    while (d < last) {
      var date = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      for (var j = open_time; j < close_time; j++) {
        if (d == this.todayDate && j <= d.getHours()) continue;

        var event = {};
        event.start = date + " " + j + ":00";
        event.end = date + " " + (j + 1) + ":00";
        event.class = "free";
        event.title = `${j}:00 - ${j + 1}:00`;
        var c = 0;
        event.label = `${j}:00 - ${j + 1}:00`;
        for (var k = 1; k <= 10; k++) {
          let tmp = Object.assign({}, event);

          if (j == parseInt(pause.start.substring(0, pause.start.length - 3))) {
            let pauseEvent = Object.assign({}, pause);
            pauseEvent.start = date + " " + pause.start;
            pauseEvent.split = k;
            pauseEvent.end = date + " " + pause.end;
            this.events.push(pauseEvent);
          }

          this.events.forEach(function (e) {
            if (e.start == event.start && e.split == k) {
              c = 1;
            }
          });
          if (c == 1) {
            c = 0;
            continue;
          }
          tmp.split = k;
          this.events.push(tmp);
        }
      }
      d = d.addDays(1);
    }
    this.loadingDialog = false;
  },

  methods: {
    onEventClick(event, e) {
      this.selectedEvent = event;
      this.showDialog = true;
      e.stopPropagation();
    },
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
  color: rgba(0, 0, 0, 0.1);
  font-size: 26px;
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

.vuecal__event.excange {
  background-color: rgba(252, 248, 197, 0.9);
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
  border-bottom:5px;

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
