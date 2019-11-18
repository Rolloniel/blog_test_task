$(document).ready(function () {
    var validations = {
            email: [/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/, 'Please enter a valid email address. Example "example@example.com"']
        }, emtpyFieldStr = "That field cannot be empty!",
        successStyle = {
            "border": '2px solid #a4ff70'
        }, errorStyle = {
            "border": '2px solid red'
        }, resetStyte = {
            "border": '1px solid #CCC'
        }, style = resetStyte;

    function validateEmail(email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    $("#id_email").after("<div id='email_check'></div>");

    function validate(email) {
        $("#email_check").text("");
        if (validateEmail(email)) {
            console.log('+');
            $("#email_check").text('                                                                                                                            ');
            $("#id_email").css(successStyle);
        } else {
            console.log('-');
            $("#email_check").text(email + " is not valid.");
            $("#id_email").css(errorStyle);
        }
        return false;
    }

    $('#id_email').blur(function () {
        var email = $(this).val().toLowerCase();
        if (email == '')return;

        $.ajax({
            type: "GET",
            url: "/user/check/email/",
            data: {
                'email': email,
            },
            dataType: "html",
            cache: false,
            success: function (data) {
                if (data == 'true') {
                    $("#id_email").css(errorStyle);
                    $("#email_check").text("Email is already exist");
                } else {
                    $("#id_email").css(successStyle);
                    $("#email_check").text("");
                    validate(email);
                }
            }
        });

    });

    $("#pick-lang").click(function () {
        $('.langs').slideToggle();
    });
    var elements = document.getElementsByTagName("INPUT");
    for (var i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function (e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity(emtpyFieldStr);
                //e.target.style.borderColor='red';
            }
        };
        elements[i].oninput = function (e) {
            e.target.setCustomValidity("");
        };
    }
    $("input[type=email]").change(function () {
        validation = new RegExp(validations['email'][0]);
        if (!validation.test(this.value)) {
            this.setCustomValidity(validations['email'][1]);
            return false;
        } else {
            this.setCustomValidity('');
        }
    });

});
