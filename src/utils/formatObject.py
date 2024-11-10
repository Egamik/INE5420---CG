from typing import Tuple
from base.graphic_obj import *
from base.bezier import BezierCurve
from base.bspline import BSpline
from base.object3d import Object3D

def formatObject(points: List, type: GraphicObjectType, count: int) -> Tuple[GraphicObject, int]:
 
    count += 1
    if (type == GraphicObjectType.BezierCurve):
        return (BezierCurve("bcurve" + str(count), QColor("black"), points), count)
    
    elif (type == GraphicObjectType.Object3D):
        return (Object3D("3Dobject" + str(count), points, QColor("black")), count)
    
    elif (type == GraphicObject.BSpline):
        # TODO: FInish contrutor
        return (BSpline("bspline" +str(count), QColor("black")), count)
    
    if len(points) == 1:
        return (Point("point " + str(count), QColor("black"), points[0]), count)
    
    elif len(points) == 2:
        return (Line("line " + str(count), QColor("black"), points[0], points[1]), count)
    
    else:
        # Format points into lines
        formatted = []
        for i in range(len(points) - 1):
            formatted.append(points[i])
            formatted.append(points[i+1])
        formatted.append(points[len(points) - 1])
        formatted.append(points[0])
        
        return (Polygon("poli " + str(count), QColor("black"), formatted), count)