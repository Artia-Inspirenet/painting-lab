var PSD = require('psd');

document.getElementById('dropzone').addEventListener('dragover', onDragOver, true);
document.getElementById('dropzone').addEventListener('drop', onDrop, true);

function onDragOver(evt) {
  evt.stopPropagation();
  evt.preventDefault();
  evt.dataTransfer.dropEffect = 'copy';
}

function onDrop(evt) {
  evt.stopPropagation();
  evt.preventDefault();
  PSD.fromEvent(evt).then(function (psd) {
    console.log(psd.tree().export());
  });
}

var formData = new FormData();
formData.append('file', $('#file')[0].files[0]);

$.ajax({
  url : 'api/',
  type : 'POST',
  data : formData,
  processData: false,  // tell jQuery not to process the data
  contentType: false,  // tell jQuery not to set contentType
  success : function(data) {
    console.log(data);
    alert(data);
  }
});
