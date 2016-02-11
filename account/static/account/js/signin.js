function openSignIn() {
    $("#signin-modal").modal("show");
};

function closeSignIn() {
    $("#signin-modal").modal("hide");
    $("#signin-modal").html("");
};

function getSignIn(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            if (json["status"] === "done") {
                $("#signin-modal").html(json["signin_modal"]);
                openSignIn();
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

function postSignIn(url) {
    showOverlay();
    updateCSRF();
    $.ajax({
        url: url,
        type: "POST",
        data: {
            signin_form: $("#signin-form").serialize()
        },
        success: function(json) {
            hideOverlay();
            if (json["status"] === "done") {
                $("#user-name").html(json["user_name"]);
                $("#user-menu").html(json["user_menu"]);
                closeSignIn();
            }
            else if (json["status"] === "auth") {
                closeSignIn();
            }
            else if (json["status"] === "validation" ||
                     json["status"] === "user") {
                $("#signin-modal").html(json["signin_modal"]);
                centerModals();
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
