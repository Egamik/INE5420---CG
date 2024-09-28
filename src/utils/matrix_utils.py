import numpy as np
from typing import List
from math import sin, cos, radians as rad
from base.point import Point3D
from base.axis import Axis

def multiplyMatrices(matrices: List[np.matrix]) -> np.matrix:
    matrix = matrices[0]

    for m in matrices[1:]:
        matrix = matrix @ m

    return matrix

def rotateAroundPoint(matrix: np.matrix, angle: int, point: Point3D, axis: Axis=Axis.Z) -> np.matrix:
    t_matrix = getTranslationMatrix(Point3D(-point.x, -point.y, -point.z))
    r_matrix = getRotationMatrix(angle, axis)
    i_matrix = getTranslationMatrix(point)
    return multiplyMatrices([matrix, t_matrix, r_matrix, i_matrix])

def getTranslationMatrix(t: Point3D) -> np.matrix:
    return np.matrix([
        [  1,   0,   0,   0 ],
        [  0,   1,   0,   0 ],
        [  0,   0,   1,   0 ],
        [t.x, t.y, t.z,   1 ]
    ])

def getScaleMatrix(s: Point3D) -> np.matrix:
  return np.matrix([
    [s.x,   0,   0,   0 ],
    [  0, s.y,   0,   0 ],
    [  0,   0, s.z,   0 ],
    [  0,   0,   0,   1 ]
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