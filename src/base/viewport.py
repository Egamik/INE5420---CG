from typing import List
from base.axis import Axis
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
        # Canva dimensions
        self.width:int = int(width)
        self.height:int = int(height)
        # View bounds cartesian
        self.x_min = - self.width / 2
        self.y_min = - self.height / 2
        self.x_max = self.width / 2
        self.y_max = self.height / 2
        # Viewport transformation and projection data
        self.focus_point = Point3D()
        self.projection_type = projection
        self.transformations = Transform()
        self.objList: List[GraphicObject] = []
        # gambiarra
        self.camera_position = Point3D()

    def addObject(self, obj: GraphicObject):
        self.objList.append(obj)

    def removeObject(self, obj: GraphicObject):
        self.objList.remove(obj)

    def updateBounds(self):
        self.x_min = - self.width / 2
        self.y_min = - self.height / 2
        self.x_max = self.width / 2
        self.y_max = self.height / 2
        
    def getObjectList(self):
        return self.objList
    
    def setObjectList(self, objects: List[GraphicObject]):
        self.objList = objects

    def pan(self, pan_x: int, pan_y: int):
        self.transformations.position.x += pan_x
        self.transformations.position.y += pan_y
    
    def zoom(self, value: float):
        self.x_min += value
        self.y_min += value
        self.x_max -= value
        self.y_max -= value
        
    def rotate(self, angle: float, axis: Axis):
        rotation = self.transformations.rotation
        if axis == Axis.X:
            rotation.x = (rotation.x + angle)
                
        elif axis == Axis.Y:
            rotation.y = (rotation.y + angle)
        
        elif axis == Axis.Z:
            rotation.z = (rotation.z + angle)
        
        self.transformations.rotation =rotation
        

    def clear(self):
        self.objList.clear()
        
    def setProjectionType(self, projection: CameraProjection):
        self.projection_type = projection