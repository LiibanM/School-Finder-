

//This was used from Djangos official documentation
// this handles the cookie thats sent whenever AJax requests are made
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

//This was used from Djangos official documentation
// this handles the cookie thats sent whenever AJax requests are made
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
//This was used from Djangos official documentation
// this handles the cookie thats sent whenever AJax requests are made
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//when delete is called call the ajax request
$(function(){
$(".list-button1").click(deleteRow)
});

// function hello(){
//   school_id = $(this).attr("value");
//   console.log(school_id);
// }


function deleteRow(){
  //grabbing the id thats to be removed and which list item is going to be removed
  school_id = $(this).attr("value");
  item_to_remove = $(this).parent().attr("id")

//ajax post request to send the school id to the backend view where i remove it
  $.ajax({

    url: '/deleteRow/',
    type: "POST",
    data:{
      school_id : school_id,
    },
    success: function(response){
        //after succesful removing this removes the html of the list
        $('#'+item_to_remove).remove()

    },
  });
}
