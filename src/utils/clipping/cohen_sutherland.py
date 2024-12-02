from typing import List

from utils.math_utils import Point2D
from window import Window

INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000
    
def applyCohenSutherland(startPoint: Point2D, endPoint: Point2D, window: Window) -> List[Point2D]:
    
  xMin = window.xMin
  yMin = window.yMin
  xMax = window.xMax
  yMax = window.yMax

  startPointRC: int = getRegionCode(startPoint, xMin, yMin, xMax, yMax)
  endPointRC: int = getRegionCode(endPoint, xMin, yMin, xMax, yMax)

  newStartPoint = Point2D(startPoint.x, startPoint.y)
  newEndPoint = Point2D(endPoint.x, endPoint.y)
  
  while True:

    if startPointRC == 0 and endPointRC == 0:
      return [newStartPoint, newEndPoint]
    elif (startPointRC & endPointRC) != 0:
      return []
    else:
      newX = 1
      newY = 1

      if startPointRC != 0:
        rcOut = startPointRC
      else:
        rcOut = endPointRC

      if rcOut & TOP:
        newX = startPoint.x + (endPoint.x - startPoint.x) * \
                        (yMax - startPoint.y) / (endPoint.y - startPoint.y)
        newY = yMax

      elif rcOut & BOTTOM:
        newX = startPoint.x + (endPoint.x - startPoint.x) * \
                          (yMin - startPoint.y) / (endPoint.y - startPoint.y)
        newY = yMin

      elif rcOut & RIGHT:
        newY = startPoint.y + (endPoint.y - startPoint.y) * \
                          (xMax - startPoint.x) / (endPoint.x - startPoint.x)
        newX = xMax

      elif rcOut & LEFT:
        newY = startPoint.y + (endPoint.y - startPoint.y) * \
                          (xMin - startPoint.x) / (endPoint.x - startPoint.x)
        newX = xMin

      newPoint = Point2D(newX, newY)
      newRC = getRegionCode(newPoint, xMin, yMin, xMax, yMax)

      if rcOut == startPointRC:
        newStartPoint = newPoint
        startPointRC = newRC
      else:
        newEndPoint = newPoint
        endPointRC = newRC
  
def getRegionCode(point: Point2D, xMin: int, yMin: int, xMax: int, yMax: int) -> int:
  rc = INSIDE

  if point.x < xMin:
      rc |= LEFT
  elif point.x > xMax:
      rc |= RIGHT
  if point.y < yMin:
      rc |= BOTTOM
  elif point.y > yMax:
      rc |= TOP

  return rc