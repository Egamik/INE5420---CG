from base.point import Point3D

class Transform:
  def __init__(self):
    self.position: Point3D = Point3D()
    self.rotation: Point3D = Point3D()
    self.scale: Point3D = Point3D()
