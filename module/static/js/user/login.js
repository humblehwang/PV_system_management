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

//登入
var email = document.getElementById("email");
var password = document.getElementById("password");
var loginSmtBtn = document.getElementById("login_btn");
var user = firebase.auth().currentUser;






firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
     self.location='/search';
  }
});


loginSmtBtn.addEventListener("click",function(e){
    e.preventDefault();
    firebase.auth().signInWithEmailAndPassword(email.value, password.value)
        .then(function(){
            alert("登入成功");
            self.location='/search';          
    })
      .catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      if (errorCode === 'auth/wrong-password') {
        alert('Wrong password.');
      } else {
        alert(errorMessage);
      }
      console.log(error);
    });

});
