import Vue from 'vue'
import Router from 'vue-router'
import Plebeians from '@/components/Plebeians'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Plebeians',
      component: Plebeians
    }
  ]
})
