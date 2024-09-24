from typing import List, Tuple
from GUI.viewport import ViewportLayout

INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def applyClipping(points: List[Tuple]):

    return

#TODO: decidir como tratar as coordenadas do QImage
def getRegionCode(point: Tuple, minBound: Tuple, maxBound: Tuple):

    rc = INSIDE

    if point[0] < minBound[0]:
        rc |= LEFT
    elif point[0] > maxBound[0]:
        rc |= RIGHT
    elif point[1] < minBound[1]:
        rc |= BOTTOM
    elif point[1] > maxBound[1]:
        rc |= TOP
    return rc

# Cohen-Sutherland algorithm for Line clipping
def cohenSutherland(viewport: ViewportLayout, start_point: Tuple, end_point: Tuple):
    
    bounds = viewport.getBoundaries()
    x_min = bounds[0][0]
    y_min = bounds[0][1]
    x_max = bounds[1][0]
    y_max = bounds[1][1]

    new_start: Tuple = (0, 0)
    new_end: Tuple = (0, 0)
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
                new_x = start_point[0] + (end_point[0] - start_point[0]) * (y_max - start_point[1]) / (end_point[1] - start_point[1])
                new_y = y_max
            elif code_out & BOTTOM:
                new_x = start_point[0] + (end_point[0] - start_point[0]) * (y_min - start_point[1]) / (end_point[1] - start_point[1])
                new_y = y_min
            elif code_out & RIGHT:
                new_y = start_point[1] + (end_point[1] - start_point[1]) * (x_max - start_point[0]) / (end_point[0] - start_point[0])
                new_x = x_max
            elif code_out & LEFT:
                new_y = start_point[1] + (end_point[1] - start_point[1]) * (x_min - start_point[0]) / (end_point[0] - start_point[0])
                new_x = x_min
            
            new_point = (new_x, new_y)
            new_code = getRegionCode(new_point, bounds[0], bounds[1])

            if code_out == start_rc:
                new_start = new_point
                start_rc = new_code
            else:
                new_end = new_point
                end_rc = new_code

def liangBarsky(viewport: ViewportLayout, start_point: Tuple, end_point: Tuple):
    bounds = viewport.getBoundaries()
    x_min = bounds[0][0]
    y_min = bounds[0][1]
    x_max = bounds[1][0]
    y_max = bounds[1][1]

    delta_x: int = end_point[0] - start_point[0]
    delta_y: int = end_point[1] - start_point[1]

    p = [-delta_x, delta_x, -delta_y, delta_y]
    q = [start_point[0] - x_min, x_max - start_point[0], start_point[1] - y_min, y_max - start_point[1]]
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
    
    new_start = (start_point[0] + t_enter * delta_x, start_point[1] + t_enter * delta_y)
    new_end = (start_point[0] + t_exit * delta_x, start_point[1] + t_exit * delta_y)

    return [new_start, new_end]