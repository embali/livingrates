$(window).on("load", function() {
    $("#status-modal").modal("show");
    $("#status-modal").on("shown.bs.modal", function() {
        $("#status-modal").on("hidden.bs.modal", function() {
            window.location.replace("/");
        });
    });
    centerModals();
});
