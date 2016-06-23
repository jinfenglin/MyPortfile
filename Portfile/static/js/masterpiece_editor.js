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

function TextBlock(){
	/*create elements*/
	var frame=document.createElement('div');
	var container=document.createElement('div');
	var textArea=document.createElement('textarea');

	/*append elements*/
	document.body.appendChild(frame);
	frame.appendChild(container);
	container.appendChild(textArea);

	/*init and set default values*/
	var _this=this;
	this.text="";
	this.textArea_width=$(textArea).width();
	this.textArea_height=$(textArea).height();
	this.container_position=$(container).position();
	this.frame_position=$(frame).position();

	/*set event handler*/
	textArea.addEventListener("keyup",storeText,false);
	textArea.setAttribute('class','moveable-textarea');
	$(container).draggable({cancel:false,
		containment:"parent",
		stop:function(evt,ui){
			_this.container_position=ui.position;
			console.log('container location:'+_this.container_position);
		},
	});
	$(textArea).resizable({
		cancel:false,
		stop:function(evt,ui){
			//_this.frame_width=$(frame).width();
			_this.frame_height=$(frame).height();
			//this.container_width=$(container).width();
			//this.container_height=$(container).height();
			_this.textArea_width=$(textArea).width();
			_this.textArea_height=$(textArea).height();
		},
	});

	/*debug settings*/
	container.style.border='1px solid #F00';
	container.style.display='inline-block';
	frame.style.border='1px solid #F00';
	container.addEventListener('click',function(){
		textArea.focus();
	});
	function storeText(){
		_this.text=textArea.value;
		console.log(_this.text);
	};	
}
TextBlock.createText=function(){
	var instance=new TextBlock();
	block.push(instance);
}
//if single file uploaded, insert it as normal, if multipleones uploaded,create gallary
function VideoBlock(){//create video upload area# show video files  icon in the area
	//provide function to delete the video(mouse or key)
	return null;
}
function ImageBlock(){//create image upload area #show image in place, provide function to delete the image
	return null;
}

function MySubmission(evt){//rewrite this function, press to save the data to server
	console.log("start sending...");
	//evt.preventDefault();
	//var xhr=new XMLHttpRequest();
	var formData = new FormData();

	//pop out a dialog, each file have a progress bar
	for(var key in fileCache){
		console.log("key:"+key);
		console.log("size:"+fileCache[key].size);
		formData.append("upload",fileCache[key]);

		$.ajax({
			xhr: function() {
				var xhr = new window.XMLHttpRequest();
				xhr.upload.addEventListener("progress", function(evt) {
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
			url:'masterpiece_edit',
			type:'POST',
			data:formData,
			success:function(){
				console.log("success submiting files");
			},
			cache: false,
			contentType: false,
			processData: false
		});
	}


}

function test(evt){
	console.log("test:"+block);	
	$.ajax({
		dataType:'JSON',
		url:'masterpiece_detail',
		data:{
			html_element:JSON.stringify(block),
		},
		type:'POST',		
	});	
}

