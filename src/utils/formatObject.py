from graphic_obj import *

def formatObject(points: List[Point3D], count: int) -> GraphicObject:
    count += 1
    
    if len(points) == 1:
        return Point(str(count), QColor("black"), points[0])
    
    elif len(points) == 2:
        return Line(str(count), QColor("black"), points[0], points[1])
    
    else:
        return Polygon(str(count), QColor("black"), points)