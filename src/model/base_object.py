import abc
from typing import List

from PyQt5.QtGui import QColor

from enumerators.graphic_object_type import GraphicObjectType
from utils.math_utils import Point2D, Point3D
from core.components import Transform

class GraphicObject:
	def __init__(self, name: str, objType: GraphicObjectType, points: List[Point3D], color: QColor) -> None:
		self.name: str = name
		self.type: GraphicObjectType = objType
		self.color: QColor = color
		self.points: List[Point3D] = points
		self.normalizedPoints: List[Point2D] = [None] * len(points) 
		self.renderPoints: List[Point2D] = [None] * len(self.normalizedPoints)
		self.transform: Transform = Transform()
		self.updateTransform()

	def updateTransform(self):
		numPoints = len(self.points)
		if (numPoints <= 0): return

		positionSum:Point3D = Point3D()
		for point in self.points:
			positionSum = Point3D(positionSum.x + point.x, positionSum.y + point.y, positionSum.z + point.z)
		self.transform.position = (positionSum.x / numPoints, positionSum.y / numPoints, positionSum.z / numPoints)

	def getPoints(self) -> List[Point3D]:
		return self.points

	@abc.abstractmethod
	def draw(self, painter, viewport, window):
		pass