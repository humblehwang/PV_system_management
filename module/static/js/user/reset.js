firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in.
  
  var chgPwd = document.getElementById("new-password");
  var chgPwdBtn = document.getElementById("reset_btn");
  chgPwdBtn.addEventListener("click",function(e){
    e.preventDefault();
	user.updatePassword(chgPwd.value).then(function() {
    // Email sent.
    alert("更改密碼成功，請重新登入");
    console.log("更改密碼成功");
    chgPwd.value = "";
 
    //After change the password, the user will be logout
    firebase.auth().signOut().then(function() {
		console.log("User sign out!");
        self.location='/'; 
	}, function(error) {
  	console.log("User sign out error!");
	})    
        
        
    self.location='/';
   }, function(error) {
    // An error happened.
    console.error("更改密碼",error);
   })
  },false);    
      
    
  } else {
    // No user is signed in.
    self.location='/';
  }
});



