var lrMap;
var lrMark;

function initMap() {
    ymaps.ready(locateMap);
};

function locateMap() {
    showOverlay();

    resizeMap();

    ymaps.geolocation.get().then(
        function (res) {
            var bounds = res.geoObjects.get(0).properties.get('boundedBy');
            var lat = (bounds[0][0] + bounds[1][0]) / 2;
            var lng = (bounds[0][1] + bounds[1][1]) / 2

            drawMap(lat, lng);

            hideOverlay();
        },
        function (e) {
            ymaps.geocode('Moscow').then(
                function (res) {
                    var lat = res.geoObjects.get(0).geometry.getCoordinates()[0];
                    var lng = res.geoObjects.get(0).geometry.getCoordinates()[1];

                    drawMap(lat, lng);

                    hideOverlay();
                },
                function (err) {
                    hideOverlay();

                    getError('Location not found');
                }
            );
        }
    );
};

function drawMap(lat, lng) {
    lrMap = new ymaps.Map('map', {
        center: [lat, lng],
        zoom: 12,
        controls: []
    });

    lrMap.events.add('click', handleClick);
    lrMap.events.add('boundschange', getData);

    lrMark = new ymaps.Placemark([lat, lng], {}, {
        preset: 'islands#circleDotIcon',
        iconColor: '#ff0000'
    });
    lrMap.geoObjects.add(lrMark);

    ymaps.geocode([lat, lng]).then(
        function (res) {
            var place = res.geoObjects.get(0).properties;
            var address = place.get('text');
            $('#search-input').val(address);
        },
        function (err) {
            getError('Location not found');
        }
    );

    getData();
    resizeMap();
    onResizeHandlers();
};

function resizeMap() {
    var map_div = $('#map');

    offResizeHandlers();

    map_div.width('100%');

    var window_height = $(window).height();
    var header_height = $('#header').outerHeight();
    var footer_height = $('#footer').outerHeight();
    var map_height = window_height - (header_height + footer_height);

    map_div.height(map_height.toString() + 'px');

    try {
        lrMap.container.fitToViewport();
    }
    catch (e) {
    }

    onResizeHandlers();
};

function onResizeHandlers() {
    $(document).on('ready', resizeMap);
    $(window).on('resize', resizeMap);
    $('body').on('resize', resizeMap);
};

function offResizeHandlers() {
    $(document).off('ready', resizeMap);
    $(window).off('resize', resizeMap);
    $('body').off('resize', resizeMap);
};

function getData() {
    lrMap.geoObjects.removeAll();
    lrMap.geoObjects.add(lrMark);

    var zoom = lrMap.getZoom();

    if (zoom >= 16) {
        var bounds = lrMap.getBounds();
        var lat_left = bounds[0][0];
        var lng_lower = bounds[0][1];
        var lat_right = bounds[1][0];
        var lng_upper = bounds[1][1];

        $.ajax({
            url: $('#map').data('url'),
            type: 'GET',
            data: {
                lat_left: lat_left,
                lng_lower: lng_lower,
                lat_right: lat_right,
                lng_upper: lng_upper
            },
            success: function(json) {
                if (json['status'] === 'done') {
                    for (i = 0; i < json['marks'].length; i++) {
                        var lat = json['marks'][i]['lat'];
                        var lng = json['marks'][i]['lng'];
                        var lrCircle = new ymaps.Circle([[lat, lng], 3], {}, {
                            geodesic: true
                        });

                        lrMap.geoObjects.add(lrCircle);
                    }
                }
            },
            error: function(xhr, errmsg, err) {
                getError('Server error');
            }
        });
    }
};

$(document).on('ready', initMap);
