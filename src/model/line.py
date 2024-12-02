from typing import List

from PyQt5.QtGui import QPainter, QColor

from utils.math_utils import Point3D
from enumerators.graphic_object_type import GraphicObjectType
from model.base_object import GraphicObject
from utils.window_utils import viewportTransform
from viewport import Viewport
from window import Window

class Line(GraphicObject):
  def __init__(self, name: str, p1: Point3D, p2: Point3D, color: QColor):
    super().__init__(name, GraphicObjectType.Line, [p1, p2], color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    if (len(self.renderPoints) <= 0): return
    x1, y1 = viewportTransform(self.renderPoints[0], window, viewport)
    x2, y2 = viewportTransform(self.renderPoints[1], window, viewport)
    painter.drawLine(x1, y1, x2, y2)