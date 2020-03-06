from flask import Flask, render_template, url_for, jsonify, g

import urllib.request
import json
import sqlite3
from bs4 import BeautifulSoup

from cet_bus.geo import Segment, Point, Polyline
from cet_bus.bus_routes import enumerate_shapes, guess_route

app = Flask(__name__)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('./gtfs.db')
  return db

with open('templates/shape.json') as shape_file:
  with open('templates/trips.json') as trips_file:
    shape_json = json.loads(shape_file.read())
    trips_json = json.loads(trips_file.read())
    shapes = enumerate_shapes(trips_json, shape_json)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/route.show')
def routeShow():
  return render_template('route.html')

@app.route('/app.js')
def js():
  url_for('static', filename='app.js')

@app.route('/buses')
def buses():
  handle = urllib.request.urlopen('http://ridecenter.org:7017/list')
  json_obj = json.loads(handle.read().decode('utf8'))
  cursor = get_db().cursor()
  routes = cursor.execute('''
    select route_short_name, route_id from routes;
  ''')
  route_map = {}
  for route in routes:
    try:
      int_id = int(route[0])
      route_map[int_id] = int(route[1])
    except:
      route_map[route[0]] = int(route[1])
  for bus in json_obj:
    try:
      int_id = int(bus['Route'])
      bus['Route'] = route_map[int_id]
    except:
      bus['Route'] = route_map[bus['Route']]
  response = app.response_class(
    response=json.dumps(json_obj),
    mimetype='application/json'
  )
  return response

@app.route('/stops/<route_id>')
def stops_on_route(route_id):
  cursor = get_db().cursor()
  stops = cursor.execute('''
    select distinct s.stop_id, stop_lat, stop_lon, stop_name from (
      trips t inner join stop_times st on t.trip_id = st.trip_id inner join stops s on s.stop_id = st.stop_id
    ) where route_id = ?;
  ''', (route_id, ))
  json_obj = []
  for stop in stops:
    json_obj.append({
      'stop_id': stop[0],
      'stop_lat': stop[1],
      'stop_lon': stop[2],
      'stop_name': stop[3]
    })

  response = app.response_class(
    response=json.dumps(json_obj),
    mimetype='application/json'
  )

  return response

@app.route('/stops_info/<route_id>')
def stop_info_on_route(route_id):
  cursor = get_db().cursor()
  stops = cursor.execute('''
    select stop_lat,stop_lon,trips.direction_id, stop_sequence,departure_time, trips.route_id, stops.stop_id, trips.trip_headsign, stops.stop_name, trips.trip_id
    from calendar
    join trips on trips.service_id=calendar.service_id
    join routes on trips.route_id=routes.route_id
    join stop_times on trips.trip_id=stop_times.trip_id
    join stops on stop_times.stop_id=stops.stop_id
    where trips.route_id=?
    order by trips.service_id,departure_time,direction_id,cast(shape_dist_traveled as real)
    limit 100000000;
  ''', (route_id, ))
  json_obj = []
  for stop in stops:
    json_obj.append({
      'stop_lat': stop[0],
      'stop_lon': stop[1],
      'direction_id': stop[2],
      'stop_sequence': stop[3],
      'departure_time': stop[4],
      'route_id': stop[5],
      'stop_id': stop[6],
      'trip_headsign': stop[7],
      'stop_name': stop[8],
      'trip_id': stop[9],
    })

  response = app.response_class(
    response=json.dumps(json_obj),
    mimetype='application/json'
  )
  return response


@app.route('/shape')
def shape():
  return render_template('shape.json')

@app.route('/trips')
def trips():
  return render_template('trips.json')

@app.route('/stops.json')
def stops():
  with open('templates/stops.json', 'r') as f:
    stop_json = json.loads(f.read())
    for i, stop in enumerate(stop_json):
      stop['eta'] = str(i % 10) + 'm'
    return json.dumps(stop_json)

@app.route('/index.css')
def css():
  return render_template('index.css')

@app.route('/test')
def test():
  return 'test'
