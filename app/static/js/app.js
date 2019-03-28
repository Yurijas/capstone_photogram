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

// ----- pop up comment -----
// function myFunction() {
//   var x = document.getElementById("card-comment");
//   if (x.style.display === "none") {
//     x.style.display = "block";
//   } else {
//     x.style.display = "none";
//   }
// }
// -------------------------------
