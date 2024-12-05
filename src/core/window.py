from core.components import Transform
from core.camera import Camera
from utils.math_utils import Point3D
from enumerators.axis_type import Axis

class Window:
	def __init__(self, xMin:float, yMin:float, xMax:float, yMax:float, activeCamera: Camera):
		"""Representação lógica de uma window no mundo. """
		self.activeCamera = activeCamera
		self.transform = Transform()
		self.setup(xMin, yMin, xMax, yMax)

	def setup(self, xMin:float, yMin:float, xMax:float, yMax:float):
		if (xMin >= xMax or yMin >= yMax):
			return
		self.x_min = xMin
		self.y_min = yMin
		self.x_max = xMax
		self.y_max = yMax
		self.transform.position = Point3D(((self.x_max - self.x_min) / 2) + self.x_min, ((self.y_max - self.y_min) / 2) + self.y_min, self.transform.position.z)

		self.printDimensions()

	def pan(self, xDir:int, yDir:int, value:float):
		self.setup(xDir*value + self.x_min, yDir*value + self.y_min, xDir*value + self.x_max, yDir*value + self.y_max)
		self.activeCamera.transform.position.x += xDir*value
		self.activeCamera.transform.position.y += yDir*value

	def zoom(self, value):
		self.setup(self.x_min + value, self.y_min + value, self.x_max - value, self.y_max - value)

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
			["points:", (round(self.x_min, 2), round(self.y_min, 2)), (round(self.x_max, 2), round(self.y_max, 2))],
			["center:", (round(self.transform.position.x, 2), round(self.transform.position.y, 2))], 
			["rotation:", (round(self.transform.rotation.x, 2), round(self.transform.rotation.y, 2), round(self.transform.rotation.z, 2))]
		)
