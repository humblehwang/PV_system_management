


firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
      alert(user.email);
  }
    // User is signed in.
  else {
    // No user is signed in.
      alert("請先登入系統");
      window.location.replace("http://140.96.39.108:4567/"); 
  }
});