
function ajaxSend2(route_name, div_id){
    $.ajax({ 
    url: route_name, 
    type: 'POST', 
    dataType: 'json', 
    data: "",
    contentType: 'application/json;charset=UTF-8',
    success: function(response){ 
        $(div_id).html(response.responseText);
    }, error: function(xhr) {
        console.log(xhr);
      } 
    });
}
function ajaxSend(data, route_name, div_id){
    $.ajax({ 
    url: route_name, 
    type: 'POST', 
    dataType: 'json', 
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(response){ 
        $(div_id).html(response.responseText);
    }, error: function(xhr) {
        console.log(xhr);
      } 
    });
}

// This api only use to send file object
function ajaxSendData(formdata, route_name, div_id){
    $.ajax({ 
    url: route_name, 
    type: "POST", 
    dataType: "json",
    data: formdata,
    contentType: false,
    processData: false,
    success: function(response){
        $(div_id).html(response.responseText);
        //document.getElement(.collapse)
    }, error: function(xhr) {
        console.log(xhr);
    } 
    });

}

// This api only use to download file object
function ajaxDLData(route_name){
    $.ajax({ 
    url: route_name, 
    type: "POST", 
    dataType: "json",
    data: "",
    contentType: false,
    processData: false,
    success: function(response){
        console.log(response.headers)
        //document.getElement(.collapse)
    }, error: function(xhr) {
        console.log(xhr);
    } 
    });
}

// This api only use to download file object
function ajaxNewWindow(data, route_name){
    $.ajax({ 
    url: route_name, 
    type: "POST", 
    dataType: "json",
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(response){
        var myWindow = window.open("");
        myWindow.document.write(response.responseText);
        //document.getElement(.collapse)
    }, error: function(xhr) {
        console.log(xhr);
    } 
    });
}



// for getting gantt data
function ajaxGetListReturn(data, route_name, div_id){
    $.ajax({ 
    url: route_name, 
    type: "POST", 
    dataType: "json",
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    }).done(function(data, textStatus, jqXHR) {
        $(div_id).html(data.responseText);
      // do sth
    }).fail(function(jqXHR, textStatus, errorThrown){
        alert('您輸入不存在的備案編號')
        location.reload(true);
        console.log(errorThrown);
    });
}

