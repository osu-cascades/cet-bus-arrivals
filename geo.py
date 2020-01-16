from collections import namedtuple
from itertools import islice

NearestPoint = namedtuple('NearestPoint', 'point t')

def take(n, iterable):
  return list(islice(iterable, n))

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __add__(self, point):
    return Point(self.x + point.x, self.y + point.y)

  def __sub__(self, point):
    return Point(self.x - point.x, self.y - point.y)

  def dot(self, point):
    return self.x * point.x + self.y * point.y

  def scale(self, c):
    return Point(self.x * c, self.y * c)

  def distance_to(self, point):
    dx = self.x - point.x
    dy = self.y - point.y
    return (dx * dx + dy * dy) ** 0.5

class Segment:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def __eq__(self, other):
    return (self.start == other.start and self.end == other.end)

  def nearest_point(self, point):
    v = self.end - self.start
    u = self.start - point
    t = - (v.dot(u) / v.dot(v))
    if t < 0:
      return NearestPoint(point = self.start, t = t)
    elif t > 1:
      return NearestPoint(point = self.end, t = t)
    else:
      return NearestPoint(point = self.start + v.scale(t), t = t)

  def distance_to(self, point):
    nearest = self.nearest_point(point)
    return nearest.point.distance_to(point)

class Polyline:
  class Segments:
    def __init__(self, points):
      self.i = 0
      self.end = len(points) - 1
      self.points = points
    def __iter__(self):
      return self
    def __next__(self):
      if self.i == self.end:
        raise StopIteration
      else:
        seg = Segment(self.points[self.i], self.points[self.i+1])
        self.i += 1
        return seg

  def __init__(self, points):
    self.points = points

  def segments(self):
    return iter(self.Segments(self.points))

  def closest_segment(self, point, get_distance=False):
    best = None
    for segment in self.segments():
      d = segment.distance_to(point)
      if best is None:
        best = (segment, d)
      elif d < best[0].distance_to(point):
        best = (segment, d)
    if get_distance:
      return best
    else:
      return best[0]

  def distance_along(self, point):
    nearest_to_point = None
    prev_vertex = None
    for i, segment in enumerate(self.segments()):
      n = segment.nearest_point(point)
      if nearest_to_point is None:
        nearest_to_point = n
        prev_vertex = i
      elif point.distance_to(n.point) < point.distance_to(nearest_to_point.point):
        nearest_to_point = n
        prev_vertex = i
    total_dist = 0
    for segment in take(prev_vertex, self.segments()):
      d = segment.start.distance_to(segment.end)
      total_dist += d
    total_dist += self.points[prev_vertex].distance_to(nearest_to_point.point)
    return total_dist

  def __eq__(self, other):
    is_eq = True
    for (s, o) in zip(self.points, other.points):
      is_eq = (is_eq and (s == o))
    return is_eq
