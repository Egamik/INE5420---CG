from graphic_obj import *

def formatObject(points, count) -> GraphicObject:
    count += 1
    if len(points) == 1:
        return Point("p{count}", points[0][0], points[0][1])
    elif len(points) == 2:
        return Line("l{count}", points[0][0], points[0][1], points[1][0], points[1][1])
    else:
        return Polygon('pl{count}', points)