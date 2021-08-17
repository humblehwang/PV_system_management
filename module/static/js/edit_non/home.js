
function sendselect(){
	selection = $('#inlineFormCustomSelectPref').val()
	js_data = {"selection" : selection};
    ajaxSend(js_data, "select", "#dyn_content");
    $("#data_content").html('');
    $("#host_content").html('');
}

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

