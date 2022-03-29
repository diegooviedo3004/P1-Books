$(function() {
    $('#username').on('keypress', function(e) {
        if (e.which == 32){
            return false;
        }
    });
});

$(function() {
    $('#password_confirmation').on('keypress', function(e) {
        if (e.which == 32){
            return false;
        }
    });
});

$(function() {
    $('#password').on('keypress', function(e) {
        if (e.which == 32){
            return false;
        }
    });
});