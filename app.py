from flask import Flask, render_template, url_for, jsonify

import urllib.request
import json
from bs4 import BeautifulSoup

from cet_bus.geo import Segment, Point, Polyline
from cet_bus.bus_routes import enumerate_shapes, guess_route

app = Flask(__name__)

with open('templates/shape.json') as shape_file:
  with open('templates/trips.json') as trips_file:
    shape_json = json.loads(shape_file.read())
    trips_json = json.loads(trips_file.read())
    shapes = enumerate_shapes(trips_json, shape_json)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/app.js')
def js():
  url_for('static', filename='app.js')

@app.route('/buses')
def buses():
  handle = urllib.request.urlopen('http://ridecenter.org:7016')
  json_str = handle.read().decode('utf8')
  soup = BeautifulSoup(json_str, 'html.parser')
  json_obj = json.loads(soup.body.string)
  for bus_record in json_obj:
    bus_record['route'] = str(guess_route(shapes, bus_record))
  print(json_obj)
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
