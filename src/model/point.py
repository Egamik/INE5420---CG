from PyQt5.QtGui import QPainter, QColor

from utils.math_utils import Point3D
from enumerators.graphic_object_type import GraphicObjectType
from model.base_object import GraphicObject
from utils.window_utils import viewportTransform
from viewport import Viewport
from window import Window

class Point(GraphicObject):
  def __init__(self, name: str, point: Point3D, color: QColor):
    super().__init__(name, GraphicObjectType.Point, [point], color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    if (len(self.renderPoints) <= 0): return
    x, y = viewportTransform(self.renderPoints[0], window, viewport)
    painter.drawPoint(x,y)