document.addEventListener('DOMContentLoaded', function () {
  const mymap = L.map('mapid').setView([44.0583, -121.3154], 13);
  let buslayer = L.layerGroup().addTo(mymap);
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicnJydWtvIiwiYSI6ImNrMmdiNmV6ODBkejAzY3BoNW90N2RiM3AifQ.P83jUlQTXOXqM5nLW8EhDg'
  }).addTo(mymap);
  let marker = L.marker([44.0583, -121.3154]).addTo(mymap);
  let busicon = [];

  for (let i = 0; i <= 30; i++) {
    busicon.push(
      L.icon({
        iconUrl: '/static/icons/busicon.png',
        iconSize:     [32, 32],
        iconAnchor:   [16, 16],
        popupAnchor:  [0, -10]
      }));
  }
  $.getJSON('/stops.json', function(data) {
      for (stop of data) {
        let lat = stop.stop_lat;
        let lon = stop.stop_lon;
        L.marker([lat, lon]).bindPopup("<b>" + stop.stop_name + "</b><br>Your bus will arive in: " + stop.eta).addTo(mymap);
      }
    });
  $.getJSON('/shape', function(data){
    let polylines = new Map();
    for (shape_id of ["p_30", "p_31", "p_746", "p_747", "p_748"]) {
      polylines.set(shape_id, []);
    }
    for(shape_point of data) {
      if (["p_30", "p_31", "p_746", "p_747", "p_748"].includes(shape_point.shape_id)) {
        let point = new L.LatLng(shape_point.shape_pt_lat,shape_point.shape_pt_lon);
        polylines.get(shape_point.shape_id).push(point);
      }
    }
    for (pointlist of polylines) {
      let polyline = new L.polyline(pointlist[1], {
          color: 'red',
          weight: 3,
          opacity: 0.5,
          smoothFactor: 1
      });
      polyline.addTo(mymap);
    }
  });
  setInterval(() => displayData(mymap, buslayer, busicon), 1000);
});

function displayData(mymap, buslayer, busicon) {
  $.getJSON('/buses', function(data) {
    buslayer.clearLayers();
    for(bus of data){
      let x = '-';
      let y = '-';
      let xx = 0.0;
      let yy = 0.0;
      let heading = '-';
      let head = 0.0;
      let rte = 0;
      let start = bus.route.length -5;
      let end = bus.route.length - 4;
      if (bus.latitude != null) {
        x = bus.latitude;
        try {
          xx = parseFloat(x);
        } catch (err) {
          x = '-';
          xx = 0.0;
        }
      }
      if (bus.longitude != null) {
        y = bus.longitude;
        try {
          yy = parseFloat(y);
        } catch (err) {
          y = '-';
          yy = 0.0;
        }
      }
      if (bus.heading != null) {
        heading = bus.heading;
        head = parseFloat(heading) + 90;
        if (head > 360) head = head - 360;
      }
      if (bus.Route != null) {
        rte = parseInt(bus.Route);
      }
      if (x != '-' && y != '-' && !isNaN(rte) && !isNaN(heading) && !isNaN(head)) {
        let marker = L.marker([xx, yy], { icon: busicon[rte], rotationAngle: head, alt: '' + rte }).bindPopup("<b> Bus " + bus.busNumber + " is on Route: "+ bus.route.substr(start,end).replace(/\s+|\)/g, '') + "</b>").addTo(buslayer);

      }
    }
    mymap.invalidateSize();
  });
}
