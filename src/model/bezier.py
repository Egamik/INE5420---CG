from typing import List

from PyQt5.QtGui import QPainter, QColor

from enumerators.graphic_object_type import GraphicObjectType
from model.base_object import GraphicObject
from utils.math_utils import Point2D, Point3D
from utils.curve_utils import getGB, blendingFunction
from utils.clipping.cohen_sutherland import applyCohenSutherland
from utils.window_utils import viewportTransform
from viewport import Viewport
from window import Window

class BezierCurve(GraphicObject):
  def __init__(self, name: str, points: List[Point3D], color: QColor):
    n = (len(points) - 4) % 3
    if n != 0:
      raise Exception("O numero de pontos deve atender a funcao f(x) = 4 + 3x, com x natural. Alguns valores válidos: 4, 7, 10 e 13")
    
    super().__init__(name, GraphicObjectType.BezierCurve, points, color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    numPoints = len(self.renderPoints)
    if (numPoints <= 0): return

    temp = []
    for i in range(0, len(self.renderPoints) - 3, 3):
      gb = getGB(self.renderPoints[i], self.renderPoints[i + 1], self.renderPoints[i + 2], self.renderPoints[i + 3])

      accuracy = 0.01

      t = 0.0
      while t <= 1.0:
        x1 = blendingFunction(t, gb.x)
        y1 = blendingFunction(t, gb.y)

        x2 = blendingFunction(t + accuracy, gb.x)
        y2 = blendingFunction(t + accuracy, gb.y)

        t += accuracy

        visiblePoints: List[Point2D] = applyCohenSutherland(Point2D(x1, y1), Point2D(x2, y2), window)

        # Outside of the window, should not be rendered
        if (len(visiblePoints) <= 0):
          continue

        x1, y1 = viewportTransform(visiblePoints[0], window, viewport)
        x2, y2 = viewportTransform(visiblePoints[1], window, viewport)
        
        painter.drawLine(x1, y1, x2, y2)
        