from typing import List

from PyQt5.QtGui import QPainter, QColor

from enumerators.graphic_object_type import GraphicObjectType
from utils.math_utils import Point3D
from model.base_object import GraphicObject
from utils.window_utils import viewportTransform
from viewport import Viewport
from window import Window

class Polygon(GraphicObject):
  def __init__(self, name: str, points: List[Point3D], color: QColor):
    super().__init__(name, GraphicObjectType.Polygon, points, color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    numPoints = len(self.renderPoints)
    if (numPoints <= 0): return
    for i, _ in enumerate(self.renderPoints):
      x1, y1 = viewportTransform(self.renderPoints[i], window, viewport)
      x2, y2 = viewportTransform(self.renderPoints[(i+1) % numPoints], window, viewport)
      painter.drawLine(x1, y1, x2, y2)