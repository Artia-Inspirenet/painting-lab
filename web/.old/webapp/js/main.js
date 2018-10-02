//  init
//  let PSD = require('psd');
let uploaded_file = document.getElementById('dropzone');
let sendfiles = document.getElementById('sendfiles');
let formData = new FormData();
let csrftoken = Cookies.get('csrftoken');


const csrfSafeMethod = method => {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    console.log(this);
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    };
  }
});

const onDragOver = evt => {
  console.log('File(s) is being dragged over');
  evt.stopPropagation();
  evt.preventDefault();
  evt.dataTransfer.dropEffect = 'copy';
}

const onDrop = evt => {
  console.log('File(s) dropped');
  evt.stopPropagation();
  evt.preventDefault();

  if (evt.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < evt.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (evt.dataTransfer.items[i].kind === 'file') {
        let file = evt.dataTransfer.items[i].getAsFile();
        formData.append('datafile', file);
        console.log('... file[' + i + '].name = ' + file.name);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < evt.dataTransfer.files.length; i++) {
      console.log('... file[' + i + '].name = ' + evt.dataTransfer.files[i].name);
      formData.append('datafile', evt.dataTransfer.files[i]);

    }
  }
  $.ajax({
    url : 'api/uploads/',
    type : 'POST',
    data : formData,
    processData: false,  // tell jQuery not to process the data
    contentType: false,  // tell jQuery not to set contentType
    success : data => {
      console.log(data);
      alert(data);
    }
  });
  //  PSD.fromEvent(evt).then( (psd) => {
  //    console.log(psd.tree().export());
  //  });
}

const sendFileAjax = () => {
}

uploaded_file.addEventListener('dragover', onDragOver, true);
uploaded_file.addEventListener('drop', onDrop, true);
sendfiles.addEventListener("click", sendFileAjax);
