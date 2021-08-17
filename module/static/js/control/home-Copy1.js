var sing_case = document.getElementById("select_case");
var result_list = []
// Listen for the file input change
$('#select_case').on('select2:select', function (e) {
  // Do something
  var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border text-primary" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>讀取資料中....</strong></div></div></div>'
    $("#host_content").html(waiting_con);
    var option = $( "#select_case option:selected" ).text();
    request = {"option": option}
    console.log(request);
    //result_list = genGanttData("control_edit", request, "#host_content")
    ajaxGetListReturn(request, "control_edit", "#host_content");
    
});
// sing_case.addEventListener('change', function(){

// });


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

