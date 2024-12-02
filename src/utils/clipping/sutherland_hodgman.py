from typing import List

from utils.math_utils import Point2D, getSlope  

def applySutherlandHodgman(points: List[Point2D], clippingPolygon: List[Point2D]) -> List[Point2D]:
    finalPolygon = points.copy()
    
    for i in range(len(clippingPolygon)):
        nextPolygon = finalPolygon.copy()
        finalPolygon = []
        
        clipEdgeStart = clippingPolygon[i - 1]
        clipEdgeEnd = clippingPolygon[i]
        
        for j in range(len(nextPolygon)):
            subjectEdgeStart = nextPolygon[j - 1]
            subjectEdgeEnd = nextPolygon[j]
            
            if isInside(clipEdgeStart,clipEdgeEnd,subjectEdgeEnd):
                if not isInside(clipEdgeStart, clipEdgeEnd, subjectEdgeStart):
                    intersection = getIntersection(subjectEdgeStart, subjectEdgeEnd, clipEdgeStart, clipEdgeEnd)
                    finalPolygon.append(intersection)
                finalPolygon.append(subjectEdgeEnd)

            elif isInside(clipEdgeStart, clipEdgeEnd, subjectEdgeStart):
                intersection = getIntersection(subjectEdgeStart, subjectEdgeEnd, clipEdgeStart, clipEdgeEnd)
                finalPolygon.append(intersection)
    
    return finalPolygon
    
def isInside(p1: Point2D, p2: Point2D, q: Point2D) -> bool:
    R = (p2.x - p1.x) * (q.y - p1.y) - (p2.y - p1.y) * (q.x - p1.x)
    if R <= 0:
        return True
    else:
        return False

def getIntersection(p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D) -> Point2D:
    # First line is vertical
    if p2.x - p1.x == 0:
        x = p1.x
        
        # Slope and intercept of second line
        m2 = getSlope(p3, p4)
        b2 = p3.y - m2 * p3.x
        
        # Intersection
        y = m2 * x + b2
    
    # Second line is vertical
    elif p4.x - p3.x == 0:
        x = p3.x
        
        # Slope and intercept of first line
        m1 = getSlope(p1, p2)
        b1 = p1.y - m1 * p1.x

        # Intersection
        y = m1 * x + b1
    
    # Neither line is vertical
    else:
        # Slope and intercept of first line
        m1 = getSlope(p1, p2)
        b1 = p1.y - m1 * p1.x
        
        # Slope and intercept of second line
        m2 = getSlope(p3, p4)
        b2 = p3.y - m2 * p3.x
    
        # Intersection
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    
    return Point2D(x, y) 