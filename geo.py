#  class Polyline:
#    def __init__(self, points):
#      self.points = points
#
#    def closest_segment(self, point):

class Segment:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def distance_to(self, point):
    return 0
