<template>
  <div id="app">
      <!--
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Artia Web App"/>
      -->
    <PSDFileUpload token=""/>
  </div>
</template>

<script>
import PSDFileUpload from './components/PSDFileUpload.vue'

export default {
  name: 'app',
  components: {
    PSDFileUpload
  }
}

// let csrftoken = Cookies.get('csrftoken');
// 
// 
// const csrfSafeMethod = method => {
//   // these HTTP methods do not require CSRF protection
//   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
// 
// $.ajaxSetup({
//   beforeSend: function (xhr, settings) {
//     console.log(this);
//     if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//       xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     };
//   }
// });
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
