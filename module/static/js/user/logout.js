//登出
var signoutSmtBtn = document.getElementById("signout_btn");

signoutSmtBtn.addEventListener("click",function(e){
    e.preventDefault();
	firebase.auth().signOut().then(function() {
        alert("登出成功");
		console.log("User sign out!");
        self.location='/';
	}, function(error) {
  	console.log("User sign out error!");
	})
},false);