import numpy as np
from typing import List
from PyQt5.QtGui import QColor
from base.graphic_obj import GraphicObject, GraphicObjectType
from base.point import Point2D, Point3D

BSPLINE_MATRIX = np.matrix([
    [-1/6, 1/2,  -1/2, 1/6],
    [1/2,   -1,   1/2,   0],
    [-1/2,   0,   1/2,   0],
    [1/6,   2/3,  1/6,   0]
])

def forwardDifferences(d: float, gb_x: List[float], gb_y: List[float]):
    matrix = np.matrix([
        [0,           0,           0, 1],
        [pow(d, 3),   pow(d, 2),   d, 0],
        [6*pow(d, 3), 2*pow(d, 2), 0, 0],
        [6*pow(d, 3), 0,           0, 0]
    ])

    cX: np.matrix = np.dot(BSPLINE_MATRIX, gb_x)
    cY: np.matrix = np.dot(BSPLINE_MATRIX, gb_y)

    forwardX = np.dot(matrix, cX)
    forwardY = np.dot(matrix, cY)

    return forwardX, forwardY

class BSpline(GraphicObject):
    def __init__(self, name: str, color: QColor, points: List[Point3D]):
        super().__init__(name, GraphicObjectType.BSpline, color)
        self.points = points
        self.render_points = []
        n = (len(points) - 4) % 3
        print('BSpline constructor')
        if (n != 0):
            print("Número inválido de pontos, use f(p) = 4 + 3p, p = numero de pontos")
            return
        self.setUpLines()
        
    def getPoints(self) -> List[Point3D]:
        return self.render_points
    
    def setPoints(self, points: List[Point3D]):
        self.render_points = points
    
    def getNormalizedPoints(self) -> List[np.matrix]:
        return list(map(lambda p: np.matrix([p.x, p.y, p.z, 1]), self.render_points))
    
    def setUpLines(self):
        n_points = len(self.points)
        for i in range(n_points - 3):
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
            # step
            d = 0.01
            n = 1/d
            
            x, y = forwardDifferences(d, pointX, pointY)
            
            old_x = x[0].item(0)
            old_y = y[0].item(0)
            j = 1
            
            while j < n:
                j += 1
                
                x[0][0] += x[1][0]
                x[1][0] += x[2][0]
                x[2][0] += x[3][0]

                y[0][0] += y[1][0]
                y[1][0] += y[2][0]
                y[2][0] += y[3][0]
                
                self.render_points.append(Point2D(old_x, old_y))
                self.render_points.append(Point2D(x[0].item(0), y[0].item(0)))
                
                old_x = x[0][0]
                old_y = y[0][0]
                