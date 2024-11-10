import numpy as np
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

def transformParallelProjection(point: Point3D, vpr: Point3D, r_x:int, r_y:int, r_z:int) -> Point2D:
    point_matrix = np.matrix([[point.x, point.y, point.z, 1]])
    # Move VRP to origin
    tvpr = getTranslationMatrix(Point3D(-vpr.x, -vpr.y, -vpr.z))
    # Rotate VPN along X
    rotate_x = getRotationMatrix(r_x, Axis.X)
    # Rotate VPN along Y
    rotate_y = getRotationMatrix(r_y, Axis.Y)
    # Move VRP back into place
    tvpr_inv = getTranslationMatrix(vpr)
    # Apply all rotations
    result_rotation = multiplyMatrices([tvpr, rotate_x, rotate_y, tvpr_inv])
    # Apply projection
    result = multiplyMatrices([point_matrix, result_rotation])
    teste= Point2D(result.item(0), result.item(1))
    return teste
    
# Viewplane must be parallel to XY plane
def transformPerspective(point: Point3D, distance: int) -> Point2D:
    point_matrix = np.matrix([[point.x, point.y, point.z, 1]])
    # Rotate VPN along X
    rotate_x = getRotationMatrix(0, Axis.X)
    # Rotate VPN along Y
    rotate_y = getRotationMatrix(0, Axis.Y)
    rot_point = multiplyMatrices([point_matrix, rotate_x, rotate_y])
    xp = rot_point.item(0)/(rot_point.item(2)/distance)
    yp = rot_point.item(1)/(rot_point.item(2)/distance)
    
    return Point2D(xp, yp)
    
    