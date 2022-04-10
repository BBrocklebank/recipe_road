// Inititialise Materialize js components
$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: 'right'
    });
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('.chips').chips();
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.chips').chips();
    $('.chips-initial').chips({
        data: [{
        tag: 'Apple',
        }, {
        tag: 'Microsoft',
        }, {
        tag: 'Google',
        }],
    });
    $('.chips-placeholder').chips({
        placeholder: 'Enter a tag',
        secondaryPlaceholder: '+Tag',
    });
    $('.chips-autocomplete').chips({
        autocompleteOptions: {
        data: {
            'Apple': null,
            'Microsoft': null,
            'Google': null
        },
        limit: Infinity,
        minLength: 1
        }
    });
    $('select').formSelect();
});

// List of Python flash messages
errorMessages =
    [
    error1 = 'Register: Username and email already exist',
    error2 = 'Register: Username already exists',
    error3 = 'Register: Email already registered',
    error4 = 'Register: Passwords must match',
    error5 = 'Login: Incorrect Username and/or Password',
    error6 = 'Username and email already exist',
    error7 = 'Username already exists',
    error8 = 'Email already registered'
    ];

// Opens modal to display flash messages
let formMessages = $('.flash_message').text();
$(document).ready(function () {
    if (formMessages) {
        $('.modal').modal('open');
    }

    // Sets text colour based on flash message
    if (errorMessages.includes(formMessages)) {
        $('.flash_message').css('color', 'red');
    } else {
        $('.flash_message').css('color', 'green');
    }
});

// Removes/Adds login from elements, actions & attributes
$(".login_btn, .logout_btn").click(function loginTrigger () {
    $('.modal_title').text('Login');
    $('.modal_description').text('Login to your account and start sharing recipes instantly!');
    $('.form_name, .form_email, .password_check').hide();
    $('#first_name, #last_name, #email, #password_check').attr('required', false);
    $('.password').removeClass("s6").addClass("s12");
});

$(".register_btn").click(function registerTrigger () {
    $('.modal_title').text('Register');
    $('.modal_description').text('Create an account to share and edit your own unique recipes to the Recipe Road!');
    $('.form_name, .form_email, .password_check').show();
    $('#first_name, #last_name, #email, #password_check').attr('required', true);
    $('.password').removeClass("s12").addClass("s6");
});

// On page refresh from error, sets correct modal elements
document.addEventListener("DOMContentLoaded", function(){

    if (formMessages.includes('Login')) {
        $('.login_btn').trigger('click');
    } else {
        $('.register_btn').trigger('click');
    }
});

// Alerts user to session logout
$(".logout_btn").click(function () {
    alert('You have been logged out');
});

// Unlocks profile details for editing
$(".profile_edit").click(function () {
    $('#first_name, #last_name, #email, #username').removeAttr('readonly');
});

//___________________________Delete Modal

let buttonNum = 0;
let modalNum = 0;
let spanNum = 0;
let deleteButton = $('.delete_trigger');
let deleteModal = $('.delete_modal');
let span = $('.close');

// Close Delete Modal
let closeSpan = function (){
    let spanClass = $(this).attr('class')
    let splitArray = spanClass.split("n");
    let modal = document.getElementsByClassName(splitArray[1])[0];
    modal.style.display = "none";
}

// Open selected modals
let openModal = function (){
    let buttonId = $(this).attr("id");
    let modal = document.getElementsByClassName(buttonId)[0];
    modal.style.display = "block";
};

//Give each modal unique class name
$(deleteModal).each(function() {
    modalNum++;
    $(this).addClass(String(modalNum));
})

// Give each button unique id
$(deleteButton).each(function() {
    buttonNum++;
    $(this).attr("id", buttonNum);
    $(this).on('click', openModal);
})

//Give each span unique class name
$(span).each(function() {
    spanNum++;
    $(this).addClass('span' + String(spanNum));
    $(this).on('click', closeSpan);
})


// Materialize select validation bug fix from Code Institute
validateMaterializeSelect();
function validateMaterializeSelect() {
    let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
    let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
    if ($("select.validate").prop("required")) {
        $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
    }
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
        $(this).parent(".select-wrapper").on("change", function () {
            if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                $(this).children("input").css(classValid);
            }
        });
    }).on("click", function () {
        if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
            $(this).parent(".select-wrapper").children("input").css(classValid);
        } else {
            $(".select-wrapper input.select-dropdown").on("focusout", function () {
                if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                    if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                        $(this).parent(".select-wrapper").children("input").css(classInvalid);
                    }
                }
            });
        }
    });
}