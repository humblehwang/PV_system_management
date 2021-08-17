


var auth = firebase.auth();
var email = document.getElementById("email")
var sendSmtBtn = document.getElementById("send_btn");

sendSmtBtn.addEventListener("click",function(e){
    e.preventDefault();
    auth.sendPasswordResetEmail(email.value)
        .then(function(){
            alert("請去查看您所填寫的信箱："+email.value);
            window.location.replace("http://140.96.39.108:4567/"); 
    })
      .catch(function(error) {
      // Handle Errors here.
      alert(error);
      console.log(error);
    });

});


