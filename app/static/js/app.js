// ----- modal posted-pic -----
function enlargeImage() {
  document.getElementById("img01").src = this.src;
  document.getElementById('myModal').style.display = "block";
}
(function() {
  var images = document.getElementsByClassName("posted-pic");
  for (i = 0; i < images.length; i++) {
    images[i].onclick = enlargeImage;
  }
})();
// -------------------------------

// ----- drag and drop image -----
// var dragHandler = function(evt){
//   evt.preventDefault();
//   };
// var dropHandler = function(evt){
//     evt.preventDefault();
//     var files = evt.originalEvent.dataTransfer.files;
//     console.log(files[0]);
// };
// var dropHandlerSet = {
//     dragover: dragHandler,
//     drop: dropHandler
// };
// $(".droparea").on(dropHandlerSet);
// -------------------------------

// ----- starts profile pic upload -----
// window.addEventListener("dragover", function(e) {
//   e = e || event;
//   e.preventDefault();
// }, false);
// window.addEventListener("drop", function(e) {
//   e = e || event;
//   e.preventDefault();
// }, false);
//
// $('#dropzone')
//   .on('drop', function(e) {
//     e.stopPropagation();
//     e.preventDefault();
//     var url = e.originalEvent.dataTransfer.getData('url');
//     $('#result').attr("src", url);
//   });
// ----- ends profile pic upload -----
