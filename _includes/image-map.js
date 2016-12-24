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
    open_infowindow = null

    // function scope for adding listener
    function add_listener(i) {
      markers[i].addListener('click', function() {
        if (open_infowindow) {  // close old
          open_infowindow.close();
        }
        // open new
        infowindows[i].open(map, markers[i]);
        open_infowindow = infowindows[i];
      });
    }

    // foreach image
    for (img in image_json) {
      this_image = image_json[img];

      var latLng = {lat: this_image["location"]["latitude"],
                    lng: this_image["location"]["longitude"]};

      var contentString = '<p>Taken '+ this_image["human_time"] + '</p>' +
        '<p>' + this_image["location"]["altitude"] + 'm altitude. ' +
        '<a href="{{ page.image_map.page }}#'+this_image["name"]+'">' +
        'View Full Size' +
        '</a></p>' +
        '<a href="{{ page.image_map.page }}#'+this_image["name"]+'">' +
        '<img src="{{ page.image_map.root }}/png_small/'+this_image["name"]+'.png"/>' +
        '</a>';

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

  $.getJSON("{{ page.image_map.json }}", init_markers);
}
google.maps.event.addDomListener(window, 'load', initialize);
