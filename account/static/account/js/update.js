function openUpdate() {
    $("#update-modal").modal("show");
};

function closeUpdate() {
    $("#update-modal").modal("hide");
    $("#update-modal").html("");
};

function getUpdate(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            if (json["status"] === "done") {
                $("#update-modal").html(json["update_modal"]);
                openUpdate();
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

function postUpdate(url) {
    showOverlay();
    updateCSRF();
    $.ajax({
        url: url,
        type: "POST",
        data: {
            update_form: $("#update-form").serialize()
        },
        success: function(json) {
            hideOverlay();
            if (json["status"] === "done" ||
                json["status"] === "unavailable" ||
                json["status"] === "validation" ||
                json["status"] === "password") {
                $("#user-name").html(json["user_name"]);
                $("#user-menu").html(json["user_menu"]);
                $("#update-modal").html(json["update_modal"]);
                centerModals();
            }
            else if (json["status"] === "redirect") {
                window.location.replace(json["url"]);
            }
            else if (json["status"] === "auth") {
                closeUpdate();
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
