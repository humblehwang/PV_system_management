var premissionList =["z8630076@yahoo.com.tw","meihuitseng@itri.org.tw","liyunyeh@itri.org.tw"]//檢查是否有權限查看上傳等頁面

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


function ajaxSendEmail(data, route_name){
    console.log(data);
    $.ajax({ 
    url: userEmail, 
    type: 'POST', 
    dataType: 'json', 
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(response){ 
        console.log(response.responseText);
    }, error: function(xhr) {
        console.log(xhr);
      } 
    });
}



var imported = document.createElement('script');
imported.src = "js/ajaxSend.js";

firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
      //alert(user.email);
      var data = {"user_email":user.email};
     console.log(data);
     $.ajax({ 
     url: "userEmail", 
     type: 'POST', 
     dataType: 'json', 
     data: JSON.stringify(data),
     contentType: 'application/json;charset=UTF-8',
     success: function(response){ 
         console.log(response.responseText);
     }, error: function(xhr) {
         console.log(xhr);
       } 
     });//end ajax
     if(premissionList.indexOf(user.email)==-1){
      alert("權限不符");
      self.location='/search';      
     }
  }
    // User is signed in.
   else {
    // No user is signed in.
      alert("請先登入系統");
      self.location='/';
  }
});















