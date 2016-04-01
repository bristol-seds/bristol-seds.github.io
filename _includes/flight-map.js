/* gmaps initialisation */

function initialize() {
  var mapOptions = {
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.TOP_CENTER
    },
    zoomControl: false,
    streetViewControl: false,
  };

  var map = new google.maps.Map(document.getElementById('flight_map'), mapOptions);

  var ctaLayer = new google.maps.KmlLayer({
    url: '{{ site.url }}{{ page.flight_map }}'
  });
  ctaLayer.setMap(map);
}
google.maps.event.addDomListener(window, 'load', initialize);
