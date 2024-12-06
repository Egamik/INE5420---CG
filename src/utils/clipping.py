from typing import List

from utils.math_utils import Point2D, Point3D, getSlope
from enumerators.graphic_object_type import GraphicObjectType
from enumerators.clipping_type import ClippingLineAlgorithm
from core.window import Window

# Cohen-Sutherland window zones
INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def applyClipping(objectType: GraphicObjectType, points: List[Point3D], window: Window) -> List[Point2D]:

	points = list(map(lambda p: Point2D(p.x, p.y), points))

	# Point clipping
	if objectType == GraphicObjectType.Point:
		return applyPointClipping(points[0], window)

	# Line clipping
	elif objectType == GraphicObjectType.Line:
		if window.activeCamera.lineClippingType == ClippingLineAlgorithm.CohenSutherland:
			return applyCohenSutherland(points[0], points[1], window)
		elif window.activeCamera.lineClippingType == ClippingLineAlgorithm.LiangBarsky:
			return applyLiangBarsky(points[0], points[1], window)
   
	# Polygon clipping
	else:
		clippingPolygon: List[Point2D] = [
			Point2D(window.x_min, window.y_min), 
			Point2D(window.x_min, window.y_max),
			Point2D(window.x_max, window.y_max),
			Point2D(window.x_max, window.y_min)
		]
		return applySutherlandHodgman(points, clippingPolygon)

	return points

def applyPointClipping(point: Point2D, window: Window) -> List[Point2D]:
	if point.x > window.x_min and point.x < window.x_max and point.y > window.y_min and point.y < window.y_max:
		return [point] # Inside window
	return [] # Outside window

# Cohen-Sutherland line clipping
def applyCohenSutherland(startPoint: Point2D, endPoint: Point2D, window: Window) -> List[Point2D]:
    
	xMin = window.x_min
	yMin = window.y_min
	xMax = window.x_max
	yMax = window.y_max

	start_rc: int = getRegionCode(startPoint, xMin, yMin, xMax, yMax)
	end_rc: int = getRegionCode(endPoint, xMin, yMin, xMax, yMax)

	new_start = Point2D(startPoint.x, startPoint.y)
	new_end = Point2D(endPoint.x, endPoint.y)
  
	while True:

		if start_rc == 0 and end_rc == 0:
			return [new_start, new_end]
		elif (start_rc & end_rc) != 0:
			return []
		else:
			newX = 1
			newY = 1

		if start_rc != 0:
			rc_out = start_rc
		else:
			rc_out = end_rc

		if rc_out & TOP:
			newX = startPoint.x + (endPoint.x - startPoint.x) * \
                        (yMax - startPoint.y) / (endPoint.y - startPoint.y)
			newY = yMax

		elif rc_out & BOTTOM:
			newX = startPoint.x + (endPoint.x - startPoint.x) * \
                          (yMin - startPoint.y) / (endPoint.y - startPoint.y)
			newY = yMin

		elif rc_out & RIGHT:
			newY = startPoint.y + (endPoint.y - startPoint.y) * \
                          (xMax - startPoint.x) / (endPoint.x - startPoint.x)
			newX = xMax

		elif rc_out & LEFT:
			newY = startPoint.y + (endPoint.y - startPoint.y) * \
                          (xMin - startPoint.x) / (endPoint.x - startPoint.x)
			newX = xMin

		newPoint = Point2D(newX, newY)
		newRC = getRegionCode(newPoint, xMin, yMin, xMax, yMax)

		if rc_out == start_rc:
			new_start = newPoint
			start_rc = newRC
		else:
			new_end = newPoint
			end_rc = newRC
  
def getRegionCode(point: Point2D, xMin: int, yMin: int, xMax: int, yMax: int) -> int:
	rc = INSIDE

	if point.x < xMin:
		rc |= LEFT
	elif point.x > xMax:
		rc |= RIGHT
	if point.y < yMin:
		rc |= BOTTOM
	elif point.y > yMax:
		rc |= TOP

	return rc

# Liang-Barsky line clipping
def applyLiangBarsky(start_point: Point2D , end_point: Point2D, window: Window) -> List[Point2D]:
	delta_x: int = end_point.x - start_point.x
	delta_y: int = end_point.y - start_point.y

	p = [-delta_x, delta_x, -delta_y, delta_y]
	q = [start_point.x - window.x_min, window.x_max - start_point.x, start_point.y - window.y_min, window.y_max - start_point.y]

	inside = False

	for i in range(len(p)):
		if p[i] == 0 and q[i] < 0:
			inside = True

	if inside:
		return []
      
	negative = [i for i in range(len(p)) if p[i] < 0]
	positive = [i for i in range(len(p)) if p[i] > 0]

	r = [0] * len(negative)

	i = 0
	for index in negative:
		r[i] = q[index] / p[index]
		i += 1
	c1 = max([0] + r)
  
	i = 0
	for index in positive:
		r[i] = q[index] / p[index]
		i += 1
	c2 = min([1] + r)

	if c1 > c2:
		return []

	x1  = start_point.x  + c1 * delta_x
	y1  = start_point.y  + c1 * delta_y

	x2  = start_point.x  + c2 * delta_x
	y2  = start_point.y  + c2 * delta_y

	lineToRender: List[Point2D] = [Point2D(x1, y1), Point2D(x2, y2)]

	return lineToRender  

# Sutherland-Hodgman polygon clipping 
def applySutherlandHodgman(points: List[Point2D], polygon: List[Point2D]) -> List[Point2D]:
	final_polygon = points.copy()
	
	for i in range(len(polygon)):
		next_poli = final_polygon.copy()
		final_polygon = []
		
		edge_start = polygon[i - 1]
		edge_end = polygon[i]
		
		for j in range(len(next_poli)):
			subjectEdgeStart = next_poli[j - 1]
			subjectEdgeEnd = next_poli[j]
			
			if isInside(edge_start,edge_end,subjectEdgeEnd):
				if not isInside(edge_start, edge_end, subjectEdgeStart):
					intersection = getIntersection(subjectEdgeStart, subjectEdgeEnd, edge_start, edge_end)
					final_polygon.append(intersection)
				final_polygon.append(subjectEdgeEnd)

			elif isInside(edge_start, edge_end, subjectEdgeStart):
				intersection = getIntersection(subjectEdgeStart, subjectEdgeEnd, edge_start, edge_end)
				final_polygon.append(intersection)
	
	return final_polygon
	
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