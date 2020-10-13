import Vue from 'vue'
import App from './App'
import router from './router'
import VueGeolocation from 'vue-browser-geolocation'
require('../node_modules/bootstrap/dist/css/bootstrap.css')

Vue.config.productionTip = false
Vue.use(VueGeolocation)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
