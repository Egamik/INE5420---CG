import numpy as np
from PyQt5.QtGui import QColor
from base.graphic_obj import GraphicObject, GraphicObjectType
from base.point import Point3D, Point2D
from typing import List

# Coeficientes curva cúbica
BEZIER_MATRIX = np.matrix([
    [-1,  3, -3,  1],
    [ 3, -6,  3,  0],
    [-3,  3,  0,  0],
    [ 1,  0,  0,  0]
])

def blendingFunction(t: float, gb: List[List[float]]) -> float:
    matrix = np.matrix([[pow(t, 3), pow(t, 2), t, 1]])
    blending = np.dot(matrix, BEZIER_MATRIX)
    return np.dot(blending, gb).item(0)

""" Bernstein Polynomial Bezier Curve"""
class BezierCurve(GraphicObject):
    def __init__(self, name: str, color: QColor, points: List[Point3D]):
        super().__init__(name, GraphicObjectType.BezierCurve, color)
        self.points = points
        self.render_points = []
        n = (len(points) - 4) % 3
        print('Bezier constructor')
        if (n != 0):
            print("Número inválido de pontos, use f(p) = 4 + 3p, p = numero de pontos")
            return
        self.curveToLines()
    
    def getPoints(self) -> List[Point3D]:
        return self.render_points
    
    def setPoints(self, points: List[Point3D]):
        self.render_points = points
    
    def getNormalizedPoints(self) -> List[np.matrix]:
        return list(map(lambda p: np.matrix([p.x, p.y, 1, 1]), self.render_points))
    
    def curveToLines(self):
        for i in range(0, len(self.points) - 3 , 3):
            pointX = [ [self.points[i].x  ], 
                       [self.points[i+1].x], 
                       [self.points[i+2].x], 
                       [self.points[i+3].x] 
                    ]
            pointY = [ [self.points[i].y  ], 
                       [self.points[i+1].y], 
                       [self.points[i+2].y], 
                       [self.points[i+3].y] 
                    ]            
            acc = 0.01
            t = 0.0
            print('Beizer loop')
            while t <= 1.0:
                x1 = blendingFunction(t, pointX)
                y1 = blendingFunction(t, pointY)
                
                x2 = blendingFunction(t+acc, pointX)
                y2 = blendingFunction(t+acc, pointY)
                t += acc
                self.render_points.append(Point3D(x1, y1, 1))
                self.render_points.append(Point3D(x2, y2, 1))
        return