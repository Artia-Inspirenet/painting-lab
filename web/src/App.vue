<template>
  <div id="app" >
    <p>Your CSRFToken: {{ token }}</p>
    <!--
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Artia Web App"/>
    <PSDFileUpload token=""/>
    -->
    <div
      @dragover.stop.prevent="onDragOver"
      @drop.stop.prevent="onDrop">
    <!--
      <input
        id="file-send"
        type="button"
        class="btn btn-primary"
        autocomplate="off"
        data-loading-text="jquery with bootstrap"
        value="sdfsdf"/>
    -->
      <p>Drop Files Here!</p>
    </div>
  </div>
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'
//import PSDFileUpload from './components/PSDFileUpload.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import jQuery from 'jquery'
import Cookies from 'js-cookie'

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
    //PSDFileUpload
  },
  methods: {

    onDragOver : function (evt) {
      evt.dataTransfer.dropEffect = 'copy';
    },

    onDrop : function (evt) {
      if (evt.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < evt.dataTransfer.items.length; i++) {
          // If dropped items aren't files, reject them
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

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

div div {
  width: 500px;
  height: 100px;
  border: 1px #ababab dashed;
  margin: 50px auto;
}

div div p {
  text-align: center;
  line-height: 100px;
  margin: 0;
  padding: 0;
}

</style>
