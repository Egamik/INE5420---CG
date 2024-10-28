import numpy as np
from GUI.viewport import Viewport
from base.axis import Axis
from base.point import Point3D, Point2D
from utils.matrix_utils import getRotationMatrix, getTranslationMatrix, multiplyMatrices


def transform(matrix: np.matrix, point: Point3D):
    return multiplyMatrices([matrix, getTranslationMatrix(point)])

def rotateAroundOrigin(matrix: np.matrix, angle: int, axis: Axis=Axis.Z):
    return multiplyMatrices([matrix, getRotationMatrix(angle, axis)])

def rotateAroundPoint(matrix: np.matrix, angle: int, point: Point3D, axis: Axis=Axis.Z) -> np.matrix:
    # Move to origin
    t_matrix = getTranslationMatrix(Point3D(-point.x, -point.y, -point.z))
    # Rotate
    r_matrix = getRotationMatrix(angle, axis)
    # Move back to position
    i_matrix = getTranslationMatrix(point)
    
    return multiplyMatrices([matrix, t_matrix, r_matrix, i_matrix])

def transformParallelProjection(point: Point3D, viewport: Viewport) -> Point2D:
    point_matrix = np.matrix([point.x, point.y, point.z])
    vpr = viewport.vpr
    # Move VRP to origin
    tvpr = getTranslationMatrix(Point3D(-vpr.x, -vpr.y, -vpr.z))
    # Rotate VPN along X
    rotate_x = getRotationMatrix(viewport.rot_angle, Axis.X)
    # Rotate VPN along Y
    rotate_y = getRotationMatrix(viewport.rot_angle, Axis.Y)
    # Move VRP back into place
    tvpr_inv = getTranslationMatrix(vpr)
    # Apply all rotations
    result_rotation = multiplyMatrices([tvpr, rotate_x, rotate_y, tvpr_inv])
    # Apply projection
    result = multiplyMatrices([result_rotation, point_matrix])
    
    return Point2D(result.item(0), result.item(1))
    