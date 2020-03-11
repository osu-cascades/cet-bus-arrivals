let focusedRoute = null;
let routes = new Map();
let info = L.control();
let infoL = L.control();
let div;
let curr_direction = 0;
let prevstop;
let legend;
let circleArray = {};
let polylineArray = {};
let route_direction ={};

let route_shapes = {
  '290': ["p_30", "p_31", "p_746", "p_747", "p_748"],
  '291': ["p_750","p_745","p_352","p_353"],
  '292': ["p_749","p_1116"],
  '293': ["p_1113","p_1112","p_744792","p_1667","p_1668"],
  '3136': ["p_180304","p_176598"],
  '3138': ["p_1105","p_176543"],
  '4695': ["p_745174"],
  '5917': ["p_1117","p_176608"],
  '382': ["p_751","p_753","p_176606","p_176607"],
  '710': ["p_1109","p_1124"],
  '711': ["p_1106","p_1123"],
  '712': ["p_1108","p_176539"],
  '713': ["p_1121","p_8009"],
  '714': ["p_1114","p_176595"],
  '715': ["p_1110","p_176596"],
  '716': ["p_177368","p_177368"],
  '740': ["p_744877"],
  '3225': ["p_180576","p_9617","p_180573","p_180574","p_111380"]
};

let buslocation = null;

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
  '#6FFF33',
  '#31FFEC',
  '#BD31FF',
  '#FF31FF',
  '#31FFA1'
];

document.addEventListener('DOMContentLoaded', function () {
  const mymap = L.map('mapid').setView([44.0583, -121.3154], 13);
  let buslayer = L.layerGroup().addTo(mymap);
  for (let key in route_shapes){
    polylineArray[key] = L.layerGroup().addTo(mymap);
    //route_direction[key] = 3;
  };

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicnJydWtvIiwiYSI6ImNrMmdiNmV6ODBkejAzY3BoNW90N2RiM3AifQ.P83jUlQTXOXqM5nLW8EhDg'
  }).addTo(mymap);
  let busIcons = [];
  for(var i = 0; i <= 30; ++i){
    let busicon = L.icon({
      iconUrl: '/static/icons/busicon.png',
      shadowUrl: '/static/icons/rnum/r'+i+'.png',
      iconSize:     [32, 32],
      shadowSize:   [32, 32],
      iconAnchor:   [16, 16],
      shadowAnchor: [32, 32],
      popupAnchor:  [0, -10]
    });
    busIcons.push(busicon);
}

  for (let key in polylineArray){
    let route = key;
    $.getJSON('/stops/'+key,function(data){
      for (let stop of data){
        let lat = stop.stop_lat;
        let lon = stop.stop_lon;
        L.marker([lat, lon]).bindPopup("<b>" + stop.stop_name + "</b><br>Your bus will arive in: ???").addTo(polylineArray[route]);
      }
    });

  }

  $.getJSON('/shape', function(data) {
    let i = 0;
    for (let key in route_shapes) {
      color = route_colors[i];
      initializeRoutes(route_shapes[key], data, key);
      drawRoute(mymap, key, color);
      i++;
    }
  });

  info.onAdd = function(){
    div = L.DomUtil.create('div','info');
    info.update_info_box();
    return div;
  };

  info.update_info_box = function(data){
    var button = document.createElement("button");
    button.appendChild(document.createTextNode("Refresh Map"));
    button.addEventListener("click",function(){
      mymap.setView([44.0583, -121.3154], 13);
      for (let key in polylineArray){
          mymap.addLayer(polylineArray[key]);
      }
      info.update_info_box();
    });
    if(data){
      div.innerHTML = '<h4>Route Information</h4><b> route: ' + data + '</b> <br />';
      div.appendChild(button);
    }else{
      div.innerHTML = '<h4>Route Information</h4> please click on a route';
    }
  };

  info.addTo(mymap);

  infoL.onAdd = function(){
    legend = L.DomUtil.create('div', 'info');
    legend.innerHTML = '<h4>Route Legend</h4>';

    for (let key in polylineArray){
      let route_id = key;
      let route_name = document.createElement('p','info');
      route_name.appendChild(document.createTextNode("route " + key+ "\n"));
      route_name.addEventListener("click",function(){
        clickRoute(mymap,route_id)
      });
      legend.appendChild(route_name);
    }
    return legend;
  }
  infoL.addTo(mymap);
  
  for (let id in route_shapes) {
    $.getJSON('/stops/' + id, function(data) {
      for (let stop of data) {
        let i = 0;
        let lat = stop.stop_lat;
        let lon = stop.stop_lon;
        let circle = L.circle([lat, lon], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 100
        }).addTo(polylineArray[id]);
        $.getJSON('stops_info/'+id,function(data){
          for(let stop_info of data){
            let stop_lat = stop_info.stop_lat;
            let stop_lon = stop_info.stop_lon;
            let stop_name = stop_info.stop_name;
            if(lat == stop_lat && lon == stop_lon){
              if(stop_name == 'Hawthorne Station'){
                if (id in circleArray) {
                  circleArray[id].push([circle, stop.stop_id,0]);
                  break;
                } else {
                  circleArray[id] = [];
                  break;
                }
              }else if(stop_name == 'Walmart'){
                if (id in circleArray) {
                  circleArray[id].push([circle, stop.stop_id,1]);
                  break;
                } else {
                  circleArray[id] = [];
                  break;
              }
              }
              else{
                if (id in circleArray) {
                  circleArray[id].push([circle, stop.stop_id,parseInt(stop_info.direction_id)]);
                  break;
                } else {
                  circleArray[id] = [];
                  break;
                  }
              }
            }
          }
        });
        i++;
      }
    });
    
  }
  setInterval(() => displayData(mymap, buslayer, busIcons), 1000);
});

function clickRoute(mymap, route_id) {
  let shapes = routes.get(route_id);
  let verts = [];
  for (let shape of shapes.values()) {
    verts = verts.concat(shape[1]);
  }
  info.update_info_box(route_id);
  for (let key in polylineArray){
    if(key == route_id){
      mymap.addLayer(polylineArray[key]);
    }
    if(key != route_id){
      mymap.removeLayer(polylineArray[key]);
    }
  }
  mymap.fitBounds(verts);
}

function drawRoute(mymap, route_id, color) {
  let pointlists = routes.get(route_id);
  for (let pointlist of pointlists) {
    let polyline = new L.polyline(pointlist[1], {
      color: color,
      weight: 3,
      opacity: 0.5,
      smoothFactor: 1
    });

    polyline.on('click', e => clickRoute(mymap, route_id)).addTo(polylineArray[route_id]);

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

function displayData(mymap, buslayer, busIcons) {
  let rte = 1;
  //for (key in polylineArray){
  //}
  $.getJSON('/buses', function(data) {
    buslayer.clearLayers();
    for (let bus of data){
      let x = '-';
      let y = '-';
      let xx = 0.0;
      let yy = 0.0;
      let heading = '-';
      let head = 0.0;
      let start = bus.Route.length -5;
      let end = bus.Route.length - 4;
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
      if (x != '-' && y != '-' && !isNaN(parseInt(bus.Route)) && !isNaN(heading) && !isNaN(head)) {
        let marker = L.marker([xx, yy], {icon: busIcons[rte], rotationAngle: head, alt: '' + bus.Route }).bindPopup("<b> Bus " + bus.bus + " is on Route: "+ bus.Route + "</b>").addTo(buslayer);
        rte++;
        //console.log(rte);
        if(bus.Route) {
          let routetest = parseInt(bus.Route);
          if(routetest in circleArray){   
            if(routetest == 710){
              geofence(mymap, marker, circleArray[routetest],routetest);
              buslocation = {lat: xx,lng: yy};
            }
          }
          else{
           // console.log("route "+routetest+" is not in the listing");
          }
        }
        
        
      }
    }
    mymap.invalidateSize();
  });
}

function detect_direction_change(currstop_id){
  $.getJSON('/stops/710',function(data){
    for (let stop of data){
      let stop_id = stop.stop_id
      if(stop_id == currstop_id){
        if(stop_id == '2456761'){
          curr_direction = 0;
        }
        else if(stop_id == '21004'){
          curr_direction = 1;
        }
      }    
    }
  });
  //return direction;
}

// two circles on top of each other and still finding direction 
// first stop hit is hawthorn staition or the other end point

function geofence(mymap, marker, arr,routetest) {
  for (let [circle,stop_id,direction] of arr) {
    console.log(marker.getLatLng());
    let d = mymap.distance(marker.getLatLng(), circle.getLatLng());
    let inside = d < circle.getRadius();
    let was_inside = buslocation && (mymap.distance(buslocation, circle.getLatLng()) < circle.getRadius());
    if (inside) {
      detect_direction_change(stop_id);
      if(curr_direction == direction){
        if(!was_inside){
           fetch('/arrival', {
          method: 'POST', 
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({stop_id,time:Date.now(),route_id:routetest})
        }) 
      }
        circle.setStyle({
          fillColor: 'green'
        })
      }
    }
    else {
      circle.setStyle({
        fillColor: '#f03'
      })
    }
  }
}