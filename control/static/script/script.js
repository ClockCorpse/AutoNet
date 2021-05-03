function togglePassword() {
    var checkBox = document.getElementById('change_info');
    $("#change_info").on('change', function() {
        if (checkBox.checked == true) {
            $(".password-field").slideDown("fast");

        } else {
            $(".password-field").slideUp("fast");;
        }
    });
}

$(document).ready(function() {
    togglePassword()
});