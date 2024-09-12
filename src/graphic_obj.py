import abc
from enum import Enum
from typing import List, Tuple
from PyQt5.QtGui import QPainter

class GraphicObjectType(Enum):
    Point = 1
    Line = 2
    Polygon = 3

class GraphicObject():
    def __init__(self, name: str, type: GraphicObjectType) -> None:
        self.name = name
        self.type = type

    def getPoints(self) -> List[Tuple]:
        return self.points
    
    def setPoints(self, points: List[Tuple]):
        self.points = points

class Point(GraphicObject):
    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name, GraphicObjectType.Point)
        self.points = [(x, y)]

class Line(GraphicObject):
    def __init__(self, name: str, x1: float, y1: float, x2: float, y2: float) -> None:
        super().__init__(name, GraphicObjectType.Line)
        self.points = [(x1, y1), (x2, y2)]

class Polygon(GraphicObject):
    def __init__(self, name: str, points :List[tuple]) -> None:
        super().__init__(name, GraphicObjectType.Polygon)
        self.points = points
