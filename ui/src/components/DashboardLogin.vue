<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <form v-on:submit.prevent="login">
                    <p v-if="errors.length">
                      <b>Please correct the following error(s):</b>
                      <ul>
                        <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
                      </ul>
                    </p>
                    <h1 class="h3 mb-3 font-weight-normal">Please Enter Dashboard Password</h1>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" v-model.lazy="password" class="form-control" name="password" placeholder="Enter Password">
                    </div>
                    <button class="btn btn-lg btn-primary btn-block">Login to Dashboard</button>
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
      usertoken: '',
      password: '',
      errors: []
    }
  },

  methods: {
    login () {
      if (localStorage.getItem('usertoken')) {
        this.usertoken = localStorage.getItem('usertoken')
      } else {
        console.log('Usertoken not found in localstorage')
      }
      axios.post('/users/dashboardlogin', {
        usertoken: this.usertoken,
        password: this.password
      }).then((res) => {
        if ('error' in res.data) {
          this.errors.push(res.data.error)
        } else {
          router.push({ name: 'Dashboard' })
        }
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}

</script>
