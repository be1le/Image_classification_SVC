// 웹캠 구현


function cameraOn() {
    document.getElementById("camera").style.display = "block";
    document.getElementById("capture").style.display = "block"
    document.getElementById("boxtext").style.display = "None"
    document.getElementById("red-btn").style.display = "None"
    document.getElementById("canvas").style.display = "None"
    document.getElementById("upimg-box").style.display = "None"

    var canvas = document.getElementById("canvas")
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
}

$(document).ready(function() {
    if (!('url' in window) && ('webkitURL' in window)) { window.URL = window.webkitURL; }
    $('#camera').change(function(e) {
        $('#canvas').attr('src', URL.createObjectURL(e.target.files[0]));
    });
});



// function posting2() {
//     let file = $('#file')[0].files[0]
//     let form_data = new FormData()

//     form_data.append("file_give", file)

//     $.ajax({
//         type: "POST",
//         url: "/fileupload",
//         data: form_data,
//         cache: false,
//         contentType: false,
//         processData: false,
//         success: function(response) {
//             alert(response["result"])
//                 // 아래처럼 하지 않아도, 백엔드(app.py)에서 바로 판별 함수를 실행한 뒤에
//                 // render_template 을 해서 바로 결과 페이지로 넘어가도 됨
//             window.location.href = '/result'
//         }
//     });
// }



function posting() {

    const canvas = document.getElementById('canvas');
    const imgBase64 = canvas.toDataURL('image/jpeg', 'image/octet-stream');
    const decodImg = atob(imgBase64.split(',')[1]);

    let array = [];
    for (let i = 0; i < decodImg.length; i++) {
        array.push(decodImg.charCodeAt(i));
    }

    const file = new Blob([new Uint8Array(array)], { type: 'image/jpeg' });
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
        success: function(response) {
            alert(response["result"])
                // 아래처럼 하지 않아도, 백엔드(app.py)에서 바로 판별 함수를 실행한 뒤에
                // render_template 을 해서 바로 결과 페이지로 넘어가도 됨
            window.location.href = '/result'
        }
    });
}

function reset() {
    var canvas = document.getElementById("canvas");
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("camera").style.display = "block"
    document.getElementById("canvas").style.display = "None"
    document.getElementById("capture").style.display = "block"
    document.getElementById("re_capture").style.display = "None"
    document.getElementById("show_result").style.display = "None"

}

function hide_show() {
    document.getElementById("camera").style.display = "None"
    document.getElementById("canvas").style.display = "block"
    document.getElementById("capture").style.display = "None"
    document.getElementById("re_capture").style.display = "block"
    document.getElementById("show_result").style.display = "block"
    var click = new Audio();
    click.src = "../static/Camera.mp3"
    click.currentTime = 0;
    click.volume - 1.0;
    click.play();
}

function all_char() {
    window.location.href = '/char_table'
}

function home() {
    window.location.href = '/'
}

const camera = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capture');

const constraints = {
    video: true,
};

captureButton.addEventListener('click', () => {
    // Draw the video frame to the canvas.
    context.drawImage(camera, 0, 0, canvas.width, canvas.height);
});

// Attach the video stream to the video element and autoplay.
navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
        camera.srcObject = stream;
    });

function load_detail(value) {
    let name = value
    window.location.href = '/char_detail/' + name

}

function enemy(value) {

    let enemy = value
    let name = document.getElementById("exp-title").innerText;


    console.log(enemy)
    console.log(name)

    $.ajax({
        type: 'POST',
        url: '/char_detail/search_vs',
        data: { vs_char_give: enemy, char_give: name },
        success: function(response) {
            let result = response['result']
            console.log(enemy, name, result)

            let temp_html = `
                                <div id="winning-per">
                                <p>${name}</p>
                                <p>${enemy} 상대 승률: ${result}</p>
                                <p id='enemy-title'>${enemy}</p>
                            </div>
                            <div id="winning-box">
                                <div id="pick-img" style="background-image: url(https://tekken.s3.ap-northeast-2.amazonaws.com/Full_Image/${name}.png);">
                                </div>
                                <div id="versus-box">
                                    <p>VS</p>
                                </div>
                                <div id="enemy-img" style="background-image: url(https://tekken.s3.ap-northeast-2.amazonaws.com/Full_Image/${enemy}.png);">
                                </div>
                            </div>
                            `

            $('#temp').html(temp_html)

        }
    });
}





// // 카카오톡 공유하기
// var shareLink = 'localhost:5000/char_result';

// Kakao.Link.createDefaultButton({
//   container: '#kakaoShare',
//   objectType: 'feed',
//   content: {
//     title: '나랑 닮은 철권7 캐릭터',
//     description: '{{name}}',
//     imageUrl: 'https://tekken.s3.ap-northeast-2.amazonaws.com/Full_Image/{{name}}.png',
//     link: {
//       webUrl: localhost:5000,
//       mobileWebUrl: localhost:5000
//     },
//   },
//   buttons: [
//     {
//       title: '웹으로 보기',
//       link: {
//         webUrl: shareLink,
//         mobileWebUrl: shareLink
//       }
//     },
//     {
//       title: '앱으로 보기',
//       link: {
//         webUrl: shareLink,
//         mobileWebUrl: shareLink
//       }
//     }
//   ]
// });


$('div.dropArea')
    .on("dragover", dragOver)
    .on("dragleave", dragOver)
    .on("drop", uploadFiles);

function dragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    if (e.type == "dragleave") {
        $('#camera').hide();
        $('#canvas').hide();
        $('#boxtext').hide();
        $('#upimg-box').hide();

    }
}

function uploadFiles(e) {
    e.stopPropagation();
    e.preventDefault();
    dragOver(e);

    e.dataTransfer = e.originalEvent.dataTransfer;
    var files = e.target.files || e.dataTransfer.files;
    if (files.length > 1) {
        alert('하나의 이미지만 업로드해주세요.');
        return;
    }

    let Image = files[0]
    
    if (Image.type.match(/image.*/ || /video.*/)) {
        document.getElementById("re_capture").style.display = "block"
        document.getElementById("show_result").style.display = "block"
        $(e.target).css({
            "background-image": "url(" + window.URL.createObjectURL(Image) + ")",
            "background-position": "center",
            "background-size": "cover",
            "display": "absolute",
            "max-width": "400px",
            "width": "100%",

        });
        $('div.dropArea').css({
            "object-fit": "cover",
            "width": "400px",
            "height": "300px",
            "display": "block",
            "align-items": "center",
            "border": "2px solid white",
            "border-radius": "50px",
        })

    } else {
        $('#camera').show();
        $('#canvas').show();
        $('#boxtext').show();
        $('#upimg-box').show();
        alert('지원하는 파일이 아닙니다.');
        return;
    }

    
    let form_data = new FormData()

    form_data.append("file_give", Image)

    $.ajax({
        type: "POST",
        url: "/fileupload",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            alert(response["result"])

            window.location.href = '/result'
        }
    });


}


$(function() {
    $("#up-load").on('change', function() {
        readURL(this);
    });
});

function readURL(input) {

    let Image = input.files[0]
    let form_data = new FormData()

    form_data.append("file_give", Image)

    $.ajax({
        type: "POST",
        url: "/fileupload",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            alert(response["result"])

            window.location.href = '/result'
        }
    });

}

  