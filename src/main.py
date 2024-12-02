import sys
import os
import json
from typing import List
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QAction, QMenuBar
from GUI.control_widgets import ControlWidget
from GUI.objectDialog import AddObjectDialog
from GUI.canva import Canva
from GUI.transform_widget import TransformationWidgets
from GUI.object_viewer import ObjectTableWidget
from GUI.clipping_widget import LineClippingWidget
from base.graphic_obj import GraphicObject, GraphicObjectType
from utils.formatObject import formatObject
from utils.file_parser import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Window settings
		self.setWindowTitle("Trabalho SGI")
		self.setGeometry(100, 100, 1000, 700)

		# Attributes
		self.poli_count: int = 0
		self.poli_list: List[GraphicObject] = []
		self.pan_scale: int = 50
		self.zoom_scale: float = 0.2
		self.toggle_clip = True

		# Create Menu bar
		self.createMenuBar()

		# Main Layout
		main_layout = QHBoxLayout()
		left_layout = QVBoxLayout()
		right_layout = QVBoxLayout()
		# GUI components
		self.canva = Canva(self, 720, 450, self.getClipType)
		self.object_list = ObjectTableWidget(self)
		trans_controls = TransformationWidgets(self, self.object_list.getSelectedObject, self.canva.viewport, self.canva.drawObjects)
		controls = ControlWidget(self, self.object_list.getSelectedObject, self.canva.viewport, self.canva.drawObjects)
		clip_controls = LineClippingWidget(self.setClip)
		
		control_layout = controls.getLayout()
		trans_layout = trans_controls.getLayout()
		clip_layout = clip_controls.getLayout()

		# Left components
		buttonLayout = QHBoxLayout()
		addButton = QPushButton("Add Object")
		removeButton = QPushButton("Remove Object")
		addButton.clicked.connect(self.addObject)

		# Object List
		buttonLayout.addWidget(removeButton)
		buttonLayout.addWidget(addButton)
		left_layout.addWidget(QLabel("Object List"))
		left_layout.addWidget(self.object_list)
		
		left_layout.addLayout(clip_layout)
		left_layout.addLayout(buttonLayout)
		left_layout.addLayout(trans_layout)
		left_layout.addLayout(control_layout)
		
		# Add Left Layout to Main Layout
		main_layout.addLayout(left_layout, 1)

		# Setup viewport
		right_layout.addWidget(QLabel("Viewport"))
		right_layout.addWidget(self.canva, 3)
		right_layout.addStretch(1)

		main_layout.addLayout(right_layout, 3)

		# Central Widget setup
		central_widget = QWidget()
		central_widget.setLayout(main_layout)
		self.setCentralWidget(central_widget)

	def createMenuBar(self):
		menu_bar = self.menuBar()

		file_menu = menu_bar.addMenu("Menu")

		save_action = QAction("Save", self)
		open_action = QAction("Open", self)
		exit_action = QAction("Exit", self)

		save_action.triggered.connect(self.saveFile)
		open_action.triggered.connect(self.openFile)
		exit_action.triggered.connect(self.close)

		file_menu.addAction(save_action)
		file_menu.addAction(open_action)
		file_menu.addSeparator()
		file_menu.addAction(exit_action)

	def addObject(self):
		dialog = AddObjectDialog(self)
		if dialog.exec_() == QDialog.Accepted:
			objType = dialog.getObjectType()
			
			tp = formatObject(dialog.getPointData(), objType, self.poli_count)
			obj = tp[0]
			self.poli_count = tp[1]
			
			self.object_list.addObject(obj)
			self.canva.addObject(obj)
			self.canva.drawObjects()
	
	def removeObject(self):
		print('Remove object')
		selected = self.object_list.getSelectedObject()
		self.object_list.removeObject(selected.name)
		self.canva.removeObject(selected)
		self.canva.drawObjects()
		
	def setClip(self, b: bool):
		self.toggle_clip = b
	
	def getClipType(self):
		return self.toggle_clip
	
	def openFile(self):
		path = QFileDialog.getOpenFileName(self, 'Open file', 'data', "Object files: (*.obj *.json)")
		
		if len(path[0]) <= 0: return
		
		fileExt = os.path.splitext(path[0])[1]
		
		if fileExt == ".obj":
			filePath = path[0]
			
			path = QFileDialog.getOpenFileName(self, 'Open Wavefront material', 'data/obj', "Wavefront material files: (*.mtl)")
		
			if path[0] == '': return
			mtlPath = path[0]
			objects, objectWindow = loadFromObj(filePath, mtlPath)
			
			xMin = min(objectWindow[0][0], objectWindow[1][0])
			yMin = min(objectWindow[0][1], objectWindow[1][1])
			xMax = max(objectWindow[0][0], objectWindow[1][0])
			yMax = max(objectWindow[0][1], objectWindow[1][1])
			# set up window
		
		elif fileExt == ".json":
			objects = loadFromJson(path[0])
			
		for obj in objects:
			self.object_list.addObject(obj)
			self.canva.addObject(obj)
		
	
	def saveFile(self):
		path = QFileDialog.getSaveFileName(self, 'Save File', 'data', "Wavefront Object: (*.obj);;JSON: (*.json)")
		fileName = path_leaf(path[0]).split('.')[0]
		fileExt = os.path.splitext(path[0])[1]
		if fileExt == '.json':
			saveToJson(self.canva.getObjectList())
		elif fileExt == '.obj':
			saveToObj(self.canva.getObjectList(), path[0], fileName, [[self.canva.x_min, self.canva.y_min], [self.canva.x_max, self.canva.y_max]])

def path_leaf(path):
	head, tail = os.path.split(path)
	return tail or os.path.basename(head)
# Main Application
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
