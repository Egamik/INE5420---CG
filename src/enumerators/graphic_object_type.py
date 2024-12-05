from enum import Enum

class GraphicObjectType(Enum):
	Point = "Point"
	Line = "Line"
	Polygon = "Polygon"
	BezierCurve = "BezierCurve"
	BSpline = "BSpline"
	Object3D = "Object3D"