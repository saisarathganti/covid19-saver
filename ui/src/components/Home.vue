<template>
  <div class="container">
      <div class="row">
        <div class="col-md-6 mt-5 mx-auto">
          <div>
              <h2 v-if="showUpdate"> Corona Infection Update Successful </h2>
          </div>
          <h1 class="text-center">Welcome {{this.username}}</h1>
          <template v-if="noLocation">
            <h2 class="text-center">Enable geolocation to see list of boundaries</h2>
          </template>
          <template v-if="!noLocation">
            <h2 class="text-center">Your location co-ordinates are recorded</h2>
          </template>
          <br>
          <h5>Corona Infected?</h5>
          <label for="yes">
            <input type="radio"
               id="yes"
               value="YES"
               v-model="coronaInfected"> YES
          </label>
          <label for="no">
          <input type="radio"
               id="no"
               value="NO"
               v-model="coronaInfected"> NO
          </label>
          <button class="btn btn-primary"
              @click.prevent="submitted">Submit!
          </button>
          <br>
          <div>
            <br>
            <button class="btn btn-primary"
                @click.prevent="dashboard">Dashboard Login
            </button>
          </div>
          <div>
            <p v-if="statDate">
              <br>
              <b>Latest corona stats of {{this.country}} are:</b>
              <ul>
                  <li>Date: {{this.statDate}}</li>
                  <li>Confirmed positive cases: {{this.statConfirmed}}</li>
                  <li>Deaths: {{this.statDeaths}}</li>
                  <li>Recovered: {{this.statRecovered}}</li>
              </ul>
            </p>
          </div>
          <div>
          <br>
            <button class="btn btn-primary"
                @click.prevent="infectedPeople">Get latest corona stats of my country!
            </button>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '../router'
export default {
  data () {
    return {
      usertoken: '',
      username: '',
      country: '',
      statDate: '',
      statConfirmed: '',
      statDeaths: '',
      statRecovered: '',
      noLocation: true,
      coronaInfected: '',
      showUpdate: false,
      statResponse: []
    }
  },
  beforeMount () {
    this.getBounds()
  },
  methods: {
    async getBounds () {
      try {
        const coordinates = await this.$getLocation({
          enableHighAccuracy: true
        })
        this.noLocation = false
        if (localStorage.getItem('usertoken')) {
          this.usertoken = localStorage.getItem('usertoken')
          axios.post('/users/location', {
            usertoken: this.usertoken,
            latitude: coordinates.lat,
            longitude: coordinates.lng
          }).then((res) => {
            if ('error' in res.data) {
              console.log(res.error)
            } else {
              this.username = res.data.result.username
              this.coronaInfected = res.data.result.coronaInfected
              this.country = res.data.result.country
              console.log(this.country)
            }
          }).catch((err) => {
            console.log(err)
          })
        } else {
          console.log('Usertoken not found in localstorage')
        }
      } catch (error) {
        console.log(error)
        this.noLocation = true
      }
    },
    async submitted () {
      this.showUpdate = true
      axios.post('/users/updateCoronaInfectedStatus', {
        usertoken: this.usertoken,
        coronaInfected: this.coronaInfected
      }).then((res) => {
        if ('error' in res.data) {
          console.log(res.data.error)
        }
      }).catch((err) => {
        console.log(err)
      })
      setTimeout(() => { this.showUpdate = false }, 2000)
    },
    async dashboard () {
      router.push({ name: 'DashboardLogin' })
    },
    async infectedPeople () {
      /* eslint no-eval: 0 */
      let url = 'https://pomber.github.io/covid19/timeseries.json'
      let statCountry = this.country
      let statStatement = 'response.data.' + statCountry + '[response.data.' + statCountry + '.length-1]'
      axios.get(url).then((response) => {
        this.statDate = eval(statStatement).date
        this.statConfirmed = eval(statStatement).confirmed
        this.statDeaths = eval(statStatement).deaths
        this.statRecovered = eval(statStatement).recovered
      }).catch((error) => { console.log(error) })
    }
  }
}
</script>
