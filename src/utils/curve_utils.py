from typing import List

import numpy as np

from utils.math_utils import Point2D

BEZIER_MATRIX = np.matrix([
    [-1,  3, -3,  1],
    [ 3, -6,  3,  0],
    [-3,  3,  0,  0],
    [ 1,  0,  0,  0]
])

BSPLINE_MATRIX = np.matrix([
    [-1/6, 1/2,  -1/2, 1/6],
    [1/2,   -1,   1/2,   0],
    [-1/2,   0,   1/2,   0],
    [1/6,   2/3,  1/6,   0]
])

class CurveMatrix():
  def __init__(self, x: List[List[float]], y: List[List[float]]):
      self.x = x
      self.y = y

def getGB(p0: Point2D, p1: Point2D, p2: Point2D, p3: Point2D) -> CurveMatrix:
  gbX = [ [p0.x], [p1.x], [p2.x], [p3.x] ]
  gbY = [ [p0.y], [p1.y], [p2.y], [p3.y] ]

  return CurveMatrix(gbX, gbY)

def blendingFunction(t: float, gb: List[List[float]]) -> float:
  matrix = np.matrix([[pow(t, 3), pow(t, 2), t, 1]])
  blending = np.dot(matrix, BEZIER_MATRIX)
  return np.dot(blending, gb).item(0)

def forwardDifferences(d: float, gb: List[List[float]]):
  matrix = np.matrix([
      [0, 0, 0, 1],
      [pow(d, 3), pow(d, 2), d, 0],
      [6*pow(d, 3), 2*pow(d, 2), 0, 0],
      [6*pow(d, 3), 0, 0, 0]
  ])

  cX: np.matrix = np.dot(BSPLINE_MATRIX, gb.x)
  cY: np.matrix = np.dot(BSPLINE_MATRIX, gb.y)

  forwardX = np.dot(matrix, cX)
  forwardY = np.dot(matrix, cY)

  return forwardX, forwardY