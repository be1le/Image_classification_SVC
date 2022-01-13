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


function posting2() {
    let file = $('#file')[0].files[0]
    let form_data = new FormData()

    form_data.append("file_give", file)

    $.ajax({
        type: "POST",
        url: "/fileupload",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["result"])
            // 아래처럼 하지 않아도, 백엔드(app.py)에서 바로 판별 함수를 실행한 뒤에
            // render_template 을 해서 바로 결과 페이지로 넘어가도 됨
            window.location.href='/result'
        }
    });
  }



function posting() {

  const canvas = document.getElementById('canvas');
  const imgBase64 = canvas.toDataURL('image/jpeg', 'image/octet-stream');
  const decodImg = atob(imgBase64.split(',')[1]);

  let array = [];
  for (let i = 0; i < decodImg .length; i++) {
    array.push(decodImg .charCodeAt(i));
  }

  const file = new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
  const fileName = 'canvas_img_' + new Date().getMilliseconds() + '.jpg';
  let formData = new FormData();
  formData.append('file_give', file, fileName);

    $.ajax({
      type: "POST",
      url: "/fileupload",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        alert(response["result"])
        // 아래처럼 하지 않아도, 백엔드(app.py)에서 바로 판별 함수를 실행한 뒤에
        // render_template 을 해서 바로 결과 페이지로 넘어가도 됨
        window.location.href = '/result'
      }
    });
  }

