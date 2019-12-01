import json

from geo import Segment, Point, Polyline

# Parse shape.json into a map where keys are shape ids and values are the
# shapes represented as Polylines.
def enumerate_shapes():
  shapes = {}
  shape_to_route = {}
  with open('templates/trips.json') as trips_file:
    trips_json = json.loads(trips_file.read())
    for trip in trips_json:
      shape_to_route[trip["shape_id"]] = trip["route_id"]
  with open('templates/shape.json') as shape_file:
    shape_json = json.loads(shape_file.read())
    for i in range(0, len(shape_json)-1):
      point = Point(shape_json[i]["shape_pt_lat"], shape_json[i]["shape_pt_lon"])
      shape_id = shape_json[i]["shape_id"]
      route_id = shape_to_route[shape_id]
      shapes.setdefault((shape_id, route_id), Polyline([])).points.append(point)
  return shapes

# Get the route that has the closest segment. This is likely to be the route
# that the bus is on.
def guess_route(shapes, bus_record):
  closest_so_far = None
  closest_shape_key = None
  for shape_key, shape in shapes.items():
    try:
      bus_point = Point(
        float(bus_record["latitude"]),
        float(bus_record["longitude"]))
    except ValueError as v:
      # Sometimes the bus won't have a valid lat/lon, so we'll just ignore it
      continue
    closest_seg = shape.closest_segment(bus_point)
    if closest_so_far is None:
      closest_so_far = closest_seg
      closest_shape_key = shape_key
    elif closest_seg.distance_to(bus_point) < closest_so_far.distance_to(bus_point):
      closest_so_far = closest_seg
      closest_shape_key = shape_key
  return closest_shape_key