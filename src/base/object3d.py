from typing import List, Tuple
from PyQt5.QtGui import QColor
from base.point import Point3D
from graphic_obj import GraphicObject, GraphicObjectType

class Object3D(GraphicObject):
    def __init__(self, name: str, edges: List[Tuple[Point3D]], color: QColor):
        super().__init__(name, GraphicObjectType.Object3D, color)
        
        self.edges = edges
        self.points = []
        
        for edge in self.edges:
            if edge[0] not in self.points:
                self.points.append(edge[0])
            if edge[1] not in self.points:
                self.points.append(edge[1])