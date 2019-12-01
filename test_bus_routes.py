import json
import unittest

from geo import Point, Segment, Polyline
from bus_routes import enumerate_shapes

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

if __name__ == '__main__':
  unittest.main()
