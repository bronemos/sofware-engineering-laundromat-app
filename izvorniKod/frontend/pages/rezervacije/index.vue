
<template class="background">
  <!-- App.vue -->
  <!-- <div id="app" data-app app-data="true" > -->
    <div class="background">
      <div class="hero">
        <div class="container emp-profile">
          <no-ssr>
            <vue-cal
              ref="vuecal"
              :time-from="6 * 60"
              :time-step="60"
              locale="hr"
              :disable-views="['years', 'year']"
              class="vuecal--blue-theme"
              today-button
              :selected-date="selectedDate"
              :min-date="minDate"
              :max-date="maxDate"
              :hide-weekdays="[7]"
              editable-events
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
          </no-ssr>
        </div>
      </div>
      <!-- Using Vuetify -->
      <v-dialog v-model="showDialog">
        <v-card>
          <v-card-title>
            <v-icon>{{ selectedEvent.icon }}</v-icon>
            <span>{{ selectedEvent.title }}</span>
            <v-spacer/>
            <strong>{{ selectedEvent.start && selectedEvent.start.format('DD/MM/YYYY') }}</strong>
          </v-card-title>
          <v-card-text>
            <p v-html="selectedEvent.contentFull"/>
            <strong>Event details:</strong>
            <ul>
              <li>Event starts at: {{ selectedEvent.start && selectedEvent.start.formatTime() }}</li>
              <li>Event ends at: {{ selectedEvent.end && selectedEvent.end.formatTime() }}</li>
            </ul>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  <!--</div>-->
</template>


<script>
export default {
  data: () => ({
    selectedDate: new Date(new Date().getFullYear(), 11, 31),
    stickySplitLabels: false,
    minCellWidth: 400,
    minSplitWidth: 0,
    selectedEvent: {},
    showDialog: false,
    splitDays: [
      // The id property is added automatically if none (starting from 1), but you can set a custom one.
      // If you need to toggle the splits, you must set the id explicitly.
      { id: 1, class: "washer", label: "washer" },
      { id: 2, class: "dryer", label: "dryer", hide: false }
    ],
    // events: [
    //   {
    //     start: "2020-12-15 14:00",
    //     end: "2020-12-15 18:00",
    //     title: "Need to go shopping",
    //     content: "Click to see my shopping list",
    //     contentFull:
    //       "My shopping list is rather long:<br><ul><li>Avocados</li><li>Tomatoes</li><li>Potatoes</li><li>Mangoes</li></ul>", // Custom attribute.
    //     class: "free",
    //     split: 2
    //   },
    //   {
    //     start: "2020-01-01 12:00",
    //     end: "2020-01-01 13:00",
    //     title: "Pauza",
    //     class: "break",
    //     background: true,
    //     split: 2
    //   }
    // ]
  }),
  methods: {
    onEventClick(event, e) {
      this.selectedEvent = event;
      if (event.class != "break") {
        this.showDialog = true;
      }
      // Prevent navigating to narrower view (default vue-cal behavior).
      e.stopPropagation();
    }
  },
  computed: {
    minDate() {
      return new Date();
    },
    maxDate() {
      return new Date().addDays(30);
    },
    events(){
      var events = [];
      var d = new Date();
      // console.log(d)
      var month = d.addDays(14);
      for (var d; d <= month; d=d.addDays(1)) {
        var date = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
        for (var i = 8; i < 22; i++) {
          var event = {};
          event.start = date + " " + i + ":00";
          event.end = date + " " + (i + 1) + ":00";
          event.split = 1;
          event.class = "free";
          event.title = "radi wu";
          events.push(event);
          var dryer = Object.create(event);
          dryer.split = 2
          events.push(dryer)
        }
      }
      console.log(events);  
      return events;
    }
  }
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
  color: #fff;
}
.vuecal__event.reserved {
  background-color: rgba(164, 230, 210, 0.9);
  border: 1px solid rgb(144, 210, 190);
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
    #f2f2f2 10px,
    #f2f2f2 20px
  ); /* IE 10+ */
  color: #999;
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
