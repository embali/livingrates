function openSignUp() {
    $("#signup-modal").modal("show");
};

function closeSignUp() {
    $("#signup-modal").modal("hide");
    $("#signup-modal").html("");
};

function getSignUp(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            if (json["status"] === "done") {
                $("#signup-modal").html(json["signup_modal"]);
                openSignUp();
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

function postSignUp(url) {
    showOverlay();
    updateCSRF();
    $.ajax({
        url: url,
        type: "POST",
        data: {
            signup_form: $("#signup-form").serialize()
        },
        success: function(json) {
            hideOverlay();
            if (json["status"] === "done" ||
                json["status"] === "validation" ||
                json["status"] === "password") {
                $("#signup-modal").html(json["signup_modal"]);
                centerModals();
            }
            else if (json["status"] === "auth") {
                closeSignUp();
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
