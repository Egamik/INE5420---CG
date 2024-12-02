from typing import List

from enumerators.graphic_object_type import GraphicObjectType
from enumerators.clipping_type import ClippingLineAlgorithm
from utils.math_utils import Point2D, Point3D
from utils.clipping.cohen_sutherland import applyCohenSutherland
from utils.clipping.liang_barsky import applyLiangBarsky
from utils.clipping.sutherland_hodgman import applySutherlandHodgman
from window import Window

def applyClipping(objectType: GraphicObjectType, points: List[Point3D], window: Window) -> List[Point2D]:

  points = list(map(lambda p: Point2D(p.x, p.y), points))

  # Point clipping
  if GraphicObjectType.Point == objectType:
    return applyPointClipping(points[0], window)

  # Line clipping
  elif GraphicObjectType.Line == objectType:
    if window.activeCamera.lineClippingType == ClippingLineAlgorithm.CohenSutherland:
      return applyCohenSutherland(points[0], points[1], window)
    elif window.activeCamera.lineClippingType == ClippingLineAlgorithm.LiangBarsky:
      return applyLiangBarsky(points[0], points[1], window)
   
  # Polygon clipping
  elif GraphicObjectType.Polygon == objectType:
    clippingPolygon: List[Point2D] = [
      Point2D(window.xMin, window.yMin), 
      Point2D(window.xMin, window.yMax),
      Point2D(window.xMax, window.yMax),
      Point2D(window.xMax, window.yMin)
    ]
    return applySutherlandHodgman(points, clippingPolygon)

  return points

def applyPointClipping(point: Point2D, window: Window) -> List[Point2D]:
  if point.x > window.xMin and point.x < window.xMax and point.y > window.yMin and point.y < window.yMax:
    return [point] # Inside window
  return [] # Outside window