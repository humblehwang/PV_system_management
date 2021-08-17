var premissionList = ['goodderek1@itri.org.tw', 'itri457977@itri.org.tw', 'emma.tsai@itri.org.tw', 'cmshu@itri.org.tw', 'itriA890315@itri.org.tw', 'itri458004@itri.org.tw',"jszhang@itri.org.tw","itri459148@itri.org.tw","itri459121@itri.org.tw","itri459111@itri.org.tw","z8630076@yahoo.com.tw","meihuitseng@itri.org.tw","liyunyeh@itri.org.tw","chinyanghuang@itri.org.tw","itria80333@itri.org.tw","chchen@itri.org.tw","cjlo@itri.org.tw","liyu@itri.org.tw","sjli@itri.org.tw","tina1103@itri.org.tw","fminglin@itri.org.tw"]



$('.collapse').collapse('hide');

// for the side nav bar btn
(function($) {

    "use strict";

    var fullHeight = function() {

        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function(){
            $('.js-fullheight').css('height', $(window).height());
        });

    };
    fullHeight();

    $('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);





var confirm = document.getElementById("sendsearch");
if (confirm){

    confirm.addEventListener("click", function() {
        // close the search tab
        $('#collapseExample').collapse('hide')
        var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>搜尋資料中....</strong></div></div></div>'
        $("#dyn_content").html(waiting_con);
        $("#data_content").html('')


        // catch the key word
        var keyword = $('#keyword').val();


    var request = {"keyword":keyword}
        console.log(request);

        ajaxSend(request, "select", "#dyn_content");





    try{
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
             if(premissionList.indexOf(user.email)!=-1){
                 $("#dl_form").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn1">下載清冊</button>');
                
             }
          }
        });//firebase.auth()
    }//try  
    catch{
   

    $("#dl_form").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn1">下載清冊</button>');
    }



        });
}      
      

      