---
layout: post
title:  "High-altitude balloon launch"
date:   2014-06-15 10:00:00
categories: balloon
---

The main project of 2013/2014 was to launch a high-altitude balloon into the stratosphere, where it could take photos and video, and to subsequently recover it. The balloon was successfully launched on the 15th June from an airfield near Tewksebury, Cheltenham, and landed near Glastonbury. It reached an altitude of 32 km, and spent about 3 hours in the air.
 
<!--more-->

### Trajectory
<script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
<script>
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

</script>
<div class="map-canvas" id="balloon-trajectory"></div>

### Payload
The main payload carried by the balloon contained two flight computers. The first was an [LPCXpresso](http://www.lpcware.com/lpcxpresso) microcontroller fitted with an ARM processor. This interfaced with the environmental sensors (barometers, thermometers et cetera) and the GPS receiver and relayed the data via radio. We then received this data using a portable radio receiver and uploaded it to the [habhub](http://habhub.org/) server, where it could be corroborated with other tracking data and plotted on a map. See Richard Meadows' [github](https://github.com/richardeoin/buseds-hab/tree/master/lpc-src) page for the lpc source code. The second computer was an mBed, which also received data from the GPS module and sent it via a GSM modem to an ordinary mobile phone, telling us where the balloon was. Unfortunately, this computer failed for some reason, but it wasn't essential.

The balloon was also equipped with two cameras; a GoPro Hero 3 mounted to the bottom capturing 1080p footage at 30 fps and an ordinary Canon point-and-shoot programmed to take photos every 15 seconds. For the latter, we opted for the [Canon Hack Development Kit (CHDK)](http://chdk.wikia.com/wiki/CHDK), an open source custom firmware for Canon cameras.

### Data
