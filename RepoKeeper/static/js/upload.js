var fileCache={};
var block=[];
window.onload=function(){
	if(window.File && window.FileList && window.FileReader){
		Init();
	}
}
function Init(){

	var fileselect=document.getElementById("fileselect");
	var filedrag=document.getElementById("filedrag");
	fileselect.addEventListener("change", FileSelectHandler, false);

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
		beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	});
}


function FileDragHover(e){
	e.stopPropagation();
	e.preventDefault();
	e.target.className=(e.type=="dragover"? "hover":"");
}
function FileSelectHandler(e){
	FileDragHover(e);
	var files=e.target.files || e.dataTransfer.files;
	for(var i=0,f;f=files[i];i++){
		fileCache[f.name]=f;
		console.log("file name="+f.name);
		console.log("file size="+f.size);
	}
	console.log("file cacahed="+Object.keys(fileCache).length);

}

function popUp(){
    var upload_form = document.getElementById('pop_upload');
    //upload_form.fadeIn();
    upload_form.style.display = 'block';
}
function fadeOut(){
    var uplaod_form=document.getElementById('pop_upload');
    //uplaod_form.fadeOut();
    uplaod_form.style.display= "none";
}

function MySubmission(evt){//rewrite this function, press to save the data to server
	console.log("start sending...");
	//evt.preventDefault()
	//var xhr=new XMLHttpRequest();
	var formData = new FormData();

	//pop out a dialog, each file have a progress bar
	for(var key in fileCache) {
		console.log("key:" + key);
		console.log("size:" + fileCache[key].size);
		formData.append("upload", fileCache[key]);

		$.ajax({
			xhr: function () {
				var xhr = new window.XMLHttpRequest();
				xhr.upload.addEventListener("progress", function (evt) {
					if (evt.lengthComputable) {
						var percentComplete = evt.loaded / evt.total;
						console.log(evt.total);
						percentComplete = parseInt(percentComplete * 100);
						console.log(percentComplete);

						if (percentComplete === 100) {

						}

					}
				}, false);

				return xhr;
			},
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
}


