// Inititialise Materialize js components
$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: 'right'
    });
    $('.modal').modal();
});

// Opens modal to display flash messages
let formMessages = $('.flash_message').text();
$(document).ready(function () {
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

// Alters form route depending on nav button selected
 $( ".register_btn" ).click(function() {
    $('.form').attr('action', '{{ url_for("register") }}');
  });

  $( ".login_btn" ).click(function() {
    $('.form').attr('action', '{{ url_for("login") }}');
  });

  $( ".logout_btn" ).click(function() {
    $('.form').attr('action', '{{ url_for("logout") }}');
  });