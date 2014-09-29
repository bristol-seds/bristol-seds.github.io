function initialize() {
  var bath = new google.maps.LatLng(51.375801,-2.3599039);
  var mapOptions = {
    zoom: 10,
    center: bath 
  }

  var map = new google.maps.Map(document.getElementById('balloon-trajectory'), mapOptions);

  var ctaLayer = new google.maps.KmlLayer({
    url: 'http://www.samhatfield.co.uk/balloon/balloonpath.kml'
  });
  ctaLayer.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initialize);
