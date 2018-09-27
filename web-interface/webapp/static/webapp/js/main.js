//(function () {
  var PSD = require('psd');
//
  document.getElementById('dropzone').addEventListener('dragover', onDragOver, true);
  document.getElementById('dropzone').addEventListener('drop', onDrop, true);
//
  function onDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  }
//
//  function onDrop(e) {
//    e.stopPropagation();
//    e.preventDefault();
//
//    PSD.fromEvent(e).then(function (psd) {
//      var data = JSON.stringify(psd.tree().export(), undefined, 2);
//      document.getElementById('data').innerHTML = data;
//      document.getElementById('image').appendChild(psd.image.toPng());
//    });
//  }
//}());

function onDrop(evt) {
  evt.stopPropagation();
  evt.preventDefault();
  PSD.fromEvent(evt).then(function (psd) {
    console.log(psd.tree().export());
  });
}


