from typing import Tuple
from base.graphic_obj import *
from base.bezier import BezierCurve
from base.bspline import BSpline
from base.object3d import Object3D

def formatObject(points: List, type: GraphicObjectType, count: int, name: str='', color: QColor=QColor('black')) -> Tuple[GraphicObject, int]:
 
    count += 1
    if (type == GraphicObjectType.BezierCurve):
        if name != '':
            return (BezierCurve(name, color, points), count)
        return (BezierCurve("bcurve" + str(count), color, points), count)
    
    elif (type == GraphicObjectType.Object3D):
        if name != '':
            return (Object3D(name, points, color), count)
        return (Object3D("3Dobject" + str(count), points, color), count)
    
    elif (type == GraphicObjectType.BSpline):
        # TODO: FInish contrutor
        if name != '':
            return (BSpline(name, color, points), count)
        return (BSpline("bspline" +str(count), color, points), count)
    
    if len(points) == 1:
        if name != '':
            return (Point(name, color, points[0]), count)
        return (Point("point " + str(count), color, points[0]), count)
    
    elif len(points) == 2:
        if name != '':
            return (Line(name, color, points[0], points[1]), count)
        return (Line("line " + str(count), color, points[0], points[1]), count)
    
    else:
        # Format points into lines
        formatted = []
        for i in range(len(points) - 1):
            formatted.append(points[i])
            formatted.append(points[i+1])
        formatted.append(points[len(points) - 1])
        formatted.append(points[0])
        
        if name != '':
            return (Polygon(name, color, formatted), count)
        return (Polygon("poli " + str(count), color, formatted), count)