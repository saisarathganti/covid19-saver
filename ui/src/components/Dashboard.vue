<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 mt-5 mx-auto">
        <h1 class="text-center">DASHBOARD</h1>
        <div class="form-group">
          <p v-if="coronaInfectedUsernames.length">
            <b>Corona infected usernames around you are:</b>
            <ul>
              <li v-for="username in coronaInfectedUsernames" v-bind:key="username">{{ username }}</li>
            </ul>
          </p>
          <label for="distance">Enter maximum distance to get corona infected users:</label>
          <input type="text" v-model="distance" class="form-control" name="distance" placeholder="Enter distance in KM">
          <br>
          <div>
            <button class="btn btn-primary"
              @click.prevent="getUsersWithDistance">Get corona infected users with distance!
            </button>
          </div>
          <p v-if="coronaExposedUsernames.length">
            <br>
            <b>Corona infected users you got exposed to are:</b>
            <ul>
              <li v-for="username in coronaExposedUsernames" v-bind:key="username">{{ username }}</li>
            </ul>
          </p>
          <div>
            <br>
            <button class="btn btn-primary"
              @click.prevent="exposed">Get corona infected users you got exposed to!
            </button>
          </div>
          <p v-if="statement.length">
            <br>
            <ul>
              <h5 v-for="user in statement" v-bind:key="user">{{ user }}</h5>
            </ul>
          </p>
          <p v-if="canGoUsers.length">
            <ul>
              <li v-for="user in canGoUsers" v-bind:key="user">{{ user }}</li>
            </ul>
          </p>
          <br>
          <label for="latitude">Enter latitude of place you want to visit:</label>
          <input type="text" v-model="latitude" class="form-control" name="latitude" placeholder="Enter latitude">
          <br>
          <label for="longitude">Enter longitude of place you want to visit:</label>
          <input type="text" v-model="longitude" class="form-control" name="longitude" placeholder="Enter longitude">
        </div>
        <div>
        <button class="btn btn-primary"
          @click.prevent="checkLocation">Can i go there!
        </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      usertoken: '',
      distance: '',
      latitude: '',
      longitude: '',
      canGoUsers: [],
      statement: [],
      coronaInfectedUsernames: [],
      coronaExposedUsernames: []
    }
  },
  methods: {
    getUsersWithDistance () {
      if (localStorage.getItem('usertoken')) {
        this.usertoken = localStorage.getItem('usertoken')
      } else {
        console.log('Usertoken not found in localstorage')
      }
      axios.post('/users/getCoronaInfectedUsersWithDistance', {
        usertoken: this.usertoken,
        distance: this.distance
      }).then((res) => {
        if ('error' in res.data) {
          console.log(res.data.error)
        } else {
          if (res.data.length === 0) {
            this.coronaInfectedUsernames = ['No corona infected users found around you']
          } else {
            this.coronaInfectedUsernames = res.data
          }
        }
      }).catch((err) => {
        console.log(err)
      })
    },
    exposed () {
      if (localStorage.getItem('usertoken')) {
        this.usertoken = localStorage.getItem('usertoken')
      } else {
        console.log('Usertoken not found in localstorage')
      }
      axios.post('/users/getCoronaInfectedUsersYouExposedTo', {
        usertoken: this.usertoken,
        latitude: this.latitude,
        longitude: this.longitude
      }).then((res) => {
        if ('error' in res.data) {
          console.log(res.data.error)
        } else {
          console.log(res.data)
          if (res.data.length === 0) {
            this.coronaExposedUsernames = ['You are safe, not exposed to anyone']
          } else {
            this.coronaExposedUsernames = res.data
          }
        }
      }).catch((err) => {
        console.log(err)
      })
    },
    checkLocation () {
      if (localStorage.getItem('usertoken')) {
        this.usertoken = localStorage.getItem('usertoken')
      } else {
        console.log('Usertoken not found in localstorage')
      }
      axios.post('/users/checkLocation', {
        usertoken: this.usertoken,
        latitude: this.latitude,
        longitude: this.longitude
      }).then((res) => {
        if ('error' in res.data) {
          console.log(res.data.error)
        } else {
          console.log(res.data)
          if (res.data.length === 0) {
            this.statement = ['Yes, You can go there']
          } else {
            this.canGoUsers = res.data
            this.statement = ['No, You may get corona due to the following users who visited the place below 4 hours previously:']
            console.log(this.canGoUsers)
          }
        }
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}
</script>
