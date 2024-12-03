from typing import Tuple 
import numpy as np
from math import degrees, atan

from enumerators.axis_type import Axis
from enumerators.projection_type import CameraProjection
from utils.math_utils import Point2D, Point3D, multiplyMatrices
from utils.transform_utils import getTranslationMatrix, getRotationMatrix, rotateAroundPoint
from core.window import Window
from core.viewport import Viewport

def viewportTransform(point: Point3D, window: Window, viewport: Viewport) -> Tuple:
	xWmin, yWmin, xWmax, yWmax = (window.xMin, window.yMin, window.xMax, window.yMax)
	xVmin, yVmin, xVmax, yVmax = (viewport.x, viewport.y, viewport.width + viewport.x, viewport.height + viewport.y)

	xV = ((point.x - xWmin) / (xWmax - xWmin)) * (xVmax - xVmin)
	yV = (1 - ((point.y - yWmin) / (yWmax - yWmin))) * (yVmax - yVmin)

	xV += viewport.x
	yV += viewport.y
  
	return (int(xV), int(yV))

def getNormalPoint(point: Point3D, window: Window) -> Point2D:
	if(window.activeCamera.projectionType == CameraProjection.PARALLEL):
		matrix = applyParallelProj(point, window)
	else:
		matrix = applyPerspectiveProj(point, window)

	matrix = rotateAroundPoint(matrix, -window.transform.rotation.z, window.transform.position)
	return Point2D(matrix.item(0), matrix.item(1))

def applyParallelProj(point: Point3D, window: Window) -> Point2D:
	return applyVpnRotationMatrix(point, window.transform.position, window)

def applyPerspectiveProj(point: Point3D, window: Window) -> np.matrix:
	matrix = applyVpnRotationMatrix(point, window.activeCamera.transform.position, window)

	# Get focal distance
	f = window.activeCamera.transform.position.z

	perspectiveMatrix = np.matrix([
    	[1,   0,   0,   0],
    	[0,   1,   0,   0],
    	[0,   0,   1,   0],
    	[0,   0, 1/f,   0]
	])
  
	return multiplyMatrices([matrix, perspectiveMatrix])


def applyVpnRotationMatrix(point: Point3D, focusPoint: Point3D, window: Window):
	matrix = np.matrix([point.x, point.y, point.z, 1])

	tMatrix = getTranslationMatrix(Point3D(-focusPoint.x, -focusPoint.y, -focusPoint.z)),
	tInvMatrix = getTranslationMatrix(focusPoint)

	vpn = Point3D(window.transform.position.x - focusPoint.x, window.transform.position.y - focusPoint.y, window.transform.position.z - focusPoint.z)
	rotationX = 0 
	rotationY = 0
	if (vpn.z != 0):
		rotationX = degrees(atan(vpn.y / vpn.z))
		rotationY = degrees(atan(vpn.x / vpn.z))
    
	rxMatrix = getRotationMatrix(rotationX - window.transform.rotation.x, Axis.X)
	ryMatrix = getRotationMatrix(rotationY - window.transform.rotation.y, Axis.Y)

	vpnRotationMatrix = multiplyMatrices([tMatrix, rxMatrix, ryMatrix, tInvMatrix])

	return multiplyMatrices([matrix, vpnRotationMatrix])