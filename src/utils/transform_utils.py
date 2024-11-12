import numpy as np
from math import degrees, atan
from base.viewport import Viewport
from base.axis import Axis
from base.point import Point3D, Point2D
from base.projection import CameraProjection
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

def normalizePoint(point: Point3D, viewport: Viewport) -> Point2D:
    if (viewport.projection_type == CameraProjection.PARALLEL):
        n_point = transformParallelProjection(point, viewport)
    else:
        n_point = transformPerspectiveProjection(point, viewport)
    
    mat = rotateAroundPoint(n_point, -viewport.transformations.rotation.z, viewport.transformations.position)
    return Point2D(mat.item(0), mat.item(1))

def transformParallelProjection(point: Point3D, viewport: Viewport) -> Point2D:
    #!!!!!!
    return applyViewRotationMatrix(point, viewport.transformations.position, viewport)
    
# Viewplane must be parallel to XY plane
def transformPerspectiveProjection(point: Point3D, viewport: Viewport) -> Point2D:
    mat = applyViewRotationMatrix(point, viewport.focus_point, viewport)
    
    # f = window.camera.position.z
    f = 100
    perspectiveMatrix = np.matrix([
        [1,   0,   0,   0],
        [0,   1,   0,   0],
        [0,   0,   1,   0],
        [0,   0, 1/f,   0]
    ])
    
    return multiplyMatrices([mat, perspectiveMatrix])
    
def applyViewRotationMatrix(point: Point3D, focus: Point3D, viewport: Viewport):
    mat = np.matrix([point.x, point.y, point.z, 1])
    
    focus_mat = getTranslationMatrix(focus)
    focus_tmat = getTranslationMatrix(Point3D(-focus.x, -focus.y, -focus.z))
    vpn = Point3D()
    rotation_x = 0
    rotation_y = 0
    
    if (vpn.z != 0):
        rotation_x = degrees(atan(vpn.y / vpn.z))
        rotation_y = degrees(atan(vpn.x / vpn.z))
    
    # - window.rotation
    rx_mat = getRotationMatrix(rotation_x, Axis.X)
    ry_mat = getRotationMatrix(rotation_y, Axis.Y)
    
    vpn_rotation_mat = multiplyMatrices([focus_tmat, rx_mat, ry_mat, focus_mat])
    
    return multiplyMatrices([mat, vpn_rotation_mat])
    