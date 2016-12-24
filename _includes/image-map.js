/* gmaps initialisation */

function initialize() {
  var mapOptions = {
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.TOP_CENTER
    },
    zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.LARGE,
      position: google.maps.ControlPosition.TOP_RIGHT
    },
    streetViewControl: true,
    streetViewControlOptions: {
      position: google.maps.ControlPosition.TOP_RIGHT
    }
  };

  var map = new google.maps.Map(document.getElementById('image_map'), mapOptions);

  // include the flight as a kml layer
  var ctaLayer = new google.maps.KmlLayer({
    url: '{{ site.url }}{{ page.flight_map }}'
  });
  ctaLayer.setMap(map);

  // get json for image markers from server
  function init_markers(image_json) {
    markers = []
    infowindows = []

    // function scope for adding listener
    function add_listener(i) {
      markers[i].addListener('click', function() {
        infowindows[i].open(map, markers[i]);
      });
    }

    // foreach image
    for (img in image_json) {
      this_image = image_json[img];

      var latLng = {lat: this_image["location"]["latitude"],
                    lng: this_image["location"]["longitude"]};

      var contentString = this_image["name"];

      infowindows[img] = new google.maps.InfoWindow({
        content: contentString
      });
      markers[img] = new google.maps.Marker({
        position: latLng,
        map: map,
        title: this_image["name"]
      });
      add_listener(img);
    }
  }

  $.getJSON("{{ page.image_json }}", init_markers);

  // markers
  // need to create json file with an entry for each image
  // then thumbnail sized copies for each image
  // then a patchwork of marker thumbnails
  // where should this come from?
}
google.maps.event.addDomListener(window, 'load', initialize);
