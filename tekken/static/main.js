// 웹캠 구현


function cameraOn() {
    document.getElementById("camera").style.display = "block"
    document.getElementsByClassName("boxText").display = "none"
    document.getElementsByClassName("web-btn").display = "none"
    navigator.mediaDevices.getUserMedia({ video: true })
}

$(document).ready(function(){ 
    if (!('url' in window) && ('webkitURL' in window)) 
{ window.URL = window.webkitURL; } 
$('#camera').change(function(e){ 
    $('#pic').attr('src', URL.createObjectURL(e.target.files[0])
    ); 
}); 
});





// 드래그앤드랍 부분 //


$('.dropArea')
  .on("dragover", dragOver)

  function dragOver(e){
    e.stopPropagation();
    e.preventDefault();
    if (e.type == "dragover") {  
        $('.dorpArea p').hide(); 
    }  
  }

const dropArea = document.querySelector('.dropArea')
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault()
    e.target.classList.add('over')
    
})
dropArea.addEventListener('dragleave', (e) => {
    e.target.classList.remove('over')

    
})
dropArea.addEventListener('drop', (e) => {
    e.preventDefault()
    e.target.classList.add('drop')
    let file = e.dataTransfer.files[0]
    let fileReader = new FileReader()
    fileReader.onload = (result) => {
        let img = "<img src='" + result.target.result + "' />"
        dropArea.innerHTML = img
    }
    fileReader.readAsDataURL(file)
})


