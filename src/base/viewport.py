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
                projection: CameraProjection=CameraProjection.PARALLEL
    ):
        # View center
        self.x:int = int(x)
        self.y:int = int(y)
        
        self.focus_point = Point3D()
        self.projection_type = projection
        self.transformations = Transform()
        # Canva dimensions
        self.width:int = int(width)
        self.height:int = int(height)
        self.objList: List[GraphicObject] = []
        # View point reference
        # self.vpr = Point3D(0, 0, 100)
        # View rotation angle
        self.rot_angle = 0
        # Origin
        self.center_of_perspective = Point3D()
        # Distance from COP to VP = COP.Z - VPR.Z

    def addObject(self, obj: GraphicObject):
        self.objList.append(obj)

    def removeObject(self, obj: GraphicObject):
        self.objList.remove(obj)

    def getObjectList(self):
        return self.objList
    
    def setObjectList(self, objects: List[GraphicObject]):
        self.objList = objects

    def addToPoints(self, x: int, y: int):
        for obj in self.objList:
            updated_pts = []
            for point in obj.getPoints():
                new_point = Point3D(point.x + x, point.y + y, point.z)
                updated_pts.append(new_point)
            obj.setPoints(updated_pts)

    def multPoints(self, x: int, y: int):
        for obj in self.objList:
            updated_pts = []
            for point in obj.getPoints():
                point_l = list(point)
                point_l[0] = point_l[0] * x
                point_l[1] = point_l[1] * y
                point = tuple(point_l)
                updated_pts.append(point)
            obj.setPoints(updated_pts)

    def clear(self):
        self.objList.clear()