var premissionList = ['goodderek1@itri.org.tw', 'itri457977@itri.org.tw', 'emma.tsai@itri.org.tw', 'cmshu@itri.org.tw', 'itriA890315@itri.org.tw', 'itri458004@itri.org.tw',"jszhang@itri.org.tw","itri459148@itri.org.tw","itri459121@itri.org.tw","itri459111@itri.org.tw","z8630076@yahoo.com.tw","meihuitseng@itri.org.tw","liyunyeh@itri.org.tw","chinyanghuang@itri.org.tw","itria80333@itri.org.tw","chchen@itri.org.tw","cjlo@itri.org.tw","liyu@itri.org.tw","sjli@itri.org.tw","tina1103@itri.org.tw","fminglin@itri.org.tw","serene535901@itri.org.tw"]



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
date_init('#end1');
date_init('#end1-2');
date_init('#end1-3');
date_init('#end1-4');
date_init('#end1-5');
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
if (num_cond){
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
if (num_cond2){
    num_cond2.addEventListener("change", function() {
        if(num_cond2.value == 7)
        {   
            $("#compare_num2").html('<label for="compare_num2-2" style="height: 30%"></label><input type="text" id="compare_num2-2" class="form-control" placeholder="輸入數字(KW)">');
        }else{
            $("#compare_num2").html('');
        }
    });
}


var time_cond = document.getElementById("time");
if (time_cond){
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
if (time_cond2){
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
if (time_cond3){
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
if (time_cond4){
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
if (time_cond5){
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


var confirm = document.getElementById("sendsearch");
if (confirm){

    confirm.addEventListener("click", function() {
        // close the search tab
        $('#collapseExample').collapse('hide')
        var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>搜尋資料中....</strong></div></div></div>'
        $("#dyn_content").html(waiting_con);
        $("#data_content").html('')


        // catch the key word
        var comp = $('#inputcompany').val();
        var user = $('#inputuser').val();    
        var loc = $('#inputloc').val();
        var contact = $('#inputcontact').val();
        var pronum = $('#inputpronum').val();
        var pronum2 = $('#inputpronum2').val();    
        var locnum = $('#inputlocnum').val();
        var dep = $('#inputdep').val();    
        var project_type_itri = $('#porject_type_itri').val();    

        //catch the selection value
        var e = document.getElementById("inputcasetype");
        var casetype = e.options[e.selectedIndex].text;
        if(casetype == '選擇...'|| casetype=='全選')
            casetype = '';

        var e = document.getElementById("finish_time");
        var finish_time = e.options[e.selectedIndex].text;
        if(finish_time == '選擇...'|| finish_time=='全選')
            finish_time = '';    
        var e = document.getElementById("stage_time");
        var stage_time = e.options[e.selectedIndex].text;
        if(stage_time == '選擇...'|| stage_time=='全選')
            stage_time = '';       

        e = document.getElementById("inputsetloc");
        var loctype = e.options[e.selectedIndex].text;
        if(loctype == '選擇...' || loctype =='全選')
            loctype = '';

        e = document.getElementById("inputdistrict");
        var province = e.options[e.selectedIndex].text;
        if(province == '選擇...' || province =='全選')
            province = '';


        var project_type = $('#inputprotype').val();
        //e = document.getElementById("inputprotype");
        //var project_type = e.options[e.selectedIndex].text;
        //if(project_type == '選擇...'|| project_type =='全選')
            //project_type = '';

        e = document.getElementById("inputsellelec");
        var sellmethod = e.options[e.selectedIndex].text;
        if(sellmethod == '選擇...' || sellmethod=="全選")
            sellmethod = '';

        e = document.getElementById("sta_month");
        var sta_month = e.options[e.selectedIndex].text;
        if(sta_month == '選擇...' || sta_month=="全選")
            sta_month = '';    

        
        e = document.getElementById("review");
        var review = e.options[e.selectedIndex].text;
        if(review == '免土地變更及免土地容許'){
            review = '0';
        }
        if(review == '土地變更'){
            review = '1';
        }        
        if(review == '土地容許'){
            review = '2';
        }                
        
        if(review == '選擇...' || review=="全選")
            review = '';         
        
        
        e = document.getElementById("review2");
        var review2 = e.options[e.selectedIndex].text;
        if(review2 == '免出流管制及免海岸管理'){
            review2 = '0';
        }
        if(review2 == '出流管制'){
            review2 = '1';
        }        
        if(review2 == '海岸管理'){
            review2 = '2';
        }  
        if(review2 == '出流管制 + 海岸管理'){
            review2 = '3';
        }                if(review2 == '選擇...' || review2=="全選")
            review2 = ''; 
        
        

        var status = $('#inputstatus').val();
        //e = document.getElementById("inputstatus");
        //var status = e.options[e.selectedIndex].text;
        //if(status == '選擇...' || status == "全選")
        //	status = '';

    /*使用分區、用地類別*/    

        var use_type = $('#inputusetype').val();

        //e = document.getElementById("inputusetype");
        //var use_type = e.options[e.selectedIndex].text;
        //if(use_type == '選擇...' || use_type =='全選')
            //use_type = '';

        var land_type = $('#inputlandtype').val();
        //e = document.getElementById("inputlandtype");
        //var land_type = e.options[e.selectedIndex].text;
        //if(land_type == '選擇...' || land_type =='全選')
        //	land_type = '';


        e = document.getElementById("inputstage");
        var stage = e.options[e.selectedIndex].text;
        if(stage == '選擇...' || stage =='全選')
            stage = '';    
        
        e = document.getElementById("inputstep");
        var step = e.options[e.selectedIndex].text;
        if(step == '選擇...' || step =='全選')
            step = '';    
        
        e = document.getElementById("inputcontrol");
        var inputcontrol = e.options[e.selectedIndex].text;
        if( inputcontrol== '選擇...' || inputcontrol=="全選")
            inputcontrol = '';    	
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



        // get the date interval
        e = document.getElementById("time");
        var interval_ch1 = e.options[e.selectedIndex].value;
        var interval_name1 = 'apply_date';
        if(interval_ch1 == '9'){
             start1 = '';
             end1 = '';
            interval_ch1 = '2';
        }
        else{
            ;

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
        var interval_name2 = 'appr_date';
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
        var interval_name3 = 'sign_date';
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
        var interval_name4 = 'finish_date';
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
        var interval_name5 = 'finish';
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

        // get tagging
        var tag_arr = [];
        for(var i = 1; i <= 4; i++){
            let ele = document.getElementById('tagCheckbox'+i);
            if(ele.checked)
                tag_arr.push(ele.value);
        }
        /*
        if((stage != '' || start5 !='') &&( status=="放棄或失效" || status == "已有併聯紀錄")){
            alert("預估搜尋欄位不包含放棄或失效、已有併聯紀錄");
            window.location.replace("http://140.96.39.108:4567/search");

        }

        if((stage != '' || start5 !='') && (status != "已有簽約紀錄" && status != "已取得同意備案核准" )){
            status = "已有簽約紀錄";
            var status2 = "已取得同意備案核准";
            var request = {"company": comp, "loc_addr": loc, "loca_num": locnum, "pro_num": pronum, "pro_num2": pronum2, "assoc_name":contact, "case_type": casetype, "loc_type": loctype, "province": province, "project_type":project_type, "sell_method":sellmethod, "status":[status,status2], "use_type":use_type, "land_type":land_type, "comp1":[compare1, 'app_cap', compare_num1_1, compare_num1_2], "comp2":[compare2, 'finish_cap', compare_num2_1, compare_num2_2], "interval1":[interval_ch1, interval_name1, start1, end1], "interval2":[interval_ch2, interval_name2, start2, end2], "interval3":[interval_ch3, interval_name3, start3, end3], "interval4":[interval_ch4, interval_name4, start4, end4],"tag": ['tag', tag_arr],"finish":[interval_ch5, interval_name5, start5, end5] ,"stage":stage,"control":inputcontrol,"user_email":user,"sta_month":sta_month,"flag":finish_time}
        console.log(request);
        }



        else{
                var request = {"company": comp, "loc_addr": loc, "loca_num": locnum, "pro_num": pronum,"pro_num2": pronum2, "assoc_name":contact, "case_type": casetype, "loc_type": loctype, "province": province, "project_type":project_type, "sell_method":sellmethod, "status":status, "use_type":use_type, "land_type":land_type, "comp1":[compare1, 'app_cap', compare_num1_1, compare_num1_2], "comp2":[compare2, 'finish_cap', compare_num2_1, compare_num2_2], "interval1":[interval_ch1, interval_name1, start1, end1], "interval2":[interval_ch2, interval_name2, start2, end2], "interval3":[interval_ch3, interval_name3, start3, end3], "interval4":[interval_ch4, interval_name4, start4, end4],"tag": ['tag', tag_arr],"finish":[interval_ch5, interval_name5, start5, end5] ,"stage":stage,"control":inputcontrol,"user_email":user,"sta_month":sta_month,"flag":finish_time}
        console.log(request);
        }
        */


    var request = {"project_type_itri":project_type_itri,"dep":dep,"step":step,"company": comp, "loc_addr": loc, "loca_num": locnum, "pro_num": pronum,"pro_num2": pronum2, "assoc_name":contact, "case_type": casetype, "loc_type": loctype, "province": province, "project_type":project_type, "sell_method":sellmethod, "status":status, "use_type":use_type, "land_type":land_type, "comp1":[compare1, 'app_cap', compare_num1_1, compare_num1_2], "comp2":[compare2, 'finish_cap', compare_num2_1, compare_num2_2], "interval1":[interval_ch1, interval_name1, start1, end1], "interval2":[interval_ch2, interval_name2, start2, end2], "interval3":[interval_ch3, interval_name3, start3, end3], "interval4":[interval_ch4, interval_name4, start4, end4],"tag": ['tag', tag_arr],"finish":[interval_ch5, interval_name5, start5, end5] ,"stage":stage,"control":inputcontrol,"user_email":user,"sta_month":sta_month,"flag":finish_time,"flag2":stage_time,"review":review,"review2":review2}
        console.log(request);
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
                 $("#dl_form2").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn2">下載清冊(只包含備案資訊+電訪記錄)</button>');
             }
          }
        });//firebase.auth()
    }//try  
    catch{
    $("#dl_form2").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn2">下載清冊(只包含備案資訊+電訪記錄)</button>');

    $("#dl_form").html('<button type="submit" class="btn btn-raised btn-outline-danger" form="dn_btn1">下載清冊</button>');
    }



        });
}      
      

      