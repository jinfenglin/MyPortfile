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
	var _this=this;
	this.text="";
	this.width="200px";

	/*create elements*/
	var frame=document.createElement('div');
	var container=document.createElement('div');
	var textArea=document.createElement('textarea');
	textArea.style.width=this.width;
	textArea.style.height=this.height;

	/*append elements*/
	document.body.appendChild(frame);
	frame.appendChild(container);
	container.appendChild(textArea);

	/*set event handler*/
	textArea.addEventListener("keyup",this.storeText,false);
	textArea.setAttribute('class','moveable-textarea');
	$(container).draggable({cancel:false,containment:"parent"});
	$(textArea).resizable({cancel:false});

	/*debug settings*/
	container.style.border='1px solid #F00';
	container.style.display='inline-block';
	frame.style.border='1px solid #F00';
	container.addEventListener('click',function(){
		textArea.focus();
	});
	this.storeText=function(){
		this.text=textArea.value;
		console.log('here');
	};	
}
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
	var xhr=new XMLHttpRequest();
	var formData = new FormData();
	for(var key in fileCache){
		console.log("key:"+key);
		console.log("size:"+fileCache[key].size());
		formData.append("upload",fileCache[key]);
		formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
		xhr.open("POST","masterpiece_edit",true);
		xhr.send(formData);
	}
}

function test(evt){
	console.log("test:"+block[0]);	
	$.ajax({
		url:'masterpiece_detail',
		data:{
			html_element:JSON.stringify(block[0]),
		},
		type:'POST',		
	});	
}
	
