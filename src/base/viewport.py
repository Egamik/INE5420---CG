from typing import List
from base.point import Point3D
from base.graphic_obj import GraphicObject
from base.projection import CameraProjection
from utils.view_transform import Transform


class Viewport:
    def __init__(self, 
                x: int,
                y: int,
                width: int,
                height: int,
                projection: CameraProjection = CameraProjection.PARALLEL
    ):
        # View center cartesian
        self.x:int = int(x)
        self.y:int = int(y)
        # Viewport transformation and projection data
        self.focus_point = Point3D()
        self.projection_type = projection
        self.transformations = Transform()
        # Canva dimensions
        self.width:int = int(width)
        self.height:int = int(height)
        self.objList: List[GraphicObject] = []

    def addObject(self, obj: GraphicObject):
        self.objList.append(obj)

    def removeObject(self, obj: GraphicObject):
        self.objList.remove(obj)

    def getObjectList(self):
        return self.objList
    
    def setObjectList(self, objects: List[GraphicObject]):
        self.objList = objects

    def pan(self, pan_x: int, pan_y: int):
        self.x += pan_x
        self.y += pan_y
    
    def zoom(self, value: float):
        # self.
        pass

    def clear(self):
        self.objList.clear()
        
    def setProjectionType(self, projection: CameraProjection):
        self.projection_type = projection