$(document).ready(function() {
    $("#first_name").on("blur", function () {
    // As you click off of first name in registration form
        let first_name = $(this).val();
        if (first_name == ""){
        // If first name input is empty
            $(this).addClass("is-invalid");
            // Show invalid feedback message
        }
        else{
            $(this).removeClass("is-invalid");
            $(this).addClass("is-valid");
            // Remove invalid feedback message and show valid feedback response
        }
    });

    $("#last_name").on("blur", function(){
    // As you click off of last name in registration form
        let last_name = $(this).val();
        if (last_name == ""){
        // If last name input is empty
            $(this).addClass("is-invalid");
        }
        else{
            $(this).removeClass("is-invalid");
            $(this).addClass("is-valid");
        }
    });

    $("#email").on("blur", function(){
    // As you click off of email in registration form
        let email = $(this).val();
        if (email == ""){
        // If email input is empty
            $(this).addClass("is-invalid");
        }
        else{
            $(this).removeClass("is-invalid");
            $(this).addClass("is-valid");
        }
    });

    $("#user_type").on("blur", function(){
    // As you click off of select user type in registration form
        let user_type = $(this).val();
        if (user_type == ""){
        // If user type input is empty
            $(this).addClass("is-invalid");
        }
        else{
            $(this).removeClass("is-invalid");
            $(this).addClass("is-valid");
        }
    });

    $("#password").on("blur", function(){
        // As you click off of password in registration form
            let password = $(this).val();
            if (password == ""){
            // If password input is empty
                $(this).addClass("is-invalid");
            }
            else{
                $(this).removeClass("is-invalid");
                $(this).addClass("is-valid");
            }
        });

    $("#password").on("input", function(){
    // As you input a password
        let password = $(this).val();
        if (password.length < 6){
        // If password is less than 6 characters long
            $("#err1").addClass("text-danger");
            // Show err1 in registration form in red
        }
        else{
            $("#err1").removeClass("text-danger");
            $("#err1").addClass("text-success");
            // Show err1 in green
        }

        var number= new RegExp('[0-9]');
        if(!$(this).val().match(number)){
        // If password doesn't contain a number
            $("#err2").addClass("text-danger");
            // Show err2 in red
        }
        else{
            $("#err2").removeClass("text-danger");
            $("#err2").addClass("text-success");
            // Show err2 in green
        }

        var lowerCase= new RegExp('[a-z]');
        if(!$(this).val().match(lowerCase)){
        // If password doesn't contain a lowercase letter
            $("#err3").addClass("text-danger");
            // Show err3 in red
        }
        else{
            $("#err3").removeClass("text-danger");
            $("#err3").addClass("text-success");
            // Show err3 in green
        }

        var upperCase= new RegExp('[A-Z]');
        if(!$(this).val().match(upperCase)){
        // If password doesn't contain an uppercase letter
            $("#err4").addClass("text-danger");
            // Show err4 in red
        }
        else{
            $("#err4").removeClass("text-danger");
            $("#err4").addClass("text-success");
            // Show err4 in green
        }

        var specialChar= new RegExp('[!$£@&#]');
        if(!$(this).val().match(specialChar)){
        // If password doesn't contain any of the above special characters
            $("#err5").addClass("text-danger");
            // Show err5 in red
        }
        else{
            $("#err5").removeClass("text-danger");
            $("#err5").addClass("text-success");
            // Show err5 in green
        }
    });
    
    $("#repeat_password").on("blur", function(){
        let password = $("#password").val();
        let repeat_password = $(this).val();
        console.log(password + ", " + repeat_password);
        if (repeat_password == ""){
        // If repeat password input is empty
            $(this).addClass("is-invalid");
        }
        else{
            if (password != repeat_password){
            // If password is not the same as repeat password
                $(this).addClass("is-invalid");
            }
            else{
                $(this).removeClass("is-invalid");
                $(this).addClass("is-valid");
            }
        }
    });

    $("#register").on("submit", function(e){
    // As you submit registration form
        $(".alert").hide();
        // Hide any previous showing alerts
        e.preventDefault();
        // Prevent default action of showing empty page that says form has been submitted
        let action = $(this).attr("action");
        $.ajax({
        // Processing the form
            type: "post",
            url: action,
            data: $(this).serialize(),
            success: function (response) {
                $("#register").before(response);
            }
        });
    });

    $("#login").on("submit", function(e){
    // As you submit login form
        $(".alert").hide();
        e.preventDefault();
        let action = $(this).attr("action");
        $.ajax({
            type: "post",
            url: action,
            data: $(this).serialize(),
            success: function(response){
                $("#login").before(response);
            }
        });
    });

    $("#createClass").on("submit", function(e){
    // As you submit create a class form
        $(".alert").hide();
        e.preventDefault();
        let action = $(this).attr("action");
        $.ajax({
            type: "post",
            url: action,
            data: $(this).serialize(),
            success: function(response){
                $("#createClass").before(response);
            }
        });
    });
    
    $("#joinClass").on("submit", function(e){
    // As you submit join a class form
        $(".alert").hide();
        e.preventDefault();
        let action = $(this).attr("action");
        $.ajax({
            type: "post",
            url: action,
            data: $(this).serialize(),
            success: function(response){
                $("#joinClass").before(response);
            }
        });
    });

    $("#takeQuiz").on("submit", function(e){
    // As you submit take a quiz form
        $(".alert").hide();
        e.preventDefault();
        let action = $(this).attr("action");
        $.ajax({
            type: "post",
            url: action,
            data: $(this).serialize(),
            success: function(response){
                $("#takeQuiz").before(response);
            }
        });
    });

 });