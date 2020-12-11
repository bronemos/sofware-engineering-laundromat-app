<template class="background">
  <div class="background">
    <div class="hero">
      <div class="container emp-profile">
        <no-ssr>
          <vue-cal
            :time-from="8 * 60"
            :time-step="60"
            locale="hr"
            :disable-views="['years', 'year', 'month']"
            class="vuecal--blue-theme"
            editable-events
            :events="events"
            :split-days="splitDays"
            :sticky-split-labels="stickySplitLabels"
            :min-cell-width="minCellWidth"
            :min-split-width="minSplitWidth"
          />
        </no-ssr>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    stickySplitLabels: false,
    minCellWidth: 400,
    minSplitWidth: 0,
    splitDays: [
      // The id property is added automatically if none (starting from 1), but you can set a custom one.
      // If you need to toggle the splits, you must set the id explicitly.
      { id: 1, class: "mom", label: "Mom" },
      { id: 2, class: "dad", label: "Dad", hide: false },
      { id: 3, class: "kid1", label: "Kid 1" },
      { id: 4, class: "kid2", label: "Kid 2" },
      { id: 5, class: "kid3", label: "Kid 3" },
    ],
    events: [
      {
        start: "2020-12-7 10:35",
        end: "2020-12-7 15:30",
        title: "Doctor appointment",
        class: "health",
        split: 1, // Has to match the id of the split you have set (or integers if none).
      },
    ],
  }),
};
</script>

<style lan="scss">
.vuecal__cell-split.dad {background-color: rgba(221, 238, 255, 0.5);}
.vuecal__cell-split.mom {background-color: rgba(255, 232, 251, 0.5);}
.vuecal__cell-split.kid1 {background-color: rgba(221, 255, 239, 0.5);}
.vuecal__cell-split.kid2 {background-color: rgba(255, 250, 196, 0.5);}
.vuecal__cell-split.kid3 {background-color: rgba(255, 206, 178, 0.5);}
.vuecal__cell-split .split-label {color: rgba(0, 0, 0, 0.1);font-size: 26px;}

.vuecal__event.leisure {background-color: rgba(253, 156, 66, 0.9);border: 1px solid rgb(233, 136, 46);color: #fff;}
.vuecal__event.health {background-color: rgba(164, 230, 210, 0.9);border: 1px solid rgb(144, 210, 190);}
.vuecal__event.sport {background-color: rgba(255, 102, 102, 0.9);border: 1px solid rgb(235, 82, 82);color: #fff;}
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
