from typing import List, Tuple

from enumerators.graphic_object_type import GraphicObjectType
from utils.math_utils import Point3D
from model.base_object import GraphicObject
from model.point import Point
from model.line import Line
from model.polygon import Polygon
from model.bezier import BezierCurve
from model.bspline import BSpline
from model.object3d import Object3D

def instantiateObject(name: str, objType: GraphicObjectType, coordinates: List[Tuple], color) -> GraphicObject:
  if (len(coordinates) <= 0): return

  # Object3D
  if(GraphicObjectType.Object3D == objType):
    lines = list(map(
      lambda p: (Point3D(p[0][0], p[0][1], p[0][2]), Point3D(p[1][0], p[1][1], p[1][2]),), coordinates))
    return Object3D(name, lines, color)

  points = list(map(lambda p: Point3D(p[0], p[1], p[2]) if len(p) > 2 else Point3D(p[0], p[1], 0), coordinates))
  
  # Point
  if(GraphicObjectType.Point == objType):
    return Point(name, points[0], color)

  # Line
  elif(GraphicObjectType.Line == objType):
    return Line(name, points[0], points[1], color)

  # Polygon
  elif(GraphicObjectType.Polygon == objType):
    return Polygon(name, points, color)

  # Bezier Curve
  elif(GraphicObjectType.BezierCurve == objType):
    return BezierCurve(name, points, color)

  # BSpline Curve
  elif(GraphicObjectType.BSpline == objType):
    return BSpline(name, points, color)

def getTypeByPoints(numPoints: int) -> GraphicObjectType:
  if (numPoints == 1):
    return GraphicObjectType.Point
  elif (numPoints == 2):
    return GraphicObjectType.Line
  elif (numPoints == 3):
    return GraphicObjectType.Polygon
  return None
