
var user = firebase.auth().currentUser;
var chgPwd = document.getElementById("new-password");
var chgPwdBtn = document.getElementById("reset_btn");


//登出


function logout(){
    e.preventDefault();
	firebase.auth().signOut().then(function() {
        alert("User Sign Out");
		console.log("User sign out!");
        window.location.replace("http://140.96.39.108:4567/"); 
	}, function(error) {
  	console.log("User sign out error!");
	})
},false);


chgPwdBtn.addEventListener("click",function(e){
    alert(chgPwd.value)
    e.preventDefault();
	user.updatePassword(chgPwd.value).then(function() {
    // Email sent.
    alert("更改密碼");
    console.log("更改密碼");
    chgPwd.value = "";
    logout();
  }, function(error) {
    // An error happened.
    console.error("更改密碼",error);
  })
},false);


