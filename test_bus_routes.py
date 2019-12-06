import json
import unittest

from geo import Point, Segment, Polyline
from bus_routes import enumerate_shapes, guess_route

class TestBusRoutesMethods(unittest.TestCase):
  def test_enumate_shapes_has_correct_keys(self):
    trips = json.loads("""
      [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 1"},
        {"shape_id": 2, "route_id": "route 2"}
      ]
    """)
    shapes = json.loads("""
      [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    """)
    shapes_map = enumerate_shapes(trips, shapes)

    self.assertIn((0, 'route 1'), shapes_map)
    self.assertNotIn((0, 'route 2'), shapes_map)

  def test_enumate_shapes_has_correct_values(self):
    trips = json.loads("""
      [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 1"},
        {"shape_id": 2, "route_id": "route 2"}
      ]
    """)
    shapes = json.loads("""
      [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    """)
    shapes_map = enumerate_shapes(trips, shapes)

    polyline = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(0, 2),
      Point(0, 3)
    ])

    self.assertTrue(shapes_map[(0, 'route 1')] == polyline)

  def test_enumerate_shapes_fails_when_shape_has_many_routes(self):
    trips = json.loads("""
      [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 0, "route_id": "route 2"}
      ]
    """)
    shapes = json.loads("""
      [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0}
      ]
    """)
    with self.assertRaises(ValueError):
      enumerate_shapes(trips, shapes)

  def test_guess_route(self):
    trips_json = json.loads("""
      [
        {"shape_id": 0, "route_id": "route 1"},
        {"shape_id": 1, "route_id": "route 2"}
      ]
    """)
    shapes_json = json.loads("""
      [
        {"shape_pt_lat": 0, "shape_pt_lon": 0, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 1, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 2, "shape_id": 0},
        {"shape_pt_lat": 0, "shape_pt_lon": 3, "shape_id": 0},

        {"shape_pt_lat": 1, "shape_pt_lon": 0, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 1, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 2, "shape_id": 1},
        {"shape_pt_lat": 1, "shape_pt_lon": 3, "shape_id": 1}
      ]
    """)
    shapes = enumerate_shapes(trips_json, shapes_json)

    bus = json.loads('{"latitude": 0.51, "longitude": 0}')
    closest = guess_route(shapes, bus)
    self.assertEqual(closest[1], "route 2")

    bus = json.loads('{"latitude": 0.49, "longitude": 0}')
    closest = guess_route(shapes, bus)
    self.assertEqual(closest[1], "route 1")

if __name__ == '__main__':
  unittest.main()
