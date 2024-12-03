
from typing import List

from PyQt5.QtGui import QPainter, QColor

from enumerators.graphic_object_type import GraphicObjectType
from utils.math_utils import Point2D, Point3D
from utils.curve_utils import getGB, blendingFunction, forwardDifferences
from utils.clipping import applyCohenSutherland
from model.base_object import GraphicObject
from utils.window_utils import viewportTransform
from core.viewport import Viewport
from core.window import Window

class BSpline(GraphicObject):
    
  def __init__(self, name: str, points: List[Point3D], color: QColor):
    n = (len(points) - 4) % 3
    if n != 0:
      raise Exception("O numero de pontos deve atender a funcao f(x) = 4 + 3x, com x natural. Alguns valores válidos: 4, 7, 10 e 13")
    
    super().__init__(name, GraphicObjectType.BSpline, points, color)

  def draw(self, painter: QPainter, viewport: Viewport, window: Window):
    numPoints = len(self.renderPoints)
    if (numPoints <= 0): return

    for i in range(numPoints - 3):
      gb = getGB(self.renderPoints[i], self.renderPoints[i + 1], self.renderPoints[i + 2], self.renderPoints[i + 3])

      d = 0.01
      n = 1 / d

      x, y = forwardDifferences(d, gb)
      
      oldX = x[0].item(0)
      oldY = y[0].item(0)

      j = 1
      
      while j < n:
        j += 1

        x[0][0] += x[1][0]
        x[1][0] += x[2][0]
        x[2][0] += x[3][0]

        y[0][0] += y[1][0]
        y[1][0] += y[2][0]
        y[2][0] += y[3][0]

        visiblePoints = applyCohenSutherland(Point2D(oldX, oldY), Point2D(x[0].item(0), y[0].item(0)), window)

        # Outside of the window, should not be rendered
        if (len(visiblePoints) <= 0):
          continue

        x1, y1 = viewportTransform(visiblePoints[0], window, viewport)
        x2, y2 = viewportTransform(visiblePoints[1], window, viewport)
        
        painter.drawLine(x1, y1, x2, y2)

        oldX = x[0][0]
        oldY = y[0][0]
