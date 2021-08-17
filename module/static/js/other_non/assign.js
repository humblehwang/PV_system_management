  var db_btn = document.getElementById("assign");
  db_btn.addEventListener('click',function(){ 
  console.log("assign");
var waiting_con = '<br><br><br><div class="d-flex flex-column align-items-center justify-content-center"><div class="row"><div class="spinner-border text-success" role="status" style="width: 5rem; height: 5rem;"><span class="sr-only">Loading...</span></div></div><br><div class="row"><strong>同意備案分案中....</strong></div></div></div>'
    $("#data_content").html(waiting_con);      
    $("#host_content").html('');  
  ajaxSend2("dataAssignNon","#data_content");  
  });      