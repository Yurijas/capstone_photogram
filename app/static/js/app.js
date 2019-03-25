// ----- image uploader -----
window.UPLOADCARE_PUBLIC_KEY = '4946b69592876e878d98'
UPLOADCARE_TABS = 'file url';
UPLOADCARE_CLEARABLE = true;
UPLOADCARE_IMAGE_SHRINK = '200x200';
UPLOADCARE_IMAGES_ONLY = true;

uploadcare.registerTab('preview', uploadcareTabEffects);

const widget = uploadcare.Widget('[role=uploadcare-uploader]');

let images = []

widget.onUploadComplete(function(info) {
  saveImage(info.cdnUrl).then(() => {
    $('#uploadedImage').parent().html('<a href="javascript:refreshPage()">Refresh it!</a>')
  })
})


fetchImages().then(uploadedImages => {
  images = uploadedImages

  const imageHtml = images.reduce((html, url) => {
    const fullUrl = `${url}/-/preview/-/scale_crop/200x200/`

    return (
      html +
      '<div class="col" >' +
      '<a href="#" class="d-block mb-4 h-100">' +
      `<img class="img-fluid img-thumbnail" src="${fullUrl}">` +
      '</a>' +
      '</div>'
    )
  }, '')

  $(imageHtml).appendTo('#imagesContainer')
})

function fetchImages() {
  return new Promise(resolve => {
    const images = JSON.parse(localStorage.getItem('images') || '[]')

    setTimeout(() => resolve(images), 500)
  })
}

function saveImage(url) {
  return new Promise(resolve => {
    images.push(url)
    localStorage.setItem('images', JSON.stringify(images))
    setTimeout(() => resolve(), 500)
  })
}

function refreshPage() {
  window.location.href = window.location.href
}

// ----- ends image uploader -----


// ----- starts profile pic upload -----
window.addEventListener("dragover", function(e) {
  e = e || event;
  e.preventDefault();
}, false);
window.addEventListener("drop", function(e) {
  e = e || event;
  e.preventDefault();
}, false);

$('#dropzone')
  .on('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    var url = e.originalEvent.dataTransfer.getData('url');
    $('#result').attr("src", url);
  });
// ----- ends profile pic upload -----
