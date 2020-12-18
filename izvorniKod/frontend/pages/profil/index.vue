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
                  <button class="nav-link" v-bind:class="tabSelected === 'details' ? 'active' : ''" id="details"
                          @click.prevent="tabSelected='details'; editProfile=false">Detalji
                  </button>
                </li>
                <li class="nav-item">
                  <button class="nav-link" v-bind:class="tabSelected === 'payment' ? 'active' : ''" id="payment"
                          @click.prevent="tabSelected='payment'; editProfile=false">Podaci za plaćanje
                  </button>
                </li>
                <li class="nav-item">
                  <button class="nav-link" v-bind:class="tabSelected === 'reservations' ? 'active' : ''"
                          id="reservations"
                          @click.prevent="tabSelected='reservations'; editProfile=false">Lista rezervacija
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-md-2" v-if="tabSelected === 'details' || tabSelected === 'payment'">
            <input type="button" class="profile-edit-btn" name="btnAddMore"
                   :value="editProfile || (tabSelected === 'payment') && user.card === null ? 'Pohrani' : 'Uredi'"
                   @click.prevent="submitUpdate"/>
          </div>
        </div>
        <div class="row" v-if="!editProfile">
          <div class="col-md-8">
            <div class="tab-content profile-tab" id="myTabContent">
              <div class="tab-pane fade show active" id="details-tab" v-if="tabSelected === 'details'">
                <div class="row">
                  <div class="col-md-4">
                    <label>Username</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.username}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Ime i prezime</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.first_name}} {{user.last_name}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Email</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.email}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>JMBAG</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.JMBAG}}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row" v-if="editProfile">
          <div class="col-md-8">
            <div class="tab-content profile-tab" id="myTabContentEdit">
              <div class="tab-pane fade show active" id="details-tab-edit" v-if="tabSelected === 'details'">
                <div class="row">
                  <div class="col-md-4">
                    <label>Username</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" v-model="username">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Ime i prezime</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.first_name}} {{user.last_name}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Email</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.email}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>JMBAG</label>
                  </div>
                  <div class="col-md-4">
                    <p>{{user.JMBAG}}</p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Nova šifra</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" type="password" v-model="password">
                    <div class="error" v-if="!verifyPw(password) && password.length !== 0">Format lozinke nije valjan
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <label>Potvrdi novu šifru</label>
                  </div>
                  <div class="col-md-4">
                    <input class="input-profile" type="password" v-model="repeatedPassword">
                    <div class="error"
                         v-if="!(password === repeatedPassword) && password.length !== 0 && repeatedPassword.length !== 0">
                      Lozinka nije ista
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row" v-if="tabSelected === 'payment' && !editProfile && user.card !== null">
          <div id="page" class="page">
            <div class="card">
              <div class="chip">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 230 384.4 300.4"
                  width="38"
                  height="70"
                >
                  <path
                    d="M377.2 266.8c0 27.2-22.4 49.6-49.6 49.6H56.4c-27.2 0-49.6-22.4-49.6-49.6V107.6C6.8 80.4 29.2 58 56.4 58H328c27.2 0 49.6 22.4 49.6 49.6v159.2h-.4z"
                    data-original="#FFD66E"
                    data-old_color="#00FF0C"
                    fill="rgb(237,237,237)"
                  />
                  <path
                    d="M327.6 51.2H56.4C25.2 51.2 0 76.8 0 107.6v158.8c0 31.2 25.2 56.8 56.4 56.8H328c31.2 0 56.4-25.2 56.4-56.4V107.6c-.4-30.8-25.6-56.4-56.8-56.4zm-104 86.8c.4 1.2.4 2 .8 2.4 0 0 0 .4.4.4.4.8.8 1.2 1.6 1.6 14 10.8 22.4 27.2 22.4 44.8s-8 34-22.4 44.8l-.4.4-1.2 1.2c0 .4-.4.4-.4.8-.4.4-.4.8-.8 1.6v74h-62.8v-73.2-.8c0-.8-.4-1.2-.4-1.6 0 0 0-.4-.4-.4-.4-.8-.8-1.2-1.6-1.6-14-10.8-22.4-27.2-22.4-44.8s8-34 22.4-44.8l1.6-1.6s0-.4.4-.4c.4-.4.4-1.2.4-1.6V64.8h62.8v72.4c-.4 0 0 .4 0 .8zm147.2 77.6H255.6c4-8.8 6-18.4 6-28.4 0-9.6-2-18.8-5.6-27.2h114.4v55.6h.4zM13.2 160H128c-3.6 8.4-5.6 17.6-5.6 27.2 0 10 2 19.6 6 28.4H13.2V160zm43.2-95.2h90.8V134c-4.4 4-8.4 8-12 12.8h-122V108c0-24 19.2-43.2 43.2-43.2zm-43.2 202v-37.6H136c3.2 4 6.8 8 10.8 11.6V310H56.4c-24-.4-43.2-19.6-43.2-43.2zm314.4 42.8h-90.8v-69.2c4-3.6 7.6-7.2 10.8-11.6h122.8v37.6c.4 24-18.8 43.2-42.8 43.2zm43.2-162.8h-122c-3.2-4.8-7.2-8.8-12-12.8V64.8h90.8c23.6 0 42.8 19.2 42.8 42.8v39.2h.4z"
                    data-original="#005F75"
                    class="active-path"
                    data-old_color="#005F75"
                    fill="rgba(0,0,0,.4)"
                  />
                </svg>

              </div>
              <form class="form-card" action="#">
                <label class="label-card" for="number"
                >Broj kartice
                  <input
                    class="input-card"
                    type="text"
                    id="number"
                    :value="'•••• •••• •••• ' + user.card.cc_number.slice(-4)"
                    disabled
                  />
                </label>
                <label class="label-name label-card" for="name"
                >Ime i prezime
                  <input class="input-card" type="text" id="name" :placeholder="user.first_name + ' ' + user.last_name"
                         disabled/>
                </label>
                <label class="label-date label-card" for="date"
                >Vrijedi do
                  <input class="input-card" type="text" id="date"
                         :value="user.card.cc_expiry.split('-')[1] + '/' + user.card.cc_expiry.split('-')[0].slice(-2)"
                         disabled/>
                </label>
                <label class="label-cvc label-card" for="cvc"
                >CVV
                  <input class="input-card" type="text" id="cvc" value="•••" disabled/>
                </label>
              </form>

            </div>
          </div>
        </div>
        <div class="row" v-if="tabSelected === 'payment' && (editProfile || user.card === null)">
          <div id="page-edit" class="page">
            <div class="card">
              <div class="chip">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 230 384.4 300.4"
                  width="38"
                  height="70"
                >
                  <path
                    d="M377.2 266.8c0 27.2-22.4 49.6-49.6 49.6H56.4c-27.2 0-49.6-22.4-49.6-49.6V107.6C6.8 80.4 29.2 58 56.4 58H328c27.2 0 49.6 22.4 49.6 49.6v159.2h-.4z"
                    data-original="#FFD66E"
                    data-old_color="#00FF0C"
                    fill="rgb(237,237,237)"
                  />
                  <path
                    d="M327.6 51.2H56.4C25.2 51.2 0 76.8 0 107.6v158.8c0 31.2 25.2 56.8 56.4 56.8H328c31.2 0 56.4-25.2 56.4-56.4V107.6c-.4-30.8-25.6-56.4-56.8-56.4zm-104 86.8c.4 1.2.4 2 .8 2.4 0 0 0 .4.4.4.4.8.8 1.2 1.6 1.6 14 10.8 22.4 27.2 22.4 44.8s-8 34-22.4 44.8l-.4.4-1.2 1.2c0 .4-.4.4-.4.8-.4.4-.4.8-.8 1.6v74h-62.8v-73.2-.8c0-.8-.4-1.2-.4-1.6 0 0 0-.4-.4-.4-.4-.8-.8-1.2-1.6-1.6-14-10.8-22.4-27.2-22.4-44.8s8-34 22.4-44.8l1.6-1.6s0-.4.4-.4c.4-.4.4-1.2.4-1.6V64.8h62.8v72.4c-.4 0 0 .4 0 .8zm147.2 77.6H255.6c4-8.8 6-18.4 6-28.4 0-9.6-2-18.8-5.6-27.2h114.4v55.6h.4zM13.2 160H128c-3.6 8.4-5.6 17.6-5.6 27.2 0 10 2 19.6 6 28.4H13.2V160zm43.2-95.2h90.8V134c-4.4 4-8.4 8-12 12.8h-122V108c0-24 19.2-43.2 43.2-43.2zm-43.2 202v-37.6H136c3.2 4 6.8 8 10.8 11.6V310H56.4c-24-.4-43.2-19.6-43.2-43.2zm314.4 42.8h-90.8v-69.2c4-3.6 7.6-7.2 10.8-11.6h122.8v37.6c.4 24-18.8 43.2-42.8 43.2zm43.2-162.8h-122c-3.2-4.8-7.2-8.8-12-12.8V64.8h90.8c23.6 0 42.8 19.2 42.8 42.8v39.2h.4z"
                    data-original="#005F75"
                    class="active-path"
                    data-old_color="#005F75"
                    fill="rgba(0,0,0,.4)"
                  />
                </svg>

              </div>
              <form class="form-card" action="#">
                <label class="label-card" for="number"
                >Broj kartice
                  <input
                    class="input-card"
                    type="text"
                    id="number-edit"
                    placeholder="0000 0000 0000 0000"
                    v-model="cardNumber"
                    v-on:keypress="addCardNumberSpace"
                    maxlength="19"
                  />
                </label>
                <label class="label-name label-card" for="name"
                >Ime i prezime
                  <input class="input-card" type="text" id="name-edit"
                         :value="user.first_name + ' ' + user.last_name" disabled/>
                </label>
                <label class="label-date label-card" for="date"
                >Vrijedi do
                  <input v-on:keypress="addExpirySlash" maxlength="5" class="input-card" type="text" id="date-edit"
                         placeholder="MM/YY" v-model="expiryDate" ref="expDate"/>
                </label>
                <label class="label-cvc label-card" for="cvc"
                >CVV
                  <input class="input-card" type="text" id="cvc-edit" placeholder="000" v-model="cvv" maxlength="3"/>
                </label>
              </form>

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
        tabSelected: 'details',
        editProfile: false,
        password: '',
        repeatedPassword: '',
        username: this.$auth.user.username,
        cardNumber: '',
        cvv: '',
        expiryDate: '',
      }
    },

    computed: {
      user() {
        return this.$auth.user
      },
    },

    methods: {
      addExpirySlash() {
        if (this.expiryDate.length === 2) {
          this.expiryDate = this.expiryDate + '/'
        }
      },
      addCardNumberSpace() {
        if (this.cardNumber.replace(/\s|-/gi, '').length % 4 === 0 && this.cardNumber.length !== 0 && this.cardNumber.length < 19)
          this.cardNumber = this.cardNumber + ' '
      },
      verifyPw(password) {
        const pwRegExp = RegExp('^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$')
        return pwRegExp.test(password)
      },
      verifyCC(cardNumber) {
        const ccRegExp = RegExp('^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$')
        return ccRegExp.test(cardNumber)
      },
      verifyExpiryDate(expiryDate) {
        const expDateRegExp = RegExp('^\\d{2}\\/\\d{2}$')
        if (!expDateRegExp.test(expiryDate))
          return false
        let month = parseInt(expiryDate.split('/')[0], 10) - 1
        if (month < 0 || month > 11)
          return false
        let year = parseInt('20' + expiryDate.split('/')[1], 10)
        let current = new Date()
        if (year < current.getFullYear())
          return false
        else if (year === current.getFullYear() && month < current.getMonth())
          return false
        return true
      },
      async submitUpdate() {
        if (this.tabSelected === 'details') {
          if (!this.editProfile)
            this.editProfile = !this.editProfile
          else {
            let changed = false
            let invalid_pw = false
            let formData = new FormData()
            if (this.username !== this.user.username) {
              formData.append("username", this.username)
              changed = true;
            }
            if (this.password.length || this.repeatedPassword.length) {
              if (!this.verifyPw(this.password) && this.password !== this.repeatedPassword) {
                this.$toast.error('Šifra nije valjana.', {duration: 5000})
                invalid_pw = true;
              } else {
                formData.append("password", this.password);
                changed = true;
              }
            }
            if (changed) {
              try {
                let response = await this.$axios.patch(`account/${this.user.id}/`, formData, {
                  headers: {
                    "Content-Type": "multipart/form-data",
                  },
                })
              } catch (e) {
                this.$toast.error('Username je već u uporabi.', {duration: 5000})
              }
            } else if (!invalid_pw) {
              this.$toast.success('Promjene uspješno pohranjene!', {duration: 5000})
              this.editProfile = !this.editProfile
            }
          }
        } else if (this.tabSelected === 'payment') {
          if (!this.editProfile && this.user.card !== null)
            this.editProfile = !this.editProfile
          else {
            let formData = new FormData();
            let invalid = false
            let cardNumber = this.cardNumber.replace(/\s|-/gi, '')
            if (!this.verifyCC(cardNumber)) {
              this.$toast.error('Neispravan broj kartice!', {duration: 5000})
              invalid = true
            }
            if (this.cvv.length !== 3 || isNaN(this.cvv)) {
              this.$toast.error('Neispravan CVV!', {duration: 5000})
              invalid = true
            }
            if (!this.verifyExpiryDate(this.expiryDate)) {
              this.$toast.error('Neispravan datum isteka!', {duration: 5000})
              invalid = true
            }
            if (!invalid) {
              formData.append('cc_number', cardNumber)
              formData.append('cc_expiry', '20' + this.expiryDate.split('/')[1] + '-' + this.expiryDate.split('/')[0] + '-' + '01')
              formData.append('cc_code', this.cvv)
              try {
                let response;
                if (this.user.card === null){
                  response = await this.$axios.post(`card/`, formData)
                }
                else{
                  response = await this.$axios.patch(`card/${this.user.card.id}/`, formData)
                }
                this.editProfile = false
                this.$store.commit('SET_CARD', response.data)
                this.$toast.success('Podaci uspješno pohranjeni!', {duration: 5000})
              } catch (e) {
                this.$toast.error('Greška pri pohrani podataka!', {duration: 5000})
              }
            }
          }
        }
      }
    }
  }
</script>

<style scoped>
  button:focus {
    outline: none !important;
  }

  input:focus {
    outline: none !important;
  }

  .input-profile {
    width: 40%;
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

  :root {
    --black: #525252;
    --orange: #ffb000;
    --white: #f7fbfc;
    --grey: #c2c2c2;
  }

  .page {
    width: 40%;
    height: 30vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #main {
    width: 41.875rem;
    height: 18.4375rem;
    background-color: black;
    font-family: "Questrial", sans-serif;
    position: relative;
    z-index: 1;
  }

  .card {
    width: 30.5rem;
    height: 17rem;
    background-color: #f7fbfc;
    border-radius: 0.7rem;
    padding: 1.3rem 1.6rem;
    position: relative;
    top: -2.75rem;
    right: 4.4rem;
  }

  /* .card::after {
     content: "";
     display: block;
     width: 17.5rem;
     height: 11rem;
     background-color: #2a2a2a;
     border-radius: 0.7rem;
     position: absolute;
     top: 2.7rem;
     right: -1.5rem;
     transform: rotate(8deg);
     z-index: -1;
   }
 */
  .chip {
    width: 3rem;
    height: 2.2rem;
    margin-bottom: 0.7rem;
  }

  .form-card {
    display: flex;
    flex-wrap: wrap;
    position: relative;
  }

  .label-card {
    width: 100%;
    display: flex;
    flex-direction: column;
    font-size: 1rem;
    color: #c2c2c2;
    margin-top: 0.35rem;
  }

  .label-name {
    width: 72%;
  }

  .label-date {
    width: 22%;
    margin-left: 6%;
  }

  .label-cvc {
    width: 15%;
    position: absolute;
    right: 7%;
    bottom: -3.9rem;
  }

  .label-remember {
    width: auto;
    height: 2.8rem;
    font-size: 1rem;
    position: absolute;
    left: -1rem;
    bottom: -5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row-reverse;
    padding: 10px;
    color: grey
  }

  .input-remember {
    margin-right: .5rem;
    filter: grayscale(100%);
    height: 1rem;
    width: 1rem;
  }

  .input-card {
    border: none;
    border-bottom: 1px solid #c2c2c2;
    outline: none;
    background-color: transparent;
    font-size: 1.1rem;
    padding: 0.2rem 0;
  }

  .button-card {
    height: 2.8rem;
    width: 11.8rem;
    font-size: 0.8rem;
    position: absolute;
    bottom: -10rem;
    left: 10rem;
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .fa-angle-right {
    font-size: 2rem;
    position: absolute;
    left: 72%;
  }

  .price-container {
    position: absolute;
    bottom: 0.6rem;
    left: 3.4rem;
    display: inline-block;
  }

  strong {
    font-size: 2.2rem;
    color: white;
  }

  small {
    font-size: 0.6rem;
    color: #c2c2c2;
  }
</style>
