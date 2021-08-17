var premissionList =  ['goodderek1@itri.org.tw', 'itri457977@itri.org.tw', 'emma.tsai@itri.org.tw', 'cmshu@itri.org.tw', 'itriA890315@itri.org.tw', 'itri458004@itri.org.tw',"jszhang@itri.org.tw","itri459148@itri.org.tw","itri459121@itri.org.tw","itri459111@itri.org.tw","z8630076@yahoo.com.tw","meihuitseng@itri.org.tw","liyunyeh@itri.org.tw","chinyanghuang@itri.org.tw","itria80333@itri.org.tw","chchen@itri.org.tw","cjlo@itri.org.tw","liyu@itri.org.tw","sjli@itri.org.tw","tina1103@itri.org.tw","fminglin@itri.org.tw"]//檢查是否有權限查看上傳等頁面

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















