from enum import Enum
from typing import List, Tuple

# import abc

class GraphicObjectType(Enum):
  Point = 1
  Line = 2
  Polygon = 3

  def name(self) -> str:
    if self == GraphicObjectType.Point:
      return "Point"
    if self == GraphicObjectType.Line:
      return "Line"
    if self == GraphicObjectType.Polygon:
      return "Polygon"
    else:
      raise "No definition for type "+self

class GraphicObject():
  def __init__(self, name: str, type: GraphicObjectType) -> None:
    self.name = name
    self.type = type

  def getPositions(self):
    return self.points

class Point(GraphicObject):
  def __init__(self, name: str, x: float, y: float) -> None:
    super().__init__(name, GraphicObjectType.Point)
    self.points = [(x, y)]

class Line(GraphicObject):
  def __init__(self, name: str, x1: float, y1: float, x2: float, y2: float) -> None:
    super().__init__(name, GraphicObjectType.Line)
    self.points = [(x1, y1), (x2, y2)]

class Polygon(GraphicObject):
  def __init__(self, name: str, points :List[tuple]) -> None:
    super().__init__(name, GraphicObjectType.Polygon)
    self.points = points