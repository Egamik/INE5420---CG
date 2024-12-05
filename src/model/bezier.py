from typing import List

import numpy as np
from PyQt5.QtGui import QPainter, QColor

from enumerators.graphic_object_type import GraphicObjectType
from model.base_object import GraphicObject
from utils.math_utils import Point2D, Point3D
from utils.clipping import applyCohenSutherland
from utils.window_utils import viewportTransform
from core.viewport import Viewport
from core.window import Window

BEZIER_MATRIX = np.matrix([
    [-1,  3, -3,  1],
    [ 3, -6,  3,  0],
    [-3,  3,  0,  0],
    [ 1,  0,  0,  0]
])

def blendingFunction(t: float, pointXY: List[List[float]]) -> float:
	matrix = np.matrix([[pow(t, 3), pow(t, 2), t, 1]])
	blending = np.dot(matrix, BEZIER_MATRIX)
	return np.dot(blending, pointXY).item(0)

class BezierCurve(GraphicObject):
	def __init__(self, name: str, points: List[Point3D], color: QColor):
		super().__init__(name, GraphicObjectType.BezierCurve, points, color)
		n = (len(points) - 4) % 3
		if n != 0:
			raise Exception("O numero de pontos deve atender a funcao f(x) = 4 + 3x, com x natural. Alguns valores válidos: 4, 7, 10 e 13")
    

	def draw(self, painter: QPainter, viewport: Viewport, window: Window):
		numPoints = len(self.renderPoints)
		if (numPoints <= 0): return

		for i in range(0, len(self.renderPoints) - 3, 3):
			pointX = [	[self.renderPoints[i].x   ],
						[self.renderPoints[i+1].x ],
						[self.renderPoints[i+2].x ],
						[self.renderPoints[i+3].x ]
            		]
			pointY = [	[self.renderPoints[i].y   ],
						[self.renderPoints[i+1].y ],
						[self.renderPoints[i+2].y ],
						[self.renderPoints[i+3].y ]
					]

			acc = 0.01
			t = 0.0

			while t <= 1.0:
				x1 = blendingFunction(t, pointX)
				y1 = blendingFunction(t, pointY)

				x2 = blendingFunction(t + acc, pointX)
				y2 = blendingFunction(t + acc, pointY)

				t += acc

				visiblePoints: List[Point2D] = applyCohenSutherland(Point2D(x1, y1), Point2D(x2, y2), window)

				# Outside of the window, should not be rendered
				if (len(visiblePoints) <= 0):
					continue

				x1, y1 = viewportTransform(visiblePoints[0], window, viewport)
				x2, y2 = viewportTransform(visiblePoints[1], window, viewport)
        
				painter.drawLine(x1, y1, x2, y2)
        