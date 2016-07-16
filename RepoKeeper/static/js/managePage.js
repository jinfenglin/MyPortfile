/**
 * Created by jinfenglin on 7/4/16.
 */

function createRecourseEntry(file) {
    div = document.createElement('div')
    icon = "<div class='col-xs-8'><span class='glyphicon glyphicon-file'>" + getFileName(file.fields.file) + "</span></div>";
    operationBar = '<div class="col-xs-4"> <span class="glyphicon glyphicon-trash"></span></div>'
    div.innerHTML = '<div class="list-group-item row">' + icon + operationBar + '</div>'
    return div.firstChild
}

/**
 * get the file with type given in parameter. Return files in a list
 * @param type
 */
function getTypeFile(file_list, file_type) {
    var container = $('#resList')
    container.empty()
    var type_list = [];
    file_list.forEach(function (file) {
        if (file.fields.media_type == file_type || file_type == "ALL")
            type_list.push(file)
    })
    insertEntryInContainer(type_list, container)
}
function getFileName(path){
    return path.split('/').pop()
}
function insertEntryInContainer(file_list, container) {
    file_list.forEach(function (file) {
        var res_row = createRecourseEntry(file);
        container.append(res_row)
    })
}