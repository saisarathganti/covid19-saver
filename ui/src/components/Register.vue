<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 mt-5 mx-auto">
        <form v-on:submit.prevent="register">
          <p v-if="errors.length">
            <b>Please correct the following error(s):</b>
            <ul>
              <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
            </ul>
          </p>
          <h1 class="h3 mb-3 font-weight-normal">Register</h1>
          <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" v-model="email" class="form-control" name="email" placeholder="Enter email">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" v-model="password" class="form-control" name="password" placeholder="Enter Password">
          </div>
          <label for="country">Country</label>
          <select id="country"
            class="form-control"
            v-model="selectedCountry">
            <option v-for="country in countries" v-bind:key="country">{{ country }}</option>
          </select>
          <br>
          <button class="btn btn-lg btn-primary btn-block">Register</button>
        </form>
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
      email: '',
      password: '',
      selectedCountry: 'India',
      countries: ['India', 'US', 'China'],
      errors: []
    }
  },

  methods: {
    register () {
      axios.post('/users/register', {
        email: this.email,
        password: this.password,
        country: this.selectedCountry
      }).then((res) => {
        if ('result' in res.data) {
          console.log(res.data.result)
          router.push({ name: 'Login' })
        } else {
          this.errors.push(res.data.error)
        }
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}

</script>
