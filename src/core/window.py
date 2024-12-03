from core.components import Transform
from core.camera import Camera
from utils.math_utils import Point3D
from enumerators.axis_type import Axis

class Window:
	def __init__(self, xMin:float, yMin:float, xMax:float, yMax:float, activeCamera: Camera):
		self.activeCamera = activeCamera
		self.transform = Transform()
		self.setup(xMin, yMin, xMax, yMax)

	def setup(self, xMin:float, yMin:float, xMax:float, yMax:float):
		if (xMin >= xMax or yMin >= yMax):
			return
		self.xMin = xMin
		self.yMin = yMin
		self.xMax = xMax
		self.yMax = yMax
		self.transform.position = Point3D(((self.xMax - self.xMin) / 2) + self.xMin, ((self.yMax - self.yMin) / 2) + self.yMin, self.transform.position.z)

		self.printDimensions()

	def pan(self, xDir:int, yDir:int, value:float):
		self.setup(xDir*value + self.xMin, yDir*value + self.yMin, xDir*value + self.xMax, yDir*value + self.yMax)
		self.activeCamera.transform.position.x += xDir*value
		self.activeCamera.transform.position.y += yDir*value

	def zoom(self, value):
		self.setup(self.xMin + value, self.yMin + value, self.xMax - value, self.yMax - value)

	def rotate(self, value: float, axis: Axis):
		newRotation = self.transform.rotation

		if (Axis.X == axis):
			newRotation.x = (newRotation.x + value) % 360
			if (newRotation.x < 0): 
				newRotation.x += 360
		elif (Axis.Y == axis):
			newRotation.y = (newRotation.y + value) % 360
			if (newRotation.y < 0): 
				newRotation.y += 360
		elif (Axis.Z == axis):
			newRotation.z = (newRotation.z + value) % 360
		if (newRotation.z < 0): 
			newRotation.z += 360
        
		self.transform.rotation = newRotation
		self.printDimensions()
  
	def printDimensions(self):
		print('Window dimensions:', 
			["points:", (round(self.xMin, 2), round(self.yMin, 2)), (round(self.xMax, 2), round(self.yMax, 2))],
			["center:", (round(self.transform.position.x, 2), round(self.transform.position.y, 2))], 
			["rotation:", (round(self.transform.rotation.x, 2), round(self.transform.rotation.y, 2), round(self.transform.rotation.z, 2))]
		)
