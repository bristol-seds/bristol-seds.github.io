---
---

//Dimensions of SVG window
var w = 400;
var h = 300;

// Import data
var data2 = [];
d3.text("{{ "speed.csv" | prepend: "http://www.bristol-seds.co.uk/assets/posts/buseds1/" }}", function(text) {
  var rawData2 = d3.csv.parseRows(text);
  console.log(rawData2)

  // Convert non-date values to numbers
  for (var i = 0; i < rawData2.length; i++) {
    data2.push({"x": Number(rawData2[i][0]), "y": Number(rawData2[i][1])})
  }
  dataseries2 = [{"values": data2, "key": "Ground speed", "color": '#ff7f0e'}];

  console.log(dataseries2)
  nv.addGraph(function() {
    var chart = nv.models.lineChart().margin({left: 80, right: 40});
    chart.yAxis.tickFormat(d3.format('d'))
    chart.xAxis.tickFormat(function (d) {
      return d3.time.format("%H:%M:%S")(new Date(d*1000))
    });
    chart.xAxis.axisLabel('Time')
    chart.yAxis.axisLabel('Speed (m/s)')

  d3.select("#speed-time")
    .attr("width", w).attr("height", h)
    .datum(dataseries2).call(chart);
  nv.utils.windowResize(function() { chart.update() });
  return chart;
  });
});


