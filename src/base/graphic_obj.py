from enum import Enum
from typing import List
from PyQt5.QtGui import QColor
from base.point import Point3D, Point2D
import numpy as np

class GraphicObjectType(Enum):
    Point = 1
    Line = 2
    Polygon = 3
    BezierCurve = 4
    Object3D = 5
    BSpline = 6

class GraphicObject():
    def __init__(self, name: str, type: GraphicObjectType, color: QColor):
        self.name: str = name
        self.type: GraphicObjectType = type
        self.color: QColor = color
        self.points: List[Point3D] = None
        self.render_points: List[Point3D] = None
        self.normailzedPoints: List[Point2D] = None

    # Get object's point list
    def getPoints(self) -> List[Point3D]:
        return self.points
    
    # Set object's point list
    def setPoints(self, points: List[Point3D]):
        self.points = points

    # Get list of all object's points matrices  
    def getNormalizedPoints(self) -> List[np.matrix]:
        # return list(map(lambda p: np.matrix([p.x, p.y, p.z, 1]), self.points))
        return list(map(lambda p: np.matrix([p.x, p.y, 1, 1]), self.normailzedPoints))
        
class Point(GraphicObject):
    def __init__(self, name: str, color: QColor, point: Point3D):
        super().__init__(name, GraphicObjectType.Point, color)
        self.points = [point]
        self.render_points = [point]

class Line(GraphicObject):
    def __init__(self, name: str, color: QColor, point1: Point3D, point2: Point3D):
        super().__init__(name, GraphicObjectType.Line, color)
        self.points = [point1, point2]
        self.render_points = [point1, point2]

class Polygon(GraphicObject):
    def __init__(self, name: str, color: QColor, points :List[Point3D]):
        super().__init__(name, GraphicObjectType.Polygon, color)
        self.points = points
        self.render_points = points
