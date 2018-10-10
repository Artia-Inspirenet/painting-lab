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
            <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
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
    <!--
    <p>Your CSRFToken: {{ token }}</p>
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Artia Web App"/>
    <div
      class="drop-zone"
      @dragover.stop.prevent="onDragOver"
      @drop.stop.prevent="onDrop">
      <input
        id="file-send"
        type="button"
        class="btn btn-primary"
        autocomplate="off"
        data-loading-text="jquery with bootstrap"
        value="sdfsdf"/>
      <p>Drop Files Here!</p>
    </div>
    -->
    <PsdFileUpload
      :csrf-tk=token />
  </div>
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import jQuery from 'jquery'
import Cookies from 'js-cookie'

import PsdFileUpload from './components/PsdFileUpload.vue'

let csrftoken = Cookies.get('csrftoken');
let formData = new FormData();

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
      formData: formData,
    }
  },
  components: {
    //HelloWorld
    PsdFileUpload
  },
  methods: {

    onDragOver : function (evt) {
      evt.dataTransfer.dropEffect = 'copy';
    },

    onDrop : function (evt) {
      if (evt.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < evt.dataTransfer.items.length; i++) {
          // If dropped items are't files, reject them
          if (evt.dataTransfer.items[i].kind === 'file') {
            let file = evt.dataTransfer.items[i].getAsFile();
            this.formData.append('datafile', file);
          }
        }
      } else {
        // Use DataTransfer interface to access the file(s)
        for (let i = 0; i < evt.dataTransfer.files.length; i++) {
          formData.append('datafile', evt.dataTransfer.files[i]);
        }
      }
      jQuery.ajax({
        url : 'api/uploads/',
        type : 'POST',
        data : this.formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function () {
          alert("success!");
        }
      })
    }
  }
}
</script>

<style scoped>
/*
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
*/
</style>
