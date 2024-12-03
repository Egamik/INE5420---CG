from typing import List, Tuple

from PyQt5.QtGui import QPainter, QColor

from enumerators.graphic_object_type import GraphicObjectType
from model.base_object import GraphicObject
from utils.math_utils import Point3D
from utils.window_utils import viewportTransform
from core.viewport import Viewport
from core.window import Window

class Object3D(GraphicObject):
  def __init__(self, name: str, edges: List[Tuple[Point3D]], color: QColor):
    self.edges = edges

    points = []
    for edge in self.edges:
      if edge[0] not in points:
        points.append(edge[0])
      if edge[1] not in points:
        points.append(edge[1])
    
    super().__init__(name, GraphicObjectType.Object3D, points, color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    numPoints = len(self.renderPoints)
    if (numPoints <= 0): return
    for i, _ in enumerate(self.renderPoints):
      x1, y1 = viewportTransform(self.renderPoints[i], window, viewport)
      x2, y2 = viewportTransform(self.renderPoints[(i+1) % numPoints], window, viewport)
      painter.drawLine(x1, y1, x2, y2)