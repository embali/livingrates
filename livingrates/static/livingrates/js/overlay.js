var spinner_opts = {
    lines: 16, // The number of lines to draw
    length: 16, // The length of each line
    width: 10, // The line thickness
    radius: 20, // The radius of the inner circle
    corners: 1, // Corner roundness (0..1)
    rotate: 0, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: "#32C5D2", // #rgb or #rrggbb or array of colors
    speed: 1, // Rounds per second
    trail: 70, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: "spinner", // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: "50%", // Top position relative to parent
    left: "50%" // Left position relative to parent
};
var spinner = new Spinner(spinner_opts);


function showOverlay() {
    var target = document.getElementById("overlay");
    $("#overlay").fadeIn();
    spinner.spin(target);
};

function hideOverlay() {
    spinner.stop();
    $("#overlay").fadeOut();
};
