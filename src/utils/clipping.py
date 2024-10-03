from typing import List
from base.point import Point3D, Point2D

INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def applyClipping(points: List[Point3D], boundaries: List[Point2D], clip: bool):

    if len(points) == 1:
        print('Clip point')
        if points[0].x < boundaries[0].x or points[0].x > boundaries[1].x:
            return []
        elif points[0].y < boundaries[0].y or points[0].y > boundaries[1].y:
            return []
        else:
            return points
        
    elif len(points) == 2:
        if clip:
            print('Clip line Cohen-Sutherland')
            new_points = cohenSutherland(boundaries, points[0], points[1])
            if len(new_points) != 0:
                to3d = [Point3D(round(new_points[0].x), round(new_points[0].y), 1), Point3D(round(new_points[1].x), round(new_points[1].y), 1)]
                return to3d
            return []
        else:
            print('Clip line Liang-Barsky')
            new_points = liangBarsky(boundaries, points[0], points[1])
            if len(new_points) == 2:
                return [Point3D(round(new_points[0].x), round(new_points[0].y), 1), Point3D(round(new_points[1].x), round(new_points[1].y), 1)]
            return []
            
    else:
        print('Clip poli')
        new_points = sutherlandHodman(points, boundaries)
        gambs = []
        for point in new_points:
            print('x: ', point.x, ' y: ', point.y)
            gambs.append(Point3D(round(point.x), round(point.y), 1))
        return gambs

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
    # x_min = bounds[0].x
    # y_min = bounds[1].y
    # x_max = bounds[1].x
    # y_max = bounds[0].y
    p_min = Point2D(bounds[0].x, bounds[1].y)
    p_max = Point2D(bounds[1].x, bounds[0].y)
    print('pmin: ', p_min.x, '  ', p_min.y)
    print('pmax: ', p_max.x, '  ', p_max.y)
    print('start: ', start_point.x, ' ', start_point.y)
    print('end: ', end_point.x, ' ', end_point.y)
    
    new_start = start_point
    new_end = end_point
    start_rc: int = getRegionCode(start_point, p_min, p_max)
    end_rc: int = getRegionCode(end_point, p_min, p_max)

    while True:
        print('CohenSutherland s_rc: ', start_rc, '\te_rc: ', end_rc)
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
                new_x = start_point.x + (end_point.x - start_point.x) * (p_max.y - start_point.y) / (end_point.y - start_point.y)
                new_y = p_max.y
            
            elif code_out & BOTTOM:
                new_x = start_point.x + (end_point.x - start_point.x) * (p_min.y - start_point.y) / (end_point.y - start_point.y)
                new_y = p_min.y
            
            elif code_out & RIGHT:
                new_y = start_point.y + (end_point.y - start_point.y) * (p_max.x - start_point.x) / (end_point.x - start_point.x)
                new_x = p_max.x
            
            elif code_out & LEFT:
                new_y = start_point.y + (end_point.y - start_point.y) * (p_min.x - start_point.x) / (end_point.x - start_point.x)
                new_x = p_min.x
            
            new_point = Point2D(new_x, new_y)
            new_code = getRegionCode(new_point, p_min, p_max)

            if code_out == start_rc:
                new_start = new_point
                start_rc = new_code

            else:
                new_end = new_point
                end_rc = new_code

def liangBarsky(bounds: List[Point2D], start_point: Point3D, end_point: Point3D) -> List[Point2D]:
    x_min = bounds[0].x
    y_min = bounds[1].y
    x_max = bounds[1].x
    y_max = bounds[0].y

    delta_x: int = round(end_point.x - start_point.x)
    delta_y: int = round(end_point.y - start_point.y)

    p = [-delta_x, delta_x, -delta_y, delta_y]
    q = [start_point.x - x_min, x_max - start_point.x, start_point.y - y_min, y_max - start_point.y]
    t_enter = 0.0
    t_exit = 1.0

    for i in range(len(p)):
        if p[i] == 0:
            # Line is parallel to the boundary
            if q[i] < 0:
                # Line is outside the boundary
                return []
            # If q[i] >= 0, the line is parallel but inside the boundary, so we continue
        else:
            t = q[i] / p[i]
            if p[i] < 0 and t > t_enter:
                t_enter = t
            elif p[i] > 0 and t < t_exit:
                t_exit = t
    
    if t_enter > t_exit:
        return []
    
    new_start = Point2D(start_point.x + t_enter * delta_x, start_point.y + t_enter * delta_y)
    new_end = Point2D(start_point.x + t_exit * delta_x, start_point.y + t_exit * delta_y)

    return [new_start, new_end]


# Clipping poligonos
#TODO mudar tipo de input pra Line
# def getIntersectionPoint(line1: List[Point3D], line2: List[Point3D]) -> Point2D:
#     """
#     Calculates the intersection point between two lines represented by two Point3D points each.
#     Returns the intersection as a Point2D or None if the lines are parallel.
#     """
#     if len(line1) != 2 or len(line2) != 2:
#         print('Error getIntersection. Wrong length of lines')
#         return None

#     p1, p2 = line1[0], line1[1]
#     p3, p4 = line2[0], line2[1]

#     # Numerators for x and y
#     nx = (p1.x * p2.y - p1.y * p2.x) * (p3.x - p4.x) - (p1.x - p2.x) * (p3.x * p4.y - p3.y * p4.x)
#     ny = (p1.x * p2.y - p1.y * p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x * p4.y - p3.y * p4.x)
    
#     # Denominator (checking for parallel lines)
#     den = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)
    
#     if den == 0:
#         # Lines are parallel
#         return None
    
#     # Return the intersection point as a Point2D
#     return Point2D(nx / den, ny / den)

def getIntersectionPoint(line1: List[Point3D], line2: List[Point3D]) -> Point2D:
    """
    Calculates the intersection point between two lines represented by two Point3D points each.
    Returns the intersection as a Point2D or None if the lines are parallel or do not intersect within the segments.
    """
    if len(line1) != 2 or len(line2) != 2:
        print('Error getIntersection. Wrong length of lines')
        return None

    p1, p2 = line1[0], line1[1]
    p3, p4 = line2[0], line2[1]

    # Numerators for x and y
    nx = (p1.x * p2.y - p1.y * p2.x) * (p3.x - p4.x) - (p1.x - p2.x) * (p3.x * p4.y - p3.y * p4.x)
    ny = (p1.x * p2.y - p1.y * p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x * p4.y - p3.y * p4.x)
    
    # Denominator (checking for parallel lines)
    den = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)
    
    # Use a small epsilon to check for parallel lines
    epsilon = 1e-9
    if abs(den) < epsilon:
        # Lines are parallel
        return None
    
    # Calculate the intersection point
    intersection_x = nx / den
    intersection_y = ny / den
    intersection_point = Point2D(intersection_x, intersection_y)

    # Check if the intersection point is within both segments
    if (min(p1.x, p2.x) <= intersection_x <= max(p1.x, p2.x) and
        min(p1.y, p2.y) <= intersection_y <= max(p1.y, p2.y) and
        min(p3.x, p4.x) <= intersection_x <= max(p3.x, p4.x) and
        min(p3.y, p4.y) <= intersection_y <= max(p3.y, p4.y)):
        return intersection_point

    # If the intersection point is outside the bounds of the segments
    return None


def sutherlandHodman(polygon: List[Point3D], bounds: List[Point2D]) -> List[Point3D]:
    """
    Sutherland-Hodgman polygon clipping algorithm.
    Clips a polygon against rectangular bounds and returns the clipped polygon.
    The bounds are given as two Point2D objects: bottom-left and top-right corners.
    """
    
    # def isInside(point: Point3D, edge_start: Point2D, edge_end: Point2D) -> bool:
    #     """ Determines if a point is inside the boundary formed by an edge. """
    #     return (edge_end.x - edge_start.x) * (point.y - edge_start.y) > (edge_end.y - edge_start.y) * (point.x - edge_start.x)
    
    def isInside(point: Point3D, edge_start: Point2D, edge_end: Point2D, edge_index: int) -> bool:
        if edge_index == 0:  # Left edge (x_min)
            return point.x >= edge_start.x
        elif edge_index == 1:  # Top edge (y_max)
            return point.y <= edge_start.y
        elif edge_index == 2:  # Right edge (x_max)
            return point.x <= edge_start.x
        elif edge_index == 3:  # Bottom edge (y_min)
            return point.y >= edge_start.y
        return False
    
    # Defining the boundary edges of the clipping rectangle
    x_min = bounds[0].x
    y_min = bounds[1].y
    x_max = bounds[1].x
    y_max = bounds[0].y
    # Top-left clockwise
    boundaries = [Point2D(x_min, y_max), Point2D(x_max, y_max), Point2D(x_max, y_min), Point2D(x_min, y_min)]
    
    final_poli = polygon.copy()
    
    # Clip polygon against each boundary (left, top, right, bottom)
    for i in range(len(boundaries)):
        next_poli = final_poli.copy()
        final_poli = []
        
        edge_start = boundaries[(i-1) % len(boundaries)]    # Previous boundary edge
        edge_end = boundaries[i]                            # Current boundary edge
        print('Prev bound: ', edge_start.x, ' ,', edge_start.y)
        print('Curr bound: ', edge_end.x, ' ,', edge_end.y)
        for j in range(len(next_poli)):
            curr_edge_start = next_poli[(j-1) % len(next_poli)]
            curr_edge_end = next_poli[j]
            
            print('Prev edge: ', curr_edge_start.x, ' ,', curr_edge_start.y)
            print('Curr edge: ', curr_edge_end.x , ' ,', curr_edge_end.y)
            
            if isInside(curr_edge_end, edge_start, edge_end, i):
                print('Edge end inside')
                if not isInside(curr_edge_start, edge_start, edge_end, i):
                    print('Edge start not inside')
                    # Current edge crosses the boundary, add intersection point
                    intersec = getIntersectionPoint([curr_edge_start, curr_edge_end], [Point3D(edge_start.x, edge_start.y, 1), Point3D(edge_end.x, edge_end.y, 1)])
                    if intersec:
                        final_poli.append(Point3D(intersec.x, intersec.y, 1))
                # Add current point if it's inside
                final_poli.append(curr_edge_end)
            
            elif isInside(curr_edge_start, edge_start, edge_end, i):
                # Edge crosses the boundary, add intersection point
                print('Edge crosses boundary')
                intersec = getIntersectionPoint([curr_edge_start, curr_edge_end], [Point3D(edge_start.x, edge_start.y, 1), Point3D(edge_end.x, edge_end.y, 1)])
                if intersec:
                    final_poli.append(Point3D(intersec.x, intersec.y, 1))
    
    return final_poli