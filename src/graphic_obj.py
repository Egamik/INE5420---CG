from enum import Enum
from PyQt5.QtGui import QPainter

import abc

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

class GraphicObject:
  def __init__(self, name: str, type: GraphicObjectType) -> None:
    self.name = name
    self.type = type

  def getPositions(self):
    return self.points

  @abc.abstractmethod
  def draw(self, painter: QPainter, viewport, window):
    pass


class Point(GraphicObject):
  def __init__(self, name: str, x: float, y: float) -> None:
    super().__init__(name, GraphicObjectType.Point)
    self.points = [(x, y)]

  def draw(self, painter: QPainter, viewport, window):
    if (self.points == None): return