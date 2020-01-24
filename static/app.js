let focusedRoute = null;
let polylineLayer;
let routes = new Map();
let info = L.control();
let div;

let route_shapes = {
  'route 290': ["p_30", "p_31", "p_746", "p_747", "p_748"],
  'route 291': ["p_750","p_745","p_352","p_353"],
  'route 292': ["p_749","p_1116"],
  'route 293': ["p_1113","p_1112","p_744792","p_1667","p_1668"],
  'route 3136': ["p_180304","p_176598"],
  'route 3138': ["p_1105","p_176543"],
  'route 4695': ["p_745174"],
  'route 5917': ["p_1117","p_176608"],
  'route 382': ["p_751","p_753","p_176606","p_176607"],
  'route 710': ["p_1109","p_1124"],
  'route 711': ["p_1106","p_1123"],
  'route 712': ["p_1108","p_176539"],
  'route 713': ["p_1121","p_8009"],
  'route 714': ["p_1114","p_176595"],
  'route 715': ["p_1110","p_176596"],
  'route 716': ["p_177368","p_177368"],
  'route 740': ["p_744877"],
  'route 3225': ["p_180576","p_9617","p_180573","p_180574","p_111380"]
};
let route_colors =[
  'red',
  'blue',
  'green',
  'yellow',
  'pink',
  'brown',
  'teal',
  'orange',
  'purple',
  'black',
  '#00DCFF',
  '#FF00AA',
  '#31FF8F',
  '#6FFF3',
  '#31FFEC',
  '#BD31FF',
  '#FF31FF',
  '#31FFA1'
];

document.addEventListener('DOMContentLoaded', function () {
  const mymap = L.map('mapid').setView([44.0583, -121.3154], 13);
  let buslayer = L.layerGroup().addTo(mymap);
  polylineLayer = L.layerGroup().addTo(mymap);
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicnJydWtvIiwiYSI6ImNrMmdiNmV6ODBkejAzY3BoNW90N2RiM3AifQ.P83jUlQTXOXqM5nLW8EhDg'
  }).addTo(mymap);
  //let marker = L.marker([44.0583, -121.3154]).addTo(mymap);
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
  $.getJSON('/shape', function(data) {
    i = 0;
    for (key in route_shapes) {
      color = route_colors[i];
      initializeRoutes(route_shapes[key], data, key);
      drawRoute(mymap, key, color);
      i++;
    }
  });

  info.onAdd = function(mymap){
    div = L.DomUtil.create('div','info');
    info.update()
    return div;
  };

  info.update = function(data){
    div.innerHTML = '<h4>Route Information</h4>' + (data ? '<b>' + data + '</b> <br /><a href = /> Reset Map </a>': 'please click on a route');
  };

  info.addTo(mymap);

  setInterval(() => displayData(mymap, buslayer, busicon), 1000);
});

function clickRoute(mymap, route_id) {
  let shapes = routes.get(route_id);
  let verts = [];
  for (shape of shapes.values()) {
    verts = verts.concat(shape[1]);
  }
  info.update(route_id);
  mymap.fitBounds(verts);
}

function drawRoute(mymap, route_id, color) {
  let pointlists = routes.get(route_id);
  for (pointlist of pointlists) {
    let polyline = new L.polyline(pointlist[1], {
      color: color,
      weight: 3,
      opacity: 0.5,
      smoothFactor: 1
    });
    polyline.on('click', e => clickRoute(mymap, route_id)).addTo(polylineLayer);
  }
}

function initializeRoutes(shape_id_list, data, route_id){
  let polylines = new Map();
  for (let shape_id of shape_id_list) {
    polylines.set(shape_id, []);
  }
  for (let shape_point of data) {
    if (shape_id_list.includes(shape_point.shape_id)) {
      let point = new L.LatLng(shape_point.shape_pt_lat,shape_point.shape_pt_lon);
      polylines.get(shape_point.shape_id).push(point);
    }
  }
  routes.set(route_id, []);
  for (let pointlist of polylines) {
    routes.get(route_id).push(pointlist);
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
       // let marker = L.marker([xx, yy], { icon: busicon[rte], rotationAngle: head, alt: '' + rte }).on('click',clickRoute).addTo(buslayer);
      }
    }
    mymap.invalidateSize();
  });
}
