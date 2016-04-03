var fileCache={};
function createTextInput(){
	var newText=document.createElement("input");
	var hinter=document.getElementById("hinter");
	var br= document.createElement("br");
	//newText=newText.appendChild(br);
	newText.type="text";
	last=document.body.lastChild;
	hinter.innerHTML=last.innerHTML;
	document.body.insertBefore(newText,last);
	document.body.insertBefore(br,last);	
	//document.body.appendChild(newText);
}
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
function MySubmission(evt){
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
	
