function openReset() {
    $("#reset-modal").modal("show");
};

function closeReset() {
    $("#reset-modal").modal("hide");
    $("#reset-modal").html("");
};

function getReset(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            if (json["status"] === "done") {
                $("#reset-modal").html(json["reset_modal"]);
                openReset();
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

function postReset(url) {
    showOverlay();
    updateCSRF();
    $.ajax({
        url: url,
        type: "POST",
        data: {
            reset_form: $("#reset-form").serialize()
        },
        success: function(json) {
            hideOverlay();
            if (json["status"] === "done" ||
                json["status"] === "unavailable" ||
                json["status"] === "validation") {
                $("#reset-modal").html(json["reset_modal"]);
                centerModals();
            }
            else if (json["status"] === "auth") {
                closeReset();
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
