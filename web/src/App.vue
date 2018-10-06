<template>
  <div id="app">
    <p>Your CSRFToken: {{ token }}</p>
    <button type="button" class="btn btn-primary" autocomplate="off" data-loading-text="jquery with bootstrap" @click="clickBtn"></button>
    <br>
    <img alt="Vue logo" src="./assets/logo.png">
    <!--
    <HelloWorld msg="Welcome to Your Artia Web App"/>
    <PSDFileUpload token=""/>
    -->
  </div>
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'
//import PSDFileUpload from './components/PSDFileUpload.vue'

import Cookies from 'js-cookie'

let csrftoken = Cookies.get('csrftoken');


const csrfSafeMethod = method => {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

jQuery.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
})

export default {
  name: 'app',
  data: function () {
    return {
      token: csrftoken
    }
  },
  components: {
    //HelloWorld
    //PSDFileUpload
  },
  methods: {
    clickBtn (event) {
      $(event.target).button('loading')
      setTimeout(function() {
        $(event.target).button('reset')
      }, 1000);
    }
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
