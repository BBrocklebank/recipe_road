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

// Removes/Adds from elements and action

$(".login_btn").click(function () {
    $('.form_name').hide();
    $('.form_email').hide();
    $('.password_check').hide();
    $('.password').removeClass("s6").addClass("s12");
    $('.form').attr('action', '{{ url_for("login") }}');
});

$(".register_btn").click(function () {
    $('.form_name').show();
    $('.form_email').show();
    $('.password_check').show();
    $('.password').removeClass("s12").addClass("s6");
    $('.form').attr('action', '{{ url_for("register") }}');
});