from typing import List

from utils.math_utils import Point2D
from window import Window

def applyLiangBarsky(startPoint: Point2D , endPoint: Point2D, window: Window) -> List[Point2D]:
  deltaX: int = endPoint.x - startPoint.x
  deltaY: int = endPoint.y - startPoint.y

  p = [-deltaX, deltaX, -deltaY, deltaY]
  q = [startPoint.x - window.xMin, window.xMax - startPoint.x, startPoint.y - window.yMin, window.yMax - startPoint.y]

  inside = False

  for i in range(len(p)):
      if p[i] == 0 and q[i] < 0:
          inside = True

  if inside:
      return []
      
  negative = [i for i in range(len(p)) if p[i] < 0]
  positive = [i for i in range(len(p)) if p[i] > 0]

  r = [0] * len(negative)

  i = 0
  for index in negative:
      r[i] = q[index] / p[index]
      i += 1
  c1 = max([0] + r)
  
  i = 0
  for index in positive:
      r[i] = q[index] / p[index]
      i += 1
  c2 = min([1] + r)

  if c1 > c2:
      return []

  x1  = startPoint.x  + c1 * deltaX
  y1  = startPoint.y  + c1 * deltaY

  x2  = startPoint.x  + c2 * deltaX
  y2  = startPoint.y  + c2 * deltaY

  lineToRender: List[Point2D] = [Point2D(x1, y1), Point2D(x2, y2)]

  return lineToRender  

