console.log("sdfsdfsdfsdf")
// File upload function
var fileUploader = document.querySelector('#file_uploader');
// Listen for the file input change
fileUploader.addEventListener('change', (f) => {
    var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>讀取資料中....</strong></div></div></div>'
    $("#data_content").html(waiting_con);
    $("#host_content").html('');
    var fileobject = document.getElementById("file_uploader").files[0];
    var formData = new FormData;
    formData.append('file', fileobject);
    ajaxSendData(formData, "dataFormat", "#data_content");
});

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
