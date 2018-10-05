<template>
  <div id="psd-file-upload">
    <p>Drop the PSD</p>
    <p>Here is csrftoken: {{ token }}</p>
  </div>
</template>

<script>
export default {
  name: 'PSDFileUpload',
  props: {
    token: String
  },
  method: {
    let uploaded_file = document.getElementById('psd-file-upload');
    //let sendfiles = document.getElementById('sendfiles');
    let formData = new FormData();

    const onDragOver = evt => {
      evt.stopPropagation();
      evt.preventDefault();
      evt.dataTransfer.dropEffect = 'copy';
    }

    const onDrop = evt => {
      evt.stopPropagation();
      evt.preventDefault();

      if (evt.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < evt.dataTransfer.items.length; i++) {
          // If dropped items aren't files, reject them
          if (evt.dataTransfer.items[i].kind === 'file') {
            let file = evt.dataTransfer.items[i].getAsFile();
            formData.append('datafile', file);
          }
        }
      } else {
        // Use DataTransfer interface to access the file(s)
        for (let i = 0; i < evt.dataTransfer.files.length; i++) {
          formData.append('datafile', evt.dataTransfer.files[i]);

        }
      }
      //  $.ajax({
      //    url : 'api/uploads/',
      //    type : 'POST',
      //    data : formData,
      //    processData: false,  // tell jQuery not to process the data
      //    contentType: false,  // tell jQuery not to set contentType
      //    success : data => {
      ////      console.log(data);
      //      alert(data);
      //    }
      //  });
      //  //  PSD.fromEvent(evt).then( (psd) => {
      //    console.log(psd.tree().export());
      //  });
    }

    //const sendFileAjax = () => {
    //}

    uploaded_file.addEventListener('dragover', onDragOver, true);
    uploaded_file.addEventListener('drop', onDrop, true);
    //sendfiles.addEventListener("click", sendFileAjax);
  }
}
</script>

<style>
#psd-file-upload {
  width: 500px;
  height: 100px;
  border: 1px #ababab dashed;
  margin: 50px auto;
}

#psd-file-upload p {
  text-align: center;
  line-height: 100px;
  margin: 0;
  padding: 0;
}
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
