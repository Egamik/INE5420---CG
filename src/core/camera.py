from core.components import Transform
from enumerators.projection_type import CameraProjection
from enumerators.clipping_type import ClippingLineAlgorithm, ClippingCurveAlgorithm

class Camera:
	def __init__(self,
		projectionType = CameraProjection.PARALLEL, 
		lineClipType = ClippingLineAlgorithm.CohenSutherland,
		curveClippingType = ClippingCurveAlgorithm.Bezier
	):
		self.setProjectionType(projectionType)
		self.setLineClipping(lineClipType)
		self.setCurveClipping(curveClippingType)
    
		self.transform = Transform()
   
	def setProjectionType(self, projectionType: CameraProjection):
		self.projectionType = projectionType

	def setLineClipping(self, algorithm: ClippingLineAlgorithm):
		self.lineClippingType = algorithm

	def setCurveClipping(self, algorithm: ClippingCurveAlgorithm):
		self.curveClippingType = algorithm
