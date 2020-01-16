import json
import unittest

from geo import Point, Segment, Polyline
from bus_routes import *

class TestBusRoutesMethods(unittest.TestCase):
  def test_enumate_shapes_has_correct_keys(self):
    trips = [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 1"},
        {"shape_id": 2, "route_id": "route 2"}
      ]
    shapes = [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    shapes_map = enumerate_shapes(trips, shapes)

    self.assertIn((0, 'route 1'), shapes_map)
    self.assertNotIn((0, 'route 2'), shapes_map)

  def test_enumate_shapes_has_correct_values(self):
    trips = [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 1"},
        {"shape_id": 2, "route_id": "route 2"}
      ]
    shapes = [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    shapes_map = enumerate_shapes(trips, shapes)

    polyline = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(0, 2),
      Point(0, 3)
    ])

    self.assertTrue(shapes_map[(0, 'route 1')] == polyline)

  def test_enumerate_shapes_fails_when_shape_has_many_routes(self):
    trips = [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 0, "route_id": "route 2"}
      ]
    shapes = [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    with self.assertRaises(ValueError):
      enumerate_shapes(trips, shapes)

  def test_guess_route(self):
    trips_json = [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 2"}
      ]
    shapes_json = [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0},

        {"shape_pt_lat": 1, "shape_pt_lon": 0, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 1, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 2, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 3, "shape_id": 1}
      ]
    shapes = enumerate_shapes(trips_json, shapes_json)

    bus = {"latitude": 0.51, "longitude": 0}
    closest = guess_route(shapes, bus)
    self.assertEqual(closest[1], "route 2")

    bus = {"latitude": 0.49, "longitude": 0}
    closest = guess_route(shapes, bus)
    self.assertEqual(closest[1], "route 1")

  def test_route_histo(self):
    trips_json = [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 2"}
      ]
    shapes_json = [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0},

        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 1},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 1},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 2, "shape_id": 1}
      ]
    shapes = enumerate_shapes(trips_json, shapes_json)

    bus_history = [
        {"latitude": 0, "longitude": 0},
        {"latitude": 0, "longitude": 1},
        {"latitude": 0, "longitude": 2},
        {"latitude": 0, "longitude": 3}
      ]
    histo = route_histo(shapes, bus_history)
    self.assertEqual(min(histo, key=lambda x: x[1])[0][1], "route 1")

    bus_history[3] = { "latitude": 1, "longitude": 2 }

    histo = route_histo(shapes, bus_history)
    self.assertEqual(min(histo, key=lambda x: x[1])[0][1], "route 2")

  def test_passes(self):
    route = Polyline([
      Point(0, 0),
      Point(0, 10)
    ])

    stop = Point(0, 5)

    bus_history = [ Point(0, 4), Point(0, 5), Point(0, 6) ]
    p = passes(bus_history, stop, route)
    self.assertTrue(p)

    bus_history = [ Point(0, 6), Point(0, 5), Point(0, 4) ]
    p = passes(bus_history, stop, route)
    self.assertTrue(p)

    bus_history = [ Point(0, 4), Point(0, 3), Point(0, 2) ]
    p = passes(bus_history, stop, route)
    self.assertFalse(p)

    bus_history = [ Point(0, 6), Point(0, 6), Point(0, 6) ]
    p = passes(bus_history, stop, route)
    self.assertFalse(p)

    # Questionable edge case: should this count as passing the stop?
    bus_history = [ Point(0, 5), Point(0, 5), Point(0, 5) ]
    p = passes(bus_history, stop, route)
    self.assertFalse(p)

  def test_passes_with_curvy_road_and_measurement_error(self):
    route = Polyline([
      Point(0, 0),
      Point(0, 0.1),
      Point(0.1, 0.2),
      Point(0.2, 0.2),
      Point(0.3, 0.3),
      Point(0.3, 0.4),
      Point(0.2, 0.5),
      Point(0.1, 0.5),
      Point(0, 0.6)
    ])

    stop = Point(0.1, 0.5)

    bus_history = [Point(0.25, 0.25), Point(0.29, 0.29)]
    p = passes(bus_history, stop, route)
    self.assertFalse(p)
    bus_history = [Point(0, 0), Point(0, 0.6)]
    p = passes(bus_history, stop, route)
    self.assertTrue(p)

if __name__ == '__main__':
  unittest.main()
