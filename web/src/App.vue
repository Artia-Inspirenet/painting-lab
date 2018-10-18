<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="/">Artia Wepapp</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="/">Home<span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/api">API</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/api-auth/login/?next=/api/">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/admin/">Admin</a>
          </li>
        </ul>
      </div>
    </nav>
    <PsdFileUpload :csrf-tk=token />
    <InstancePicker />
  </div>
</template>

<script>
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import jQuery from 'jquery'
import Cookies from 'js-cookie'

import PsdFileUpload from './components/PsdFileUpload.vue'
import InstancePicker from './components/InstancePicker.vue'

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
      token: csrftoken,
    }
  },
  components: {
    PsdFileUpload,
    InstancePicker
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
