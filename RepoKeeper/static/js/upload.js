window.onload = function () {
    if (window.File && window.FileList && window.FileReader) {
        Init();
    }
}
function Init() {

    var fileselect = document.getElementById("fileselect");
    var filedrag = document.getElementById("filedrag");
    fileselect.addEventListener("change", FileSelectHandler, false);

    //if clickoutside the pop_upload window, close the pop_up
    $('#overlay').on('click', function (event) {
        if (event.target != $('#pop_upload').get(0) & $.inArray(event.target, $('#pop_upload').children()) == -1) {
            fadeOut();
        }
    })

    var xhr = new XMLHttpRequest();
    if (xhr.upload) {
        // file drop
        filedrag.addEventListener("dragover", FileDragHover, false);
        filedrag.addEventListener("dragleave", FileDragHover, false);
        filedrag.addEventListener("drop", FileSelectHandler, false);
        filedrag.style.display = "block";
    }


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
}


function FileDragHover(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    //evt.target.className = (evt.type == "dragover" ? "hover" : "");
}

function createEntry(file) {
    div = document.createElement('div');
    icon = "<div class='col-xs-4'><span class='glyphicon glyphicon-file'>"+file.name+"</span></div>";
    progressBar = '<div class="col-xs-4"><div class="progress"> <div class="progress-bar progress-bar-striped" role="progressbar" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"> </div></div></div>';
    operationBar= '<div class="col-xs-4"> <span class="glyphicon glyphicon-trash"></span></div>'
    div.innerHTML='<div class="row">'+icon+progressBar+operationBar+'</div>';
    return div.firstChild;
}

function FileSelectHandler(evt) {
    FileDragHover(evt);
    var files = evt.target.files || evt.dataTransfer.files;
    var entries=[];
    for (var i = 0, f; f = files[i]; i++) {
        entry = createEntry(f)
        $('#filedrag').append(entry);
        uploadFiles(f, $(entry).find('.progress-bar'))
    }
}

function popUp() {
    $('#overlay').fadeIn();
}
function fadeOut() {
    $('#overlay').fadeOut();
}

//upload a single file a time and update the progress bar
function uploadFiles(file, progressBar) {
    console.log("start sending...");
    var formData = new FormData();
    formData.append("upload", file);
    $.ajax({
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    console.log(evt.total);
                    percentComplete = parseInt(percentComplete * 100);
                    $(progressBar).css('width', percentComplete + '%');
                    console.log(percentComplete);
                }
            }, false);
            return xhr;
        },
        async: true,
        url: 'uploadPage',
        type: 'POST',
        data: formData,
        success: function (data) {
            console.log(data);
        },
        cache: false,
        contentType: false,
        processData: false
    });

}


