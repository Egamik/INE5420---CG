from typing import List
from base.point import Point3D, Point2D

INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def applyClipping(points: List[Point3D], boundaries: List[Point2D]):

    if len(points) == 1:
        print('Clip point')
        if points[0].x < boundaries[0].x or points[0].x > boundaries[1].x:
            return []
        elif points[0].y < boundaries[0].y or points[0].y > boundaries[1].y:
            return []
        else:
            return points
        
    elif len(points) == 2:
        #if seila:
        print('Clip line')
        if True:
            new_points = cohenSutherland(boundaries, points[0], points[1])
            if len(new_points) != 0:
                to3d = [Point3D(new_points[0].x, new_points[0].y, 1), Point3D(new_points[1].x, new_points[1].y, 1)]
                return to3d
            return []
        else:
            new_points = liangBarsky(boundaries, points[0], points[1])
            if len(new_points) == 2:
                return [Point3D(new_points[0].x, new_points[1].y, 1)]
            return []
            
    else:
        print('Clip poli')
        new_points = sutherlandHodman(points, boundaries)
        for point in new_points:
            print('x: ', point.x, ' y: ', point.y)
        return new_points

#TODO: decidir como tratar as coordenadas do QImage
def getRegionCode(point: Point3D, minBound: Point2D, maxBound: Point2D):

    rc = INSIDE

    if point.x < minBound.x:
        rc |= LEFT
        
    elif point.x > maxBound.x:
        rc |= RIGHT
    
    elif point.y < minBound.y:
        rc |= BOTTOM
    
    elif point.y > maxBound.y:
        rc |= TOP
    
    return rc

def cohenSutherland(bounds: List[Point2D], start_point: Point3D, end_point: Point3D) -> List[Point2D]:
    """ Algoritmo Cohen-Sutherland para clipping de linhas """
    x_min = bounds[0].x
    y_min = bounds[0].y
    x_max = bounds[1].x
    y_max = bounds[1].y

    new_start = start_point
    new_end = end_point
    start_rc: int = getRegionCode(start_point, bounds[0], bounds[1])
    end_rc: int = getRegionCode(end_point, bounds[0], bounds[1])

    while True:

        if start_rc == 0 and end_rc == 0:
            return [new_start, new_end]
        
        if (start_rc & end_rc) != 0:
            return []

        else:
            new_x = 1
            new_y = 1

            if start_rc != 0:
                code_out = start_rc
            
            else:
                code_out = end_rc

            if code_out & TOP:
                new_x = start_point.x + (end_point.x - start_point.x) * (y_max - start_point.y) / (end_point.y - start_point.y)
                new_y = y_max
            
            elif code_out & BOTTOM:
                new_x = start_point.x + (end_point.x - start_point.x) * (y_min - start_point.y) / (end_point.y - start_point.y)
                new_y = y_min
            
            elif code_out & RIGHT:
                new_y = start_point.y + (end_point.y - start_point.y) * (x_max - start_point.x) / (end_point.x - start_point.x)
                new_x = x_max
            
            elif code_out & LEFT:
                new_y = start_point.y + (end_point.y - start_point.y) * (x_min - start_point.x) / (end_point.x - start_point.x)
                new_x = x_min
            
            new_point = Point2D(new_x, new_y)
            new_code = getRegionCode(new_point, bounds[0], bounds[1])

            if code_out == start_rc:
                new_start = new_point
                start_rc = new_code

            else:
                new_end = new_point
                end_rc = new_code

def liangBarsky(bounds: List[Point2D], start_point: Point3D, end_point: Point3D) -> List[Point2D]:
    x_min = bounds[0].x
    y_min = bounds[0].y
    x_max = bounds[1].x
    y_max = bounds[1].y

    delta_x: int = round(end_point.x - start_point.x)
    delta_y: int = round(end_point.y - start_point.y)

    p = [-delta_x, delta_x, -delta_y, delta_y]
    q = [start_point.x - x_min, x_max - start_point.x, start_point.y - y_min, y_max - start_point.y]
    t_enter = 0.0
    t_exit = 1.0

    for i in range(len(p)):
        if p[i] == 0 and q[i] < 0:
            return []
        else:
            t = q[i] / p[i]
            if p[i] < 0 and t > t_enter:
                t_enter = t
            elif t < t_exit:
                t_exit = t
    
    if t_enter > t_exit:
        return []
    
    new_start = Point2D(start_point.x + t_enter * delta_x, start_point.y + t_enter * delta_y)
    new_end = Point2D(start_point.x + t_exit * delta_x, start_point.y + t_exit * delta_y)

    return [new_start, new_end]

# Clipping poligonos
#TODO mudar tipo de input pra Line
def getIntersectionPoint(line1: List[Point3D], line2: List[Point3D]) -> Point2D:
    # y - y0 = m *(x-x0)
    # y = m * (x-x0) + y0
    # x = ((y-y0)/m) + x0
    if len(line1) != 2 or len(line2) != 2:
        print('Error getIntersection. Wrong len')
        return None
    p1 = line1[0]
    p2 = line1[1]
    p3 = line2[0]
    p4 = line2[1]

    nx = (p1.x * p2.y - p1.y * p2.x) * (p3.x - p4.x) - (p1.x - p2.x) * (p3.x * p4.y - p3.y * p4.x)
    ny = (p1.x * p2.y - p1.y * p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x * p4.y - p3.y * p4.x)
    
    # diferenca dos coeficinetes angulares
    den = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)
    
    # linhas paralelas
    if den == 0:
        return None
    
    return Point2D(nx/den, ny/den)

def sutherlandHodman(polygon: List[Point3D], bounds: List[Point2D]):
    
    def isInside(point: Point3D, edge_start: Point2D, edge_end: Point2D) -> bool:
        return (edge_end.x - edge_start.x) * (point.y - edge_start.y) > (edge_end.y - edge_start.y) * (point.x - edge_start.x)
    
    final_poli = polygon.copy()
    boundaries = [bounds[0], Point2D(bounds[1].x, bounds[0].y), bounds[1], Point2D(bounds[0].x, bounds[1].y)]
    
    for i in range(len(boundaries)):
        next_poli = final_poli.copy()
        final_poli = []
        edge_start = boundaries[i-1]
        edge_end = boundaries[i]
        
        for j in range(len(next_poli)):
            curr_edge_s = next_poli[j-1]
            curr_edge_e = next_poli[j]
            
            if isInside(curr_edge_e, edge_start, edge_end):
                if not isInside(curr_edge_s, edge_start, edge_end):
                    intersec = getIntersectionPoint([edge_start, edge_end], [curr_edge_s, curr_edge_e])
                    final_poli.append(intersec)
            
            elif isInside(curr_edge_s, edge_start, edge_end):
                intersec = getIntersectionPoint([edge_start, edge_end], [curr_edge_s, curr_edge_e])
                final_poli.append(intersec)
    
    return final_poli