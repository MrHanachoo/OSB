/**
 * Created by med on 4/23/15.
 */


function searchFunc(ev, val) {
if (ev.keyCode == 13) {
    window.open("localhost:8081/account1?val="+val);
    }
}




$(document).ready(function () {
    //Define styles for forms
    $('form div div#swift_user input').addClass("form-control");
    $('form div div#swift_pass').addClass("form-control");
    $('form div div textarea').addClass("form-control");
    $('form div div select').addClass("form-control");
    $('form div#swift-submit input').addClass("btn btn-default");
});




$('.add-loading').click(function () {
    target.loadingOverlay();
});

$('.remove-loading').click(function () {
    target.loadingOverlay('remove');
});


$(function () {
    $('[data-toggle="tooltip"]').tooltip();
})



function redirect_account(){
    window.location="localhost:8081/account"
}


function redirect_container(container_name){
    //alert(container_name)
    window.location="localhost:8081/account/"+container_name
}

function check_container_creation_process() {
    var container_name = $('#new_container_name').val();
    //alert(cont)
    $.ajax(
        {
            url: '/account/' + container_name+'/create',
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    //alert("suscess: container " + container_name + " created");
                    $('#containers_list').append("<tr class='active' ><td style='width: 51%;'><a style='color: #222222;' href='/account/"+
                    container_name+"'><small>"+container_name+"</small></a></td></tr>")
                }
                else {
                    alert("failed: container");
                }
            }
        }
    )
}


function load_container(){
    location.reload()
}

EnableSubmit1 = function(val)
{
    var sbmt = document.getElementById("cg_modal_submit");

    if (val.checked == true)
    {
        sbmt.disabled = false;
    }
    else
    {
        sbmt.disabled = true;
    }
}

function config_container(container_name){
    //alert(document.getElementById('publish').checked)
    box_status = document.getElementById('publish').checked
    $.ajax(
        {url: '/account/'+container_name+'/publish/'+box_status,
            type: 'POST',
            success: function (result){
                if (result.status){
                    //alert(result.status)
                    location.reload()
                }

            }

        }
    )

}
function modify_container_config_modal(url, container_name, acl){
    if (acl == 'False'){
        $("#status_cg_modal_body").text(" NO").css('color', 'red')
    }
    else{
        $("#status_cg_modal_body").text(" YES").css('color', 'green')
    }

    $("#cg_modal_title").text("Manage Access to '"+container_name+"'");
    $("#cg_modal_body").text(url+"/"+ container_name);
    $('#cg_modal_submit').attr("onclick", "config_container('" + container_name +"')");
    $("#cg_confirm_modal").modal("show");
}


EnableSubmit = function(val)
{
    //var sbmt = document.getElementById("obj_cg_modal_submit");
    var ttl = document.getElementById("ttl");

    if (val.checked == true) {
        //sbmt.disabled = false;
        ttl.disabled = false;
    }

    else {
        //sbmt.disabled = true;
        ttl.disabled = true;
    }
}

EnableSubmit1 = function(val)
{   //alert(val)

    var sbmt = document.getElementById("obj_cg_modal_submit");

    if (!isNaN(val))
    {
        sbmt.disabled = false;
        //alert("num")
    }

    else {
        //alert("hhh")
        sbmt.disabled = true;
    }
}

function config_object(container_name, obj_name, ttl){
    var ttl_val = document.getElementById('ttl').value
    if(confirm(document.getElementById('tempurl').value+ttl_val)){
    $.ajax(
        {url: '/account/'+container_name+'/'+obj_name+'/tempurl/'+ttl_val,
            type: 'POST',
            success: function (result){
                if (result.status){
                    //alert(result.status)
                    location.reload()
                }

            }

        }
    )

}}
function modify_object_config_modal(url, container_name,obj_name,  cont_acl, tempurl){
    if (cont_acl == 'False'){
        $("#obj_status_cg_modal_body").text(" NO").css('color', 'red')
    }
    else{
        $("#obj_status_cg_modal_body").text(" YES").css('color', 'green')
    }

    $("#obj_cg_modal_title").text(obj_name);
    $("#obj_cg_modal_body").text(url+"/"+ container_name+"/"+obj_name);
    if (tempurl == 'False' ){
        $("#tempurl_read").text("None");
    }
    else{
        $("#tempurl_read").text(tempurl);
    }

    $('#obj_cg_modal_submit').attr("onclick", "config_object('" + container_name +"','" + obj_name +"')");
    $("#obj_cg_confirm_modal").modal("show");
}



function delete_container(container_name){
    $.ajax(
        {
            url: '/account/'+container_name+'/delete',
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    //alert(object_name+' deleted !')
                    location.reload()
                }
            }
        }
    )
    location.reload()
}
function modify_container_delete_modal(container_name) {
    $("#del_modal_title").text(container_name);
    $("#del_modal_body").text("Are you sure you want to delete the container: " + container_name+" ?");
    $('#del_modal_submit').attr("onclick", "delete_container('" + container_name + "')");
    $("#del_confirm_modal").modal("show");
}



function share_object_process(container_name, object_name){
    //var container_name = document.getElementById('container_name_'+i).innerHTML;
    //var object_name = document.getElementById('object_name_'+k).innerHTML;
    c = confirm('Do you really want to generate a temporary URL for '+container_name+'/'+object_name +'?')
    if (c == true) {
        $.ajax(
            {
                url: '/account/'+container_name+'/'+object_name+ '/share',
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

function download_object_process(container_name, object_name){
    $.ajax(
        {
            url: '/account/'+container_name+'/'+ object_name + '/download',
            type: 'GET',
            success: function (result) {
                if (result.status) {
                    window.open(result.status, '_blank')
                }
            }
        }
    )

}

function delete_object(container_name,object_name){
    $.ajax(
        {
            url: '/account/'+container_name+'/'+object_name+'/delete',
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    //alert(object_name+' deleted !')
                    location.reload()
                }
            }
        }
    )
    location.reload()
}
function modify_object_delete_modal(container_name, object_name) {
    $("#delete_modal_title").text(object_name);
    $("#delete_modal_body").text("Are you sure you want to delete the object "  + object_name);
    $('#delete_modal_submit').attr("onclick", "delete_object('" + container_name + "','" + object_name + "')");
    $("#delete_confirm_modal").modal("show");
}


function view_object(container_name, object_name){
    $.ajax(
        {
            url: '/account/'+container_name+'/'+ object_name + '/view',
            type: 'GET',
            success: function (result) {
                if (result.status) {
                    window.open(result.status, '_blank')
                }
            }
        }
    )
}
function modify_object_view_modal(container_name, object_name){
    $("#view_modal_title").text(object_name);
    $("#view_modal_body").text("Are you sure you want to view the object "+object_name);
    $('#view_modal_submit').attr("onclick", "view_object('" +  container_name + "','" + object_name + "')");
    $("#view_confirm_modal").modal("show");

}




function upload_object(file_path, container_name) {

    alert(file_path+' upload to : '+container_name );
    //  container_name = 'folder1'
    /*
    $.ajax(
        {
            url: '/account/'+container_name+'/upload/'+file_path,
            type: 'POST',
            success: function (result) {
                if (result.status) {
                    alert(result.status)
                }
            }
        }
    )*/

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



