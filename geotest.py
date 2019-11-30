from geo import Point, Segment
import unittest

class TestSegmentMethods(unittest.TestCase):
  def test_distance_to_start_is_zero(self):
    s = Segment(Point(0, 0), Point(1, 1))
    
    dist = s.distance_to(Point(0, 0))
    self.assertEqual(dist, 0)

  def test_distance_to_end_is_zero(self):
    s = Segment(Point(0, 0), Point(1, 1))

    dist = s.distance_to(Point(1, 1))
    self.assertEqual(dist, 0)

  def test_distance_to_1_0_is_sqrt_2_over_2(self):
    s = Segment(Point(0, 0), Point(1, 1))

    dist = s.distance_to(Point(1, 0))
    self.assertEqual(dist, 0.5 * (2.0 ** 0.5))

  def test_distance_to_2_2_is_sqrt_2(self):
    s = Segment(Point(0, 0), Point(1, 1))

    dist = s.distance_to(Point(2, 2))
    self.assertEqual(dist, 2.0 ** 0.5)

if __name__ == '__main__':
  unittest.main()
