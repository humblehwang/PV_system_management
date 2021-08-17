
var email = document.getElementById("email");
var password = document.getElementById("password");
var signUpSmtBtn = document.getElementById("signUp_btn");


signUpSmtBtn.addEventListener("click",function(e){ 
    e.preventDefault();
    firebase.auth().createUserWithEmailAndPassword(email.value, password.value)    
        .then(function(){
            sendVerifiedEmail(email.value,password.value);
            alert("註冊成功，請先驗證您的信箱，再登入");
            
            firebase.auth().signOut().then(function() {
            }, function(error) {
            console.log("User sign out error!");
            })
        
            window.location.replace("http://140.96.39.108:4567/"); 
        })
    
        .catch(function(error){
          // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            // [START_EXCLUDE]
            if (errorCode == 'auth/weak-password') {
              alert('The password is too weak.');
            }
            else {
              alert(errorMessage);
            }
       
    
    });//end_createUser
});//end_registerSmtBtn.addEventListener



function sendVerifiedEmail (email_send,password_send){
    var user = firebase.auth().currentUser;
    
    
    firebase.auth().signInWithEmailAndPassword(email_send, password_send)
        .then(function(){
            console.log("login sucess");             
    })
      .catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      if (errorCode === 'auth/wrong-password') {
        console.log('Wrong password.');
      } else {
        console.log(errorMessage);
      }
      console.log(error);
    });
    
    
    
    
    
    user.sendEmailVerification().then(function() {
      // Email sent.
    }).catch(function(error) {
      // An error happened.
    });
}


