$.get("/static/preloader.html", function(data){
  $("#loader").replaceWith(data);
});

$(window).on('load', function(){
  setTimeout(removeLoader, 300); //wait for page load PLUS two seconds.
});

function removeLoader(){
    $( ".loader-wrapper" ).fadeOut(100, function() {
      // fadeOut complete. Remove the loading div
      $( ".loader-wrapper" ).remove(); //makes page more lightweight 
  });   
}
