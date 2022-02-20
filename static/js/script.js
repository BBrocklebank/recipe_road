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

    // ADD ALL ERROR MESSAGES AND SET TO RED -- FIX
    if (formMessages == 'Registration Succesful!') { 
        $('.flash_message').css('color', 'green');
    } else {
        $('.flash_message').css('color', 'green');
    }
});

// Removes/Adds from elements, action & attributes

$(".login_btn").click(function () {
    $('#first_name, #last_name, #email, #password_check').attr('required', false);
    $('.form_name, .form_email, .password_check').hide();
    $('.password').removeClass("s6").addClass("s12");
});

$(".register_btn").click(function () {
    $('.form_name, .form_email, .password_check').show();
    $('#first_name, #last_name, #email, #password_check').attr('required', true);
    $('.password').removeClass("s12").addClass("s6");
});