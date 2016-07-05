/**
 * Created by jinfenglin on 7/4/16.
 */

function createRecourseEntry(fileName){
    div = document.createElement('div')
    icon = "<div class='col-xs-8'><span class='glyphicon glyphicon-file'>"+fileName+"</span></div>";
    operationBar= '<div class="col-xs-4"> <span class="glyphicon glyphicon-trash"></span></div>'
    div.innerHTML='<div class="list-group-item row">'+icon+operationBar+'</div>>'
    return div.firstChild
}