var filter = $("#filter");

function hide() {
    filter[0].style.display = 'none';
}

function unhide() {
    filter[0].style.display = 'block';
}

if ($(window).width() < 1024) {
    filter.appendTo('#filter-container');
} else {
    filter.appendTo('#tab-bar');
}

$(window).resize(function () {
    if ($(window).width() < 1024) {
        filter.appendTo('#filter-container');
    } else {
        filter.appendTo('#tab-bar');
    }
});