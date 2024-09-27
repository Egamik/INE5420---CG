from graphic_obj import *

def formatObject(points: List[Point3D], count) -> GraphicObject:
    count += 1
    if len(points) == 1:
        return Point("p{count}", QColor.black(), points[0])
    elif len(points) == 2:
        return Line("l{count}", QColor.black(), points[0], points[1])
    else:
        return Polygon('pl{count}', QColor.black(), points)