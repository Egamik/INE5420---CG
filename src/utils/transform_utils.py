
from typing import List, Tuple
from math import sin, cos, degrees, atan, radians as rad

import numpy as np

from enumerators.axis_type import Axis
from utils.math_utils import Point3D, multiplyMatrices

def translate(matrix, t: Point3D) -> np.matrix:
  return multiplyMatrices([matrix, getTranslationMatrix(t)])

def rotateAroundOrigin(matrix: np.matrix, r: int, axis: Axis = Axis.Z) -> np.matrix:
  return multiplyMatrices([matrix, getRotationMatrix(r, axis)])

def rotateAroundPoint(matrix: np.matrix, r: int, point: Point3D, axis: Axis = Axis.Z) -> np.matrix:
  tMatrix = getTranslationMatrix(Point3D(-point.x, -point.y, -point.z))
  rMatrix = getRotationMatrix(r, axis)
  tInvMatrix = getTranslationMatrix(point)
  
  return multiplyMatrices([matrix, tMatrix, rMatrix, tInvMatrix])

def scale(matrix: np.matrix, s: Point3D) -> np.matrix:
  return multiplyMatrices([matrix, getScaleMatrix(s)])

def getTranslationMatrix(t: Point3D) -> np.matrix:
  return np.matrix([
    [  1,   0,   0,   0 ],
    [  0,   1,   0,   0 ],
    [  0,   0,   1,   0 ],
    [t.x, t.y, t.z,   1 ]
  ])


def getRotationMatrix(r: int, axis: Axis) -> np.matrix:
  # X Axis
  if (Axis.X == axis):
    rotationMatrix = np.matrix([
      [           1,            0,            0,            0 ],
      [           0,  cos(rad(r)),  sin(rad(r)),            0 ],
      [           0, -sin(rad(r)),  cos(rad(r)),            0 ],
      [           0,            0,            0,            1 ]
    ])

  # Y Axis
  elif (Axis.Y == axis):
    rotationMatrix = np.matrix([
      [ cos(rad(r)),            0, -sin(rad(r)),            0 ],
      [           0,            1,            0,            0 ],
      [ sin(rad(r)),            0,  cos(rad(r)),            0 ],
      [           0,            0,            0,            1 ]
    ])

  # Z Axis
  elif (Axis.Z == axis):
    rotationMatrix = np.matrix([
      [  cos(rad(r)),  sin(rad(r)),            0,            0 ],
      [ -sin(rad(r)),  cos(rad(r)),            0,            0 ],
      [            0,            0,            1,            0 ],
      [            0,            0,            0,            1 ]
    ]) 
  
  return rotationMatrix

def getScaleMatrix(s: Point3D) -> np.matrix:
  return np.matrix([
    [s.x,   0,   0,   0 ],
    [  0, s.y,   0,   0 ],
    [  0,   0, s.z,   0 ],
    [  0,   0,   0,   1 ]
  ])

def getCenterMatrixPoint(matrices: List[np.matrix]) -> Point3D:
  numMatrices = len(matrices)
  if (numMatrices <= 0): return

  positionSum:Point3D = Point3D()
  for matrix in matrices:
    positionSum = Point3D(positionSum.x + matrix.item(0), positionSum.y + matrix.item(1), positionSum.z + matrix.item(2))
  return Point3D(positionSum.x / numMatrices, positionSum.y / numMatrices, positionSum.z / numMatrices)