/*var imported = document.createElement('script');


imported.src = "https://cdn.jsdelivr.net/npm/firebase@6.1.0/firebase.js";
imported.src = "https://www.gstatic.com/firebasejs/7.11.0/firebase-app.js";
imported.src = "https://www.gstatic.com/firebasejs/7.11.0/firebase-analytics.js";
imported.src = "https://www.gstatic.com/firebasejs/7.11.0/firebase-auth.js";
imported.src = "https://www.gstatic.com/firebasejs/7.11.0/firebase-firestore.js";



var firebaseConfig = {
    apiKey: "AIzaSyAYm3PUeQpMR62EQzBCNoX4SJsl6jPRZcM",
    authDomain: "itriwebsystem.firebaseapp.com",
    databaseURL: "https://itriwebsystem.firebaseio.com",
    projectId: "itriwebsystem",
    storageBucket: "itriwebsystem.appspot.com",
    messagingSenderId: "694056489044",
    appId: "1:694056489044:web:295ae1c91d9603df385dc1",
    measurementId: "G-YMGMG1ENZB"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
*/

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
     });
  }
    // User is signed in.
   else {
    // No user is signed in.
      alert("請先登入系統");
      self.location='/'; 
  }
});

















/*
<script src="https://cdn.jsdelivr.net/npm/firebase@6.1.0/firebase.js"></script>
  <!-- Firebase App (the core Firebase SDK) is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/7.11.0/firebase-app.js"></script>

  <!-- If you enabled Analytics in your project, add the Firebase SDK for Analytics -->
<script src="https://www.gstatic.com/firebasejs/7.11.0/firebase-analytics.js"></script>

  <!-- Add Firebase products that you want to use -->
<script src="https://www.gstatic.com/firebasejs/7.11.0/firebase-auth.js"></script>
<script src="https://www.gstatic.com/firebasejs/7.11.0/firebase-firestore.js"></script>

var firebaseConfig = {
    apiKey: "AIzaSyAYm3PUeQpMR62EQzBCNoX4SJsl6jPRZcM",
    authDomain: "itriwebsystem.firebaseapp.com",
    databaseURL: "https://itriwebsystem.firebaseio.com",
    projectId: "itriwebsystem",
    storageBucket: "itriwebsystem.appspot.com",
    messagingSenderId: "694056489044",
    appId: "1:694056489044:web:295ae1c91d9603df385dc1",
    measurementId: "G-YMGMG1ENZB"
};
firebase.initializeApp(firebaseConfig);



function check_login(){
    var flag = 0
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        // User is signed in.
          flag = 1;
      } else {
        // No user is signed in.
          flage = 0;
      }
    });
    
    return flag;
}*/
