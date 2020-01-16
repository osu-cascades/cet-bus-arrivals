from collections import namedtuple

NearestPoint = namedtuple('NearestPoint', 'point t')

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
  def __init__(self, points):
    self.points = points

  def closest_segment(self, point, get_distance=False):
    best = None
    for i in range(0, len(self.points) - 1):
      s = Segment(self.points[i], self.points[i+1])
      d = s.distance_to(point)
      if best is None:
        best = (s, d)
      elif d < best[0].distance_to(point):
        best = (s, d)
    if get_distance:
      return best
    else:
      return best[0]

  def distance_along(self, point):
    nearest_to_point = None
    prev_vertex = None
    for i in range(0, len(self.points) - 1):
      seg = Segment(self.points[i], self.points[i+1])
      n = seg.nearest_point(point)
      if nearest_to_point is None:
        nearest_to_point = n
        prev_vertex = i
      elif point.distance_to(n.point) < point.distance_to(nearest_to_point.point):
        nearest_to_point = n
        prev_vertex = i

    total_dist = 0
    for i in range(0, prev_vertex):
      d = self.points[i].distance_to(self.points[i+1])
      total_dist += d
    total_dist += self.points[prev_vertex].distance_to(nearest_to_point.point)
    return total_dist

  def __eq__(self, other):
    is_eq = True
    for (s, o) in zip(self.points, other.points):
      is_eq = (is_eq and (s == o))
    return is_eq
