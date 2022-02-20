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

    error1 = 'Username and email already exist';
    error2 = 'Username already exists';
    error3 = 'Email already registered';
    error4 = 'Passwords must match';
    error5 = 'Incorrect Username and/or Password';
    error6 = 'Incorrect Username and/or Password';

    if ([error1, error2, error3, error4, error5, error6].includes(formMessages)) {
        $('.flash_message').css('color', 'red');
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