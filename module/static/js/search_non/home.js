var premissionList = ['goodderek1@itri.org.tw', 'itri457977@itri.org.tw', 'emma.tsai@itri.org.tw', 'cmshu@itri.org.tw', 'itriA890315@itri.org.tw', 'itri458004@itri.org.tw',"jszhang@itri.org.tw","itri459148@itri.org.tw","itri459121@itri.org.tw","itri459111@itri.org.tw","z8630076@yahoo.com.tw","meihuitseng@itri.org.tw","liyunyeh@itri.org.tw","chinyanghuang@itri.org.tw","itria80333@itri.org.tw","chchen@itri.org.tw","cjlo@itri.org.tw","liyu@itri.org.tw","sjli@itri.org.tw","tina1103@itri.org.tw","fminglin@itri.org.tw"]
$('.collapse').collapse('hide')

function date_init(div_id){
	$(div_id).datepicker({
    format: "yyyy-mm-dd",
    autoclose: true,
    clearBtn: true,
    calendarWeeks: true,
    todayHighlight: true,
    language: 'zh-TW'
});
}

date_init('#start1');
date_init('#start1-2');
date_init('#start1-3');
date_init('#start1-4');
date_init('#start1-5');
date_init('#start1-6');
date_init('#start1-7');
date_init('#end1');
date_init('#end1-2');
date_init('#end1-3');
date_init('#end1-4');
date_init('#end1-5');
date_init('#end1-6');
date_init('#end1-7');
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


var num_cond = document.getElementById("compare1");
if(num_cond){
num_cond.addEventListener("change", function() {
    if(num_cond.value == 7)
    {   
        $("#compare_num1").html('<label for="compare_num1-2" style="height: 30%"></label><input type="text" id="compare_num1-2" class="form-control" placeholder="輸入數字(KW)">');
    }else{
         $("#compare_num1").html('');
    }
});
}




var num_cond2 = document.getElementById("compare2");
if(num_cond2){
    num_cond2.addEventListener("change", function() {
        if(num_cond2.value == 7)
        {   
            $("#compare_num2").html('<label for="compare_num2-2" style="height: 30%"></label><input type="text" id="compare_num2-2" class="form-control" placeholder="輸入數字(KW)">');
        }else{
            $("#compare_num2").html('');
        }
    });
}
    
var num_cond3 = document.getElementById("compare3");
if(num_cond3){
    num_cond3.addEventListener("change", function() {
        if(num_cond3.value == 7)
        {   
            $("#compare_num3").html('<label for="compare_num3-2" style="height: 30%"></label><input type="text" id="compare_num3-2" class="form-control" placeholder="輸入數字(KW)">');
        }else{
            $("#compare_num3").html('');
        }
    });
}




var time_cond = document.getElementById("time");
if(time_cond){
    time_cond.addEventListener("change", function() {
        if(time_cond.value == "2")
        {   
            $("#dyn2").html('<label for="end1" style="height: 30%"></label><input type="text" id="end1" class="form-control" placeholder="結束時間">');
            date_init('#end1');
        }else{
            $("#dyn2").html('');
        }
    });

}

var time_cond2 = document.getElementById("time2");
if(time_cond2){
    time_cond2.addEventListener("change", function() {
        if(time_cond2.value == "2")
        {     
            $("#dyn2-2").html('<label for="end1-2" style="height: 30%"></label><input type="text" id="end1-2" class="form-control" placeholder="結束時間">');
            date_init('#end1-2');
        }else{  
            $("#dyn2-2").html('');
        }
    });
}

var time_cond3 = document.getElementById("time3");
if(time_cond3){
    time_cond3.addEventListener("change", function() {
        if(time_cond3.value == "2")
        {
            $("#dyn2-3").html('<label for="end1-3" style="height: 30%"></label><input type="text" id="end1-3" class="form-control" placeholder="結束時間">');
            date_init('#end1-3');
        }else{
            $("#dyn2-3").html('');
        }
    });
}
var time_cond4 = document.getElementById("time4");
if(time_cond4){
    time_cond4.addEventListener("change", function() {
        if(time_cond4.value == "2")
        {
            $("#dyn2-4").html('<label for="end1-4" style="height: 30%"></label><input type="text" id="end1-4" class="form-control" placeholder="結束時間">');
            date_init('#end1-4');
        }else{
            $("#dyn2-4").html('');
        }
    });

}

var time_cond5 = document.getElementById("time5");
if(time_cond5){
    time_cond5.addEventListener("change", function() {
        if(time_cond5.value == "2")
        {
            $("#dyn2-5").html('<label for="end1-5" style="height: 30%"></label><input type="text" id="end1-5" class="form-control" placeholder="結束時間">');
            date_init('#end1-5');
        }else{
            $("#dyn2-5").html('');
        }
    });
}
var time_cond6 = document.getElementById("time6");
if(time_cond6){
    time_cond6.addEventListener("change", function() {
        if(time_cond6.value == "2")
        {
            $("#dyn2-6").html('<label for="end1-6" style="height: 30%"></label><input type="text" id="end1-6" class="form-control" placeholder="結束時間">');
            date_init('#end1-6');
        }else{
            $("#dyn2-6").html('');
        }
    });
}
var time_cond7 = document.getElementById("time7");
if(time_cond7){
    time_cond7.addEventListener("change", function() {
        if(time_cond7.value == "2")
        {
            $("#dyn2-7").html('<label for="end1-7" style="height: 30%"></label><input type="text" id="end1-7" class="form-control" placeholder="結束時間">');
            date_init('#end1-7');
        }else{
            $("#dyn2-7").html('');
        }
    });
}
var confirm = document.getElementById("sendsearch");
if(confirm){
    confirm.addEventListener("click", function() {
        // close the search tab
        $('#collapseExample').collapse('hide')
        var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>搜尋資料中....</strong></div></div></div>'
        $("#dyn_content").html(waiting_con);
        $("#data_content").html('')


        // catch the key word
        var inputsetnum = $('#inputsetnum').val();
        var inputloc = $('#inputloc').val();
        var inputdep = $('#inputdep').val();
        var inputnote = $('#inputnote').val();   
        var inputcontact = $('#inputcontact').val();
        var inputcompany = $('#inputcompany').val();   
        var inputpoint = $('#inputpoint').val();
        

        var inputassoctel = $('#inputassoctel').val();   
        var inputstatus = $('#inputstatus').val();
        var inputuser = $('#inputuser').val();        
        //catch the selection value
        var e = document.getElementById("inputstatusland");
        var inputstatusland = e.options[e.selectedIndex].text;
        if(inputstatusland == '選擇...'|| inputstatusland=='全選')
            inputstatusland = '';

        e = document.getElementById("inputlandtype");
        var inputlandtype = e.options[e.selectedIndex].text;
        if(inputlandtype == '選擇...' || inputlandtype =='全選')
            inputlandtype = '';

        e = document.getElementById("inputdistrict");
        var inputdistrict = e.options[e.selectedIndex].text;
        if(inputdistrict == '選擇...' || inputdistrict =='全選')
            inputdistrict = '';

    
        e = document.getElementById("inputsetloc");
        var inputsetloc = e.options[e.selectedIndex].text;
        if(inputsetloc == '選擇...' || inputsetloc =='全選')
            inputsetloc = '';
        e = document.getElementById("inputstage");
        var inputstage = e.options[e.selectedIndex].text;
        if( inputstage == 'A.完成規畫整合'){
            inputstage = 'A';
        }
        else if(inputstage == 'B.完成併連審查'){
            inputstage = 'B';
        }
        else if(inputstage == 'C.取得籌備創設'){
            inputstage = 'C';
        }
        else if(inputstage == 'D.取得土地容許使用/完成用地變更'){
            inputstage = 'D';
        }
        else if(inputstage == 'E.取得施工許可'){
            inputstage = 'E';
        }
        else if(inputstage == 'F.完工併聯'){
            inputstage = 'F';
        }
        else if(inputstage == '選擇...' || inputstage=="全選"){
            inputstage = '';
        }

        e = document.getElementById("inputcontrol");
        var inputcontrol = e.options[e.selectedIndex].text;
        if( inputcontrol== '選擇...' || inputcontrol=="全選")
            inputcontrol = '';    

        e = document.getElementById("inputstationchange");
        var inputstationchange = e.options[e.selectedIndex].text;
        if( inputstationchange== '選擇...' || inputstationchange=="全選")
            inputstationchange = '';  

        //get the compare selection
        e = document.getElementById("compare1");
        var compare1_check = e.options[e.selectedIndex].text;
        if(compare1_check == 'default'){
             compare_num1_1 = '';
             compare_num1_2 = '';
        }
        else{
            var compare1 = e.options[e.selectedIndex].value; 
            var compare_num1_1 = $('#compare_num1-1').val();
            if(compare1 == "7"){
                var compare_num1_2 = $('#compare_num1-2').val();
            }else{
                var compare_num1_2 = '';
            }
        }

        //get the compare selection
        e = document.getElementById("compare2");
        var compare2_check = e.options[e.selectedIndex].text;
        if(compare2_check == 'default'){
             compare_num2_1 = '';
             compare_num2_2 = '';
        }
        else{
            var compare2 = e.options[e.selectedIndex].value;
            var compare_num2_1 = $('#compare_num2-1').val();
            if(compare2 == "7"){
                var compare_num2_2 = $('#compare_num2-2').val();
            }else{
                var compare_num2_2 = '';
            }
        }

        //get the compare selection
        e = document.getElementById("compare3");
        var compare3_check = e.options[e.selectedIndex].text;
        if(compare3_check == 'default'){
             compare_num3_1 = '';
             compare_num3_2 = '';
        }
        else{
            var compare3 = e.options[e.selectedIndex].value;
            var compare_num3_1 = $('#compare_num3-1').val();
            if(compare3 == "7"){
                var compare_num3_2 = $('#compare_num3-2').val();
            }else{
                var compare_num3_2 = '';
            }
        }

        // get the date interval
        e = document.getElementById("time");
        var interval_ch1 = e.options[e.selectedIndex].value;
        var interval_name1 = 'docu_date';
        if(interval_ch1 == '9'){
             start1 = '';
             end1 = '';
            interval_ch1 = '2';
        }
        else{
            if(interval_ch1 == "2"){
                var start1 = $('#start1').val();
                var end1 = $('#end1').val();
            }else{
                var start1 = $('#start1').val();
                var end1 = '';
            }
        }


        // get the date interval
        e = document.getElementById("time2");
        var interval_ch2 = e.options[e.selectedIndex].value;
        var interval_name2 = 'finish_date';
        if(interval_ch2 == '9'){
             start2 = '';
             end2 = '';
            interval_ch2 = '2';
        }
        else{


            if(interval_ch2 == "2"){
                var start2 = $('#start1-2').val();
                var end2 = $('#end1-2').val();
            }else{
                var start2 = $('#start1-2').val();
                var end2 = '';
            }
        }

        // get the date interval
        e = document.getElementById("time3");
         var interval_ch3 = e.options[e.selectedIndex].value;
        var interval_name3 = 'apply_setup_date';
        if(interval_ch3 == '9'){
             start3 = '';
             end3 = '';
            interval_ch3 = '2';
        }
        else{


            if(interval_ch3 == "2"){
                var start3 = $('#start1-3').val();
                var end3 = $('#end1-3').val();
            }else{
                var start3 = $('#start1-3').val();
                var end3 = '';
            }
        }

        // get the date interval
        e = document.getElementById("time4");
       var interval_ch4 = e.options[e.selectedIndex].value;
        var interval_name4 = 'setup_date';
        if(interval_ch4 == '9'){
             start4 = '';
             end4 = '';
            interval_ch4 = '2';
        }
        else{


            if(interval_ch4 == "2"){
                var start4 = $('#start1-4').val();
                var end4 = $('#end1-4').val();
            }else{
                var start4 = $('#start1-4').val();
                var end4 = '';
            }
        }
        // get the date interval
        e = document.getElementById("time5");
        var interval_ch5 = e.options[e.selectedIndex].value;
        var interval_name5 = 'get_land_date';
        if(interval_ch5 == '9'){
             start5 = '';
             end5 = '';
            interval_ch5 = '2';
        }
        else{


            if(interval_ch5 == "2"){
                var start5 = $('#start1-5').val();
                var end5 = $('#end1-5').val();
            }else{
                var start5 = $('#start1-5').val();
                var end5 = '';
            }
        }

        // get the date interval
        e = document.getElementById("time6");
        var interval_ch6 = e.options[e.selectedIndex].value;
        var interval_name6 = 'apply_date';
        if(interval_ch6 == '9'){
             start5 = '';
             end5 = '';
            interval_ch6 = '2';
        }
        else{


            if(interval_ch6 == "2"){
                var start6 = $('#start1-6').val();
                var end6 = $('#end1-6').val();
            }else{
                var start6 = $('#start1-6').val();
                var end6 = '';
            }
        }
        // get the date interval
        e = document.getElementById("time7");
        var interval_ch7 = e.options[e.selectedIndex].value;
        var interval_name7 = 'get_date';
        if(interval_ch7 == '9'){
             start7 = '';
             end7 = '';
            interval_ch7 = '2';
        }
        else{


            if(interval_ch7 == "2"){
                var start7 = $('#start1-7').val();
                var end7 = $('#end1-7').val();
            }else{
                var start7 = $('#start1-7').val();
                var end7 = '';
            }
        }




    var request = {"user_email":inputuser,"status":inputstatus,"assoc_tel":inputassoctel,"set_num": inputsetnum, "loc_addr": inputloc,"set_dep":inputdep,"note":inputnote,"assoc_name":inputcontact  ,"status_land":inputstatusland, "change_land_type" : inputlandtype, "province" : inputdistrict, "booster_sta" : inputstationchange, "company":inputcompany,"set_loc":inputsetloc,"booster_cer":inputpoint,"stage":inputstage,"control":inputcontrol,"comp1":[compare1, 'ini_cap', compare_num1_1, compare_num1_2], "comp2":[compare2, 'noapply_cap', compare_num2_1, compare_num2_2], "comp3":[compare3, 'get_cap', compare_num3_1, compare_num3_2], "interval1":[interval_ch1, interval_name1, start1, end1], "interval2":[interval_ch2, interval_name2, start2, end2], "interval3":[interval_ch3, interval_name3, start3, end3], "interval4":[interval_ch4, interval_name4, start4, end4],"interval5":[interval_ch5, interval_name5, start5, end5]}



    console.log(request);





        ajaxSend(request, "select", "#dyn_content");
        
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
        $("#dl_form").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn1">下載開發中案件清冊</button>')
         }
      }

    });//firebase.auth()        
        
        
;


        });
}