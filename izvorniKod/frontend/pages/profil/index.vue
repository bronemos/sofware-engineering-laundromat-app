<template>
  <div class="hero">
    <div class="container emp-profile">
      <form>
        <div class="row">
          <div class="col-md-6">
            <div class="profile-head">
              <h5>
                {{user.first_name}} {{user.last_name}}
              </h5>
              <ul class="nav nav-tabs" id="myTab">
                <li class="nav-item">
                  <button class="nav-link" v-bind:class="detailsSelected ? 'active' : ''" id="details" @click.prevent="detailsSelected=true">Detalji</button>
                </li>
                <li class="nav-item">
                  <button class="nav-link" v-bind:class="!detailsSelected ? 'active' : ''" id="reservations" @click.prevent="detailsSelected=false">Lista rezervacija</button>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-md-2">
            <input type="submit" class="profile-edit-btn" name="btnAddMore" value="Edit Profile"/>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <div class="tab-content profile-tab" id="myTabContent">
              <div class="tab-pane fade show active" id="details-tab" v-if="detailsSelected">
                <div class="row">
                  <div class="col-md-6">
                    <label>Username</label>
                  </div>
                  <div class="col-md-6">
                    <p>{{user.username}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <label>Ime i prezime</label>
                  </div>
                  <div class="col-md-6">
                    <p>{{user.first_name}} {{user.last_name}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <label>Email</label>
                  </div>
                  <div class="col-md-6">
                    <p>{{user.email}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <label>Datum rođenja</label>
                  </div>
                  <div class="col-md-6">
                    <p>{{user.birth_date}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <label>JMBAG</label>
                  </div>
                  <div class="col-md-6">
                    <p>{{user.JMBAG}}</p>
                  </div>
                </div>
              </div>
              <div class="tab-pane fade" id="reservations-tab" v-else>
                abcdef
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
    middleware: 'auth',

    data() {
      return {
        detailsSelected: true
      }
    },

    computed: {
      user() {
        return this.$auth.user
      }
    }
  }
</script>

<style scoped>
  button:focus {
    outline: none !important;
  }

  .hero {
    height: 100%;
    width: 100%;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
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
    transition: .5s;
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
</style>
