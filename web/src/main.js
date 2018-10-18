import Vue from 'vue'
import Vuex from 'vuex'
import VueKonva from 'vue-konva'
import axios from 'axios'

import App from './App.vue'

Vue.use(Vuex)
Vue.use(VueKonva)
Vue.config.productionTip = false
Vue.prototype.$http = axios

Vue.filter('formatSize', function (size) {
  if (size > 1024 * 1024 * 1024 * 1024) {
    return (size / 1024 / 1024 / 1024 / 1024).toFixed(2) + ' TB'
  } else if (size > 1024 * 1024 * 1024) {
    return (size / 1024 / 1024 / 1024).toFixed(2) + ' GB'
  } else if (size > 1024 * 1024) {
    return (size / 1024 / 1024).toFixed(2) + ' MB'
  } else if (size > 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  }
  return size.toString() + ' B'
})

const store = new Vuex.Store({
  state: {
    chapter: 0
  },
  mutations: {
  }
})

new Vue({
  render: h => h(App),
  store
}).$mount('#app')
