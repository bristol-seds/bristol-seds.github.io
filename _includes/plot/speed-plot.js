/*
 * Ground speed and ascent rate plots
 */

//Dimensions of SVG window
var w = 400;
var h = 300;

// Import data
d3.text("{{ page.speed_plot }}", function(text) {
  var rawData2 = d3.csv.parseRows(text);

  parsetime = d3.time.format("%y%m%d-%H:%M:%S").parse;

  var dataGroundSpeed = [];
  var dataAltSpeed = [];
  // Convert non-date values to numbers
  for (var i = 1+3; i < rawData2.length-3; i++) { // ignore top line which is header

    alt_speed = (Number(rawData2[i-3][2]) +
                 Number(rawData2[i-2][2]) +
                 Number(rawData2[i-1][2]) +
                 Number(rawData2[i-0][2]) +
                 Number(rawData2[i+1][2]) +
                 Number(rawData2[i+2][2]) +
                 Number(rawData2[i+3][2]))/7

    dataGroundSpeed.push({"x": parsetime(rawData2[i][0]), "y": Number(rawData2[i][1])});
    dataAltSpeed.push(   {"x": parsetime(rawData2[i][0]), "y": alt_speed});
  }
  dataseries2 = [// {values: dataGroundSpeed, key: "Ground speed",
                 //  color: 'steelblue' },
                 {values: dataAltSpeed,    key: "Ascent Rate",
                  color: 'rgb(44,160,44)'}];

  nv.addGraph(function() {
    var chart2 = nv.models.lineChart().margin({left: 80, right: 40});
    chart2.yAxis.tickFormat(d3.format('.2f'));
    chart2.xAxis.tickFormat(function (d) {
	  return d3.time.format("%H:%M:%S")(new Date(d));
    });
    chart2.xAxis.axisLabel('Time');
    chart2.yAxis.axisLabel('Speed (m/s)');
    chart2.useInteractiveGuideline(true);

    d3.select("#speed-time")
      .attr("width", w).attr("height", h)
      .datum(dataseries2).call(chart2);
    nv.utils.windowResize(function() { chart2.update() });
    return chart2;
  });
});
