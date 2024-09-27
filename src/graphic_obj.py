from enum import Enum
from typing import List
from PyQt5.QtGui import QColor
from base.point import Point3D

class GraphicObjectType(Enum):
    Point = 1
    Line = 2
    Polygon = 3

class GraphicObject():
    def __init__(self, name: str, type: GraphicObjectType, color: QColor):
        self.name = name
        self.type = type
        self.color = color

    def getPoints(self) -> List[Point3D]:
        return self.points
    
    def setPoints(self, points: List[Point3D]):
        self.points = points

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
