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
}
google.maps.event.addDomListener(window, 'load', initialize);
