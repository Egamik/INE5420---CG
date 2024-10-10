from base.graphic_obj import *

def formatObject(points: List[Point3D], count: int) -> GraphicObject:
    count += 1
    
    if len(points) == 1:
        return Point(str(count), QColor("black"), points[0])
    
    elif len(points) == 2:
        return Line(str(count), QColor("black"), points[0], points[1])
    
    else:
        # Format points into lines
        formatted = []
        for i in range(len(points) - 1):
            formatted.append(points[i])
            formatted.append(points[i+1])
        formatted.append(points[len(points) - 1])
        formatted.append(points[0])
        
        return Polygon(str(count), QColor("black"), formatted)