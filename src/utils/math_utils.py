from typing import List
import numpy as np

class Point2D:
  def __init__(self, x: float = 0, y: float  = 0):
    self.x = x
    self.y = y
  
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

class Point3D:
  def __init__(self, x: float = 0, y: float  = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.z == other.z

def getSlope(startPoint: Point2D, endPoint: Point2D) -> float:
  slope = 0
  x = endPoint.x - startPoint.x
  y = endPoint.y - startPoint.y
  if (x != 0):
    slope = y/x
  return slope

def multiplyMatrices(matrices: List[np.matrix]) -> np.matrix:
  matrix = matrices[0]

  for m in matrices[1:]:
    matrix = matrix @ m

  return matrix