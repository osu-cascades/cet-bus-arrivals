from geo import Point, Segment, Polyline
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

  def test_distance_to_n1_n1_is_sqrt_2(self):
    s = Segment(Point(0, 0), Point(1, 1))

    dist = s.distance_to(Point(-1, -1))
    self.assertEqual(dist, 2.0 ** 0.5)

  def test_distance_to_n1_1_is_sqrt_2(self):
    s = Segment(Point(0, 0), Point(1, -1))

    dist = s.distance_to(Point(-1, 1))
    self.assertEqual(dist, 2.0 ** 0.5)

  def test_distance_to_2_n2_is_sqrt_2(self):
    s = Segment(Point(0, 0), Point(1, -1))

    dist = s.distance_to(Point(2, -2))
    self.assertEqual(dist, 2.0 ** 0.5)

class TestPolylineMethods(unittest.TestCase):
  def test_closest_segment_when_point_is_exactly_on_segment(self):
    # Unit square shaped polyline
    square = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(1, 1),
      Point(1, 0)
    ])
    closest = square.closest_segment(Point(0.01, 0.5))
    self.assertEqual(closest, Segment(Point(0, 0), Point(0, 1)))

  def test_closest_segment_when_point_is_near_segment(self):
    # Unit square shaped polyline
    square = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(1, 1),
      Point(1, 0)
    ])
    closest = square.closest_segment(Point(0, 0.5))
    self.assertEqual(closest, Segment(Point(0, 0), Point(0, 1)))

  def test_closest_segment_when_point_is_far_from_segment(self):
    # Unit square shaped polyline
    square = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(1, 1),
      Point(1, 0)
    ])
    closest = square.closest_segment(Point(1000, 0.5))
    self.assertEqual(closest, Segment(Point(1, 1), Point(1, 0)))


  def test_closest_segment_when_choice_is_ambiguous(self):
    # Unit square shaped polyline
    square = Polyline([
      Point(0, 0),
      Point(0, 1),
      Point(1, 1),
      Point(1, 0)
    ])
    # In ambiguous cases, we don't care which segment is picked
    # We're asserting the answer here anyway to document this behavior
    closest = square.closest_segment(Point(0.5, 0.5))
    self.assertEqual(closest, Segment(Point(0, 0), Point(0, 1)))

if __name__ == '__main__':
  unittest.main()
