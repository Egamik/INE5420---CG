
import os
import ntpath
import numpy as np
from math import radians as rad, tan
from ast import literal_eval

from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, 
                            QMainWindow, QPushButton, QLineEdit, QListWidget, QFileDialog, 
                            QRadioButton, QButtonGroup, QAction, QWidget, QDialog,
                            )
from PyQt5.QtGui import QColor
from enumerators.projection_type import CameraProjection
from enumerators.graphic_object_type import GraphicObjectType
from enumerators.axis_type import Axis

from core.window import Window
from core.camera import Camera
from core.viewport import Viewport, ViewportLayout

from widgets.arrows import ArrowsWidget
from widgets.console import ConsoleWidget
from widgets.transformation import TransformationWidget
from widgets.object_dialog import AddObjectDialog
from utils.object_utils import instantiateObject
from utils.clipping import ClippingLineAlgorithm, applyClipping
from utils.window_utils import getNormalPoint
from utils.transform_utils import rotateAroundOrigin 
from utils.math_utils import Point3D
from file_parser import loadFromJson, saveToJson, loadFromObj, saveToObj
from model.base_object import GraphicObject
from widgets.axis_selector import AxisWidget

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    # Config window
    self.focal_angle = 15
    self.focal_distance = 500
    self.pan_value = 100
    self.zoom_value = 100
    self.rotate_value = 0
    self.rotate_axis = Axis.Z
    self.setupWorldWindow(0, 0, 1000, 1000, CameraProjection.PARALLEL)

    # Create main layout
    self.setStyleSheet("background-color: #303030;" "color: white")
    self.setWindowTitle('SGI')
    main_layout = QHBoxLayout()
    self.resize(1000, 900)
    
    right_layout = QVBoxLayout()
    left_layout = QVBoxLayout()
    # Set up viewport and canva
    main_layout.addLayout(left_layout, 1)
    main_layout.addLayout(right_layout, 3)
    right_layout.addLayout(self.setupViewport(800, 800, 0.8))
    
    right_layout.addWidget(QLabel("Console Output"))
    right_layout.addLayout(ConsoleWidget())

    left_layout.addLayout(self.setupObjectsUI())
    left_layout.addLayout(self.setupCameraProjectionUI())
    left_layout.addLayout(self.setupLineClippingUI())
    left_layout.addLayout(self.setupPanUI())
    left_layout.addLayout(self.setupRotateUI())
    
    self.updateObjectList()
    self.zoomTextField.setText(str(self.zoom_value))
    self.panTextField.setText(str(self.pan_value))
    self.rotateTextField.setText(str(self.rotate_value))
    
    self.setupMenu()
    
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    self.setCentralWidget(central_widget)

  def setupWorldWindow(self, x, y, width, height, cameraProjection: CameraProjection):
    self.worldWindow = Window(x, y, width, height, Camera(projectionType=cameraProjection))
    cameraPosition = Point3D(self.worldWindow.transform.position.x, self.worldWindow.transform.position.y - (tan(rad(self.focal_angle)) * self.focal_distance), self.worldWindow.transform.position.z + self.focal_distance)
    self.worldWindow.activeCamera.transform.position = cameraPosition

  def setupMenu(self):
    menu_bar = self.menuBar()

    file_menu = menu_bar.addMenu("File")

    save_action = QAction("Save", self)
    open_action = QAction("Open", self)
    exit_action = QAction("Exit", self)

    save_action.triggered.connect(self.onSaveFile)
    open_action.triggered.connect(self.onLoadFile)
    exit_action.triggered.connect(self.close)

    file_menu.addAction(save_action)
    file_menu.addAction(open_action)
    file_menu.addSeparator()
    file_menu.addAction(exit_action)

  def setupObjectsUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 15)
    layout.addWidget(QLabel("Object List"))
    
    # Create object list
    self.objectList = QListWidget()

    # Create buttons
    transformButton = QPushButton("Transform Object")
    addObjectButton = QPushButton("Add Object")
    removeObjectButton = QPushButton("Remove Object")
    addObjectButton.clicked.connect(self.onAddObject)
    removeObjectButton.clicked.connect(self.onRemoveObject)
    transformButton.clicked.connect(self.showTranslationMenu)

    # Add widgets to layout
    layout.addWidget(self.objectList)
    layout.addWidget(addObjectButton)
    layout.addWidget(removeObjectButton)
    layout.addWidget(transformButton)

    return layout

  def setupCameraProjectionUI(self) -> QHBoxLayout:
    # Create layout
    layout: QHBoxLayout = QHBoxLayout()

    # Create labels
    proj_title = QLabel()
    proj_title.setText("Camera Projection Type: " )
    proj_title.setAutoFillBackground(True)
    proj_title.adjustSize()

    # Create Buttons
    button_layout = QHBoxLayout()

    parallelButton = QRadioButton("Parallel")
    parallelButton.setChecked(True)
    parallelButton.toggled.connect(lambda: (self.worldWindow.activeCamera.setProjectionType(CameraProjection.PARALLEL), self.onWindowChange()))
    button_layout.addWidget(parallelButton)
    
    perspectiveButton = QRadioButton("Perspective")
    perspectiveButton.toggled.connect(lambda: (self.worldWindow.activeCamera.setProjectionType(CameraProjection.PERSPECTIVE), self.onWindowChange()))
    button_layout.addWidget(perspectiveButton)
    
    # Add widgets to layout
    layout.addWidget(proj_title)
    layout.addLayout(button_layout)

    if (self.worldWindow.activeCamera.projectionType == CameraProjection.PARALLEL):
      parallelButton.setChecked(True)
    else:
      perspectiveButton.setChecked(True)

    return layout

  def setupLineClippingUI(self) -> QHBoxLayout:
    # Create layout
    layout: QHBoxLayout = QHBoxLayout()

    # Create labels
    clippingTitle = QLabel()
    clippingTitle.setText("Line Clipping Type: " )
    clippingTitle.setAutoFillBackground(True)
    clippingTitle.adjustSize()

    # Create Buttons
    buttons = QButtonGroup()

    self.clipping_liangbarsky_radio = QRadioButton("Liang-Barsky")
    self.clipping_liangbarsky_radio.setChecked(True)
    self.clipping_liangbarsky_radio.clicked.connect(lambda: (self.worldWindow.activeCamera.setLineClipping(ClippingLineAlgorithm.LiangBarsky), self.onWindowChange()))
    buttons.addButton(self.clipping_liangbarsky_radio)
    
    self.clippingCohenSutherlandRadio = QRadioButton("Cohen-Sutherland")
    self.clippingCohenSutherlandRadio.clicked.connect(lambda: (self.worldWindow.activeCamera.setLineClipping(ClippingLineAlgorithm.CohenSutherland), self.onWindowChange()))
    buttons.addButton(self.clippingCohenSutherlandRadio)

    # Add widgets to layout
    layout.addWidget(clippingTitle)
    layout.addWidget(self.clipping_liangbarsky_radio)
    layout.addWidget(self.clippingCohenSutherlandRadio)

    return layout

  def setupPanUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()

    # Create labels
    panText = QLabel()
    zoomText = QLabel()
    panText.setText("Window Pan: " )
    zoomText.setText("Window Zoom: " )
    
    # Create text field
    self.panTextField = QLineEdit()
    self.zoomTextField = QLineEdit()
    self.panTextField.adjustSize()
    self.zoomTextField.adjustSize()
    self.panTextField.textChanged[str].connect(self.onPanInput)
    self.zoomTextField.textChanged[str].connect(self.onZoomInput)

    # Create pan arrows
    arrows = ArrowsWidget(lambda: self.onPan(0, 1), lambda: self.onPan(0, -1), lambda: self.onPan(-1, 0), lambda: self.onPan(1, 0), self.onZoomIn, self.onZoomOut)

    # Add widgets to layout
    layout.addWidget(panText)
    layout.addWidget(self.panTextField)
    layout.addWidget(zoomText)
    layout.addWidget(self.zoomTextField)
    layout.addLayout(arrows.getLayout())

    return layout

  def setupRotateUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 25, 0, 25)

    # Create labels
    rotateText = QLabel()
    rotateText.setText("Window Rotation: " )
    
    # Create axis radio buttons
    rotateBtnLayout = QHBoxLayout()
    self.axis_x_radio = QRadioButton("X")
    self.axis_y_radio = QRadioButton("Y")
    self.axis_z_radio = QRadioButton("Z")
    
    rotateBtnLayout.addWidget(self.axis_x_radio)
    rotateBtnLayout.addWidget(self.axis_y_radio)
    rotateBtnLayout.addWidget(self.axis_z_radio)
    
    self.axis_z_radio.setChecked(True)
    axisGroup = QButtonGroup(self)
    axisGroup.addButton(self.axis_x_radio)
    axisGroup.addButton(self.axis_y_radio)
    axisGroup.addButton(self.axis_z_radio)
    axisGroup.buttonClicked.connect(self.setRotateAxis)

    # Create text field
    self.rotateTextField = QLineEdit()
    self.rotateTextField.adjustSize()
    self.rotateTextField.textChanged[str].connect(self.onRotateInput)
 
    # Create buttons
    rotateButton = QPushButton("Rotate")
    rotateButton.clicked.connect(self.onRotate)

    # Add widgets to layout
    layout.addWidget(rotateText)
    layout.addLayout(rotateBtnLayout)
    layout.addWidget(self.rotateTextField)
    layout.addWidget(rotateButton)

    return layout

  def setupViewport(self, width: int, height: int, canvasRatio: float) -> QVBoxLayout:
    posMultiplier = (1 - canvasRatio) / 2
    self.viewport = Viewport(posMultiplier*width, posMultiplier*height, canvasRatio*width, canvasRatio*height)

    layout: QVBoxLayout = QVBoxLayout()
    self.viewLayout = ViewportLayout(self, self.viewport, self.worldWindow, width, height)
    layout.addWidget(self.viewLayout)
    return layout

  def updateObjectList(self):
    self.objectList.clear()

    for obj in self.viewport.displayFile:
      points = list(map(lambda p: (round(p.x, 2), round(p.y, 2), round(p.z, 2)) , obj.getPoints()))
      self.objectList.addItem(f'[{obj.type.value}] {obj.name} {points}' )
    self.onWindowChange()

  def updatePointsAndRepaint(self):
    for obj in self.viewport.displayFile:
      for i in range(len(obj.points)):
        obj.normalizedPoints[i] = getNormalPoint(obj.points[i], self.worldWindow)
      obj.renderPoints = applyClipping(obj.type, obj.normalizedPoints, self.worldWindow)
    self.repaint()

  def getSelectedObject(self) -> GraphicObject:
    index = self.objectList.currentRow()
    if (index < 0): return
    return self.viewport.displayFile[index]

  def createInstance(self, points: list, name: str, objType: GraphicObjectType, color: QColor):
    self.viewport.addObject(instantiateObject(name, objType, points, color))

  def repaint(self):
    self.viewLayout.drawDisplayFile()
    super().repaint()

  def onWindowChange(self):
    self.updatePointsAndRepaint()

  def onLoadFile(self):
    path = QFileDialog.getOpenFileName(self, 'Open file', 'data', "Object files: (*.obj *.json)")
    if (len(path[0]) <= 0): return
    
    fileExtension = os.path.splitext(path[0])[1]
    if fileExtension == ".json":
      objects = loadFromJson(path[0])
    elif fileExtension == ".obj":
      objPath = path[0]
      path = QFileDialog.getOpenFileName(self, 'Open Wavefront material', 'data/obj', "Wavefront material files: (*.mtl)")
      if (path[0] == ''): return
      mtlPath = path[0]
      objects, objWindow = loadFromObj(objPath, mtlPath)
      xMin = min(objWindow[0][0], objWindow[1][0])
      yMin = min(objWindow[0][1], objWindow[1][1])
      xMax = max(objWindow[0][0], objWindow[1][0])
      yMax = max(objWindow[0][1], objWindow[1][1])
      self.worldWindow.setup(xMin, yMin, xMax, yMax)
    self.viewport.displayFile = objects
    self.updateObjectList()

  def onSaveFile(self):
    path = QFileDialog.getSaveFileName(self, 'Save file', 'data', "Wavefront Object: (*.obj);;JSON: (*.json)")
    filename = path_leaf(path[0]).split('.')[0]
    fileExtension = os.path.splitext(path[0])[1]
    if fileExtension == ".json":
      saveToJson(self.viewport.displayFile, path[0])
    elif fileExtension == ".obj":
      saveToObj(self.viewport.displayFile, path[0], filename, [[self.worldWindow.x_min, self.worldWindow.y_min], [self.worldWindow.x_max, self.worldWindow.y_max]])

  def onAddObject(self):
    dialog = AddObjectDialog(self)
    if dialog.exec_() == QDialog.Accepted:
      obj_type = dialog.getObjectType()
      obj_points = dialog.getPointData()
      obj_name = dialog.getObjectName()
      obj_color = dialog.getObjectColor()
      print('Create instance: ', obj_name, ' type: ', obj_type.name)
      self.createInstance(obj_points, obj_name, obj_type, obj_color)
      self.updateObjectList()
      self.repaint()
      

  def onRemoveObject(self):
    obj = self.getSelectedObject()
    if(obj == None): return
    self.viewport.removeObject(obj)
    self.updateObjectList()

  def onPan(self, xDir: int, yDir: int):
    print('Pan: ', self.zoom_value)
    matrix = np.matrix([xDir, yDir, 0, 1])
    matrix = rotateAroundOrigin(matrix, self.worldWindow.transform.rotation.z, Axis.Z)
    self.worldWindow.pan(matrix.item(0), matrix.item(1), self.pan_value)
    self.onWindowChange()

  def onZoomIn(self):
    print('Zoom in: ', self.zoom_value)
    self.worldWindow.zoom(self.zoom_value)
    self.onWindowChange()

  def onZoomOut(self):
    print('Zoom out: ', self.zoom_value)
    self.worldWindow.zoom(-self.zoom_value)
    self.onWindowChange()

  def onRotate(self):
    print('Rotate: ', self.rotate_value)
    self.worldWindow.rotate(self.rotate_value, self.rotate_axis)
    print("Rotating window on axis: " + self.rotate_axis.name)
    self.onWindowChange()

  def onZoomInput(self, value):
    self.zoom_value = float(value)

  def onPanInput(self, value):
    self.pan_value = float(value)
  
  def onRotateInput(self, value):
    self.rotate_value = float(value)  
  
  def showTranslationMenu(self):
    index = self.objectList.currentRow()
    if (index < 0): return
    self.translation = TransformationWidget(self.viewport.displayFile[index], self.worldWindow, self.repaint)
    self.translation.show()

  def setRotateAxis(self, button):
    if button == self.axis_x_radio:
      self.rotate_axis = Axis.X
    elif button == self.axis_y_radio:
      self.rotate_axis = Axis.Y
    elif button == self.axis_z_radio:
      self.rotate_axis = Axis.Z

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
