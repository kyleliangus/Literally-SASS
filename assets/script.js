$(document).ready(function() {

  $("#submit").click(function() {
    $.post("10.142.175.48", $("#file_form").serialize());
  });



})
