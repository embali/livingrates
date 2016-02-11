function getSignOut(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            if (json["status"] === "done") {
                $("#signout-hidden").html(json["signout_hidden"]);
                $("#signout-form").submit();
            }
            else if (json["status"] === "auth") {
                //
            }
            else {
                getError("Server error");
            }
        },
        error: function(xhr, errmsg, err) {
            getError("Server error");
        }
    });
};

function postSignOut(url) {
    showOverlay();
    updateCSRF();
    $.ajax({
        url: url,
        type: "POST",
        data: {
            signout_form: $("#signout-form").serialize()
        },
        success: function(json) {
            hideOverlay();
            if (json["status"] === "done") {
                $("#user-name").html(json["user_name"]);
                $("#user-menu").html(json["user_menu"]);
            }
            else if (json["status"] === "auth") {
                //
            }
            else {
                getError("Server error");
            }
        },
        error: function(xhr, errmsg, err) {
            hideOverlay();
            getError("Server error");
        }
    });
};
