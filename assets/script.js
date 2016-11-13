$(document).ready(function() {

  $("#submit").click(function() {
    var url = "10.142.175.48";
    var params = "lorem=ipsum&name=alpha";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
  });



})
