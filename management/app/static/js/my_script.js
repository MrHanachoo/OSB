/**
 * Created by med on 4/23/15.
 */

$(document).ready(function () {
    //Define styles for forms
    $('form div div#swift_user input').addClass("form-control");
    $('form div div#swift_pass').addClass("form-control");
    $('form div div textarea').addClass("form-control");
    $('form div div select').addClass("form-control");
    $('form div#swift-submit input').addClass("btn btn-default");




});

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})

/*
 ajax
 */
function check_container_creation_process() {
    var container_name = $('#new_container_name').val();
    //alert(cont)
    $.ajax(
        {
            url: '/account/create/' + container_name,
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    //alert("suscess: container " + container_name + " created");
                    $('#containers_list').append("<li class='active'><a href='/account/"+container_name+"'><table><tbody><tr><td width='70%'><div style='color: #333' id='container_name'>"+container_name+"</div></td><div id='show'><td width='13%'><button style='color: #333' title='upload' class='glyphicon glyphicon-cloud-upload' id='upload_obj' type='file' multiple='true'></button></td><td width='4%'></td><td width='13%'><button style='color: #333' title='delete container' class='glyphicon glyphicon-trash' onclick='check_container_deletion_process()' data-toggle='modal' data-target='#delete-modal'></button></td></div></tr></tbody></table> </a></li>");

                }
                else {
                    alert("failed: container");
                }
            }
        }
    )
}

function check_container_deletion_process(i) {
    var container_name = document.getElementById('container_name_'+i).innerHTML;
    var c = confirm('delete '+container_name+' container?');
    if(c == true){
        $.ajax(
        {
            url: '/account/delete/'+container_name,
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    alert(container_name+' deleted !')
                    window.location="localhost:8081/account/";
                }
            }
            /*
            timeout: 10000,
            success: function (result) {
                if (result.status) {
                    alert("suscess: container " + container_name + " deleted");
                    //$('#containers_list').("<li class='active' data-target='#upload_obj'><a href='/account/'+container_name>" + container_name + "<span id='upload_obj'  class=' btn btn-default btn-xs btn-file'>+ <input type='file'></span><span class='sr-only'>(current)</span></a></li>");

                }
                else {
                    alert("failed: container");
                }
            }*/
        }
    )
         //window.location="localhost:8081/account/";
    }


}

function check_object_deletion_process(object_name){

    var c = confirm('do you really want to delete '+object_name+' ?');
    if(c == true){
        $.ajax(
        {
            url: '/account/'+object_name+'/delete',
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    //alert(object_name+' deleted !')
                    location.reload()
                }
            }
        }
    )}
}

function share_object_process(object_name){
        //var container_name = document.getElementById('container_name_'+i).innerHTML;
        //var object_name = document.getElementById('object_name_'+k).innerHTML;
    c = confirm('Do you really want to generate a temporary URL for '+object_name +'?')
    if (c == true) {
        $.ajax(
            {
                url: '/account/' + object_name + '/share',
                type: 'GET',
                success: function (result) {
                    if (result.status) {
                        alert("Temporary URL:  " +
                        "" + result.status)
                    }
                }
            }
        )
    }
}

function download_object_process(object_name){
        //var container_name = document.getElementById('container_name_'+i).innerHTML;
        //var object_name = document.getElementById('object_name_'+k).innerHTML;
    c = confirm('Do you want to download '+object_name +'?')
    if (c == true) {
        $.ajax(
            {
                url: '/account/' + object_name + '/download',
                type: 'GET',
                success: function (result) {
                    if (result.status) {
                        window.open(result.status, '_blank')
                    }
                }
            }
        )
    }
}


function upload_object_process(i) {
    var container_name = document.getElementById('container_name_'+i).innerHTML;
    alert('upload to : '+container_name )
    //  container_name = 'folder1'
    $.ajax(
        {
            url: '/account/'+container_name+'/upload',
            type: 'POST',
            success: function (result) {
                    if (result.status) {
                        alert(result.status)
                    }
                }
        }
    )
    alert('end of ajax')

}
/*
 function upload_object(){
 var upload = $('#upload_obj').val()
 alert('hhh')
 upload.file({showUpload: true, maxFileCount: 10, mainClass: "input-group-lg"});
 }



 function share_object(){
 var link = $('#object_link').val()
 }



 function update_containers_list_dynamically(){
 var cont_list = $('#containers_list').val()

 }

 */