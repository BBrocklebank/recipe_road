// Inititialise Materialize js components
$(document).ready(function(){
    $('.sidenav').sidenav({edge: 'right'});
    $('.modal').modal();
    });

 // Opens modal to display flash messages
 let formMessages = $('.flash_message').text();
 $(document).ready(function() {
     if (formMessages) {
         $('.modal').modal('open');
     }

     // Sets text colour based on flash message
     if (formMessages == 'Registration Succesful!') {
         $('.flash_message').css('color', 'green');
     } else {
         $('.flash_message').css('color', 'red');
     }

 });