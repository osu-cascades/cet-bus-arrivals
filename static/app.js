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
    //route 290
    displayShape(mymap,["p_30", "p_31", "p_746", "p_747", "p_748"],data,'red');
    //route 291
    displayShape(mymap,["p_750","p_745","p_352","p_353"],data,'blue');
    //route 292
    displayShape(mymap,["p_749","p_1116"],data,'green');
    //route 293
    displayShape(mymap,["p_1113","p_1112","p_744792","p_1667","p_1668"],data,'yellow'); 
    //route 3136
    displayShape(mymap,["p_180304","p_176598"],data,'grey');
    //route 3138
    displayShape(mymap,["p_1105","p_176543"],data,'pink');
    //route 3225
    displayShape(mymap,["p_180576","p_9617","p_180573","p_180574","p_111380"],data,'#31FF8F');
    //route 382
    displayShape(mymap,["p_751","p_753","p_176606","p_176607"],data,'#6FFF31');
    //route 4695
    displayShape(mymap,["p_745174"],data,'#31FFEC');
    //route 5917
    displayShape(mymap,["p_1117","p_176608"],data,'#BD31FF');
    //route 710
    displayShape(mymap,["p_1109","p_1124"],data,'#FF31FF');
    //route 711
    displayShape(mymap,["p_1106","p_1123"],data,'#FFCD31');
    //route 712
    displayShape(mymap,["p_1108","p_176539"],data,'#31FFA1');
    //route 713
    displayShape(mymap,["p_1121","p_8009"],data,'#31D3FF');
    //route 714
    displayShape(mymap,["p_1114","p_176595"],data,'#8231FF');
    //route 715
    displayShape(mymap,["p_1110","p_176596"],data,'#4431FF');
    //route 716
    displayShape(mymap,["p_177368","p_177368"],data,'#F631FF');
    //route 740
    displayShape(mymap,["p_744877"],data,'black');

  });
  setInterval(() => displayData(mymap, buslayer, busicon), 1000);
});

function displayShape(mymap, shape_id_list,data,shape_color){
  let polylines = new Map();
  for (shape_id of shape_id_list) {
    polylines.set(shape_id, []);
  }
  for(shape_point of data) {
    if (shape_id_list.includes(shape_point.shape_id)) {
      let point = new L.LatLng(shape_point.shape_pt_lat,shape_point.shape_pt_lon);
      polylines.get(shape_point.shape_id).push(point);
    }
  }
  for (pointlist of polylines) {
    let polyline = new L.polyline(pointlist[1], {
        color: shape_color,
        weight: 3,
        opacity: 0.5,
        smoothFactor: 1
    });
    polyline.addTo(mymap);
  }
}

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
