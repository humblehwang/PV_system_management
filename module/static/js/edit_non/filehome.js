
// File upload function
var editfileUploader = document.querySelector('#editfile_uploader');
// Listen for the file input change
editfileUploader.addEventListener('change', (f) => {
    var loading_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>處理資料中....</strong></div></div></div>'
    $("#host_content").html(loading_con);
    $("#data_content").html('');
    var fileobject = document.getElementById("editfile_uploader").files[0];
    var formData = new FormData;
    formData.append('file', fileobject);
    ajaxSendData(formData, "fileEditSelect", "#host_content");
});


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
