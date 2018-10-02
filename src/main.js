// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import Vuetify from 'vuetify'
import('vuetify/dist/vuetify.min.css')
import('@mdi/font/css/materialdesignicons.min.css')

Vue.config.productionTip = false

Vue.use(Vuetify)

const vueConfig = require('vue-config')
const defConfig = require('./config/defaults.js')
const envConfig = require(`./config/${process.env.NODE_ENV}`)
const config = Object.assign({}, defConfig, envConfig)
config.compile()
Vue.use(vueConfig, config)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
