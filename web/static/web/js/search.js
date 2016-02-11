function getSearch(url) {
    var address = $('#search-input').val();

    searchLocation(url, address);
};

function handleClick(e) {
    showOverlay();

    var coords = e.get('coords');

    ymaps.geocode(coords).then(
        function (res) {
            var place = res.geoObjects.get(0).properties;
            var address = place.get('text');
            var kind = place.get('metaDataProperty').GeocoderMetaData.kind;

            if (kind === 'house') {
                $('#search-input').val(address);

                var url = $('#search-form').data('url');

                ymaps.geocode(address).then(
                    function (res) {
                        var coords = res.geoObjects.get(0).geometry.getCoordinates();
                        var place = res.geoObjects.get(0).properties;
                        var address = place.get('text');
                        var kind = place.get('metaDataProperty').GeocoderMetaData.kind;

                        if (kind === 'house') {
                            handleSearch(url, address, coords);
                        }
                        else {
                        }

                        hideOverlay();
                    },
                    function (err) {
                        hideOverlay();

                        getError('Location not found');
                    }
                );
            }

            hideOverlay();
        },
        function (err) {
            hideOverlay();

            getError('Location not found');
        }
    );
};

function searchLocation(url, address) {
    showOverlay();

    ymaps.geocode(address).then(
        function (res) {
            var coords = res.geoObjects.get(0).geometry.getCoordinates();
            var place = res.geoObjects.get(0).properties;
            var address = place.get('text');
            var kind = place.get('metaDataProperty').GeocoderMetaData.kind;

            lrMap.setCenter(coords);

            if (kind === 'house') {
                handleSearch(url, address, coords);
            }
            else {
            }

            hideOverlay();
        },
        function (err) {
            hideOverlay();

            getError('Location not found');
        }
    );
};

function handleSearch(url, address, coords) {
    var lat = coords[0];
    var lng = coords[1];

    $.ajax({
        url: url,
        type: 'GET',
        data: {
            address: address,
            lat: lat,
            lng: lng
        },
        success: function(json) {
            if (json['status'] === 'done') {
                var lat = json['lat'];
                var lng = json['lng'];

                lrMark.geometry.setCoordinates([lat, lng]);

                getData();
            }
        },
        error: function(xhr, errmsg, err) {
            getError('Server error');
        }
    });
};
