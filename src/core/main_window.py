
import os
import ntpath
import numpy as np
from math import radians as rad, tan
from ast import literal_eval

from PyQt5.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QFileDialog, QRadioButton, QButtonGroup

from enumerators.projection_type import CameraProjection
from enumerators.graphic_object_type import GraphicObjectType
from enumerators.axis_type import Axis

from core.window import Window
from core.camera import Camera
from core.viewport import Viewport, ViewportLayout

from widgets.object_type import SelectObjectTypeWidget
from widgets.arrows import ArrowsWidget
from widgets.console import ConsoleWidget
from widgets.color_picker import ColorPickerWidget
from widgets.transformation import TransformationWidget
from utils.object_utils import instantiateObject, getTypeByPoints
from utils.clipping import ClippingLineAlgorithm, applyClipping
from utils.window_utils import getNormalPoint
from utils.transform_utils import rotateAroundOrigin 
from utils.math_utils import Point3D
from utils.object_utils import instantiateObject, getTypeByPoints
from file_parser import loadFromJson, saveToJson, loadFromObj, saveToObj
from model.base_object import GraphicObject
from widgets.axis_selector import AxisWidget

class MainWindow(QWidget):
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
    self.layout: QHBoxLayout = self.setupAppWindowUI(1030, 720)
    self.layout.addLayout(self.setupControllersUI(), 40)
    right_layout = QVBoxLayout()
    self.layout.addLayout(right_layout, 60)
    right_layout.addLayout(self.setupViewport(600, 600, 0.8))
    right_layout.addWidget(QLabel("Console Output"))
    right_layout.addLayout(ConsoleWidget())

    self.layout.setContentsMargins(20, 20, 20, 20)

    self.updateObjectList()
    self.zoomTextField.setText(str(self.zoom_value))
    self.panTextField.setText(str(self.pan_value))
    self.rotateTextField.setText(str(self.rotate_value))

  def setupWorldWindow(self, x, y, width, height, cameraProjection: CameraProjection):
    self.worldWindow = Window(x, y, width, height, Camera(projectionType=cameraProjection))
    cameraPosition = Point3D(self.worldWindow.transform.position.x, self.worldWindow.transform.position.y - (tan(rad(self.focal_angle)) * self.focal_distance), self.worldWindow.transform.position.z + self.focal_distance)
    self.worldWindow.activeCamera.transform.position = cameraPosition

  def setupAppWindowUI(self, width, height) -> QHBoxLayout:
    layout: QHBoxLayout = QHBoxLayout(self)
    self.resize(width, height)
    self.setAutoFillBackground(True)
    self.setStyleSheet("background-color: #303030;"
                       "color: white"
    )
    self.setWindowTitle('Computer Graphics - T1')

    return layout

  def setupControllersUI(self) -> QVBoxLayout:
    # Setup main controllers layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 30, 0)
    layout.addLayout(self.setupObjectsUI())
    layout.addLayout(self.setupCameraProjectionUI())
    layout.addLayout(self.setupLineClippingUI())
    layout.addLayout(self.setupZoomUI())
    layout.addLayout(self.setupPanUI())
    layout.addLayout(self.setupRotateUI())
    return layout

  def setupObjectsUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 15)
    layout.addWidget(QLabel("Scene objects"))
    
    # Create object list
    self.objectList = QListWidget()

    # Create buttons
    self.colorButton = ColorPickerWidget()
    loadFileButton = QPushButton("Load File")
    saveFileButton = QPushButton("Save File")
    transformButton = QPushButton("Transform Object")
    addObjectButton = QPushButton("Add Object")
    removeObjectButton = QPushButton("Remove Object")
    loadFileButton.clicked.connect(self.onLoadFile)
    saveFileButton.clicked.connect(self.onSaveFile)
    addObjectButton.clicked.connect(self.onAddObject)
    removeObjectButton.clicked.connect(self.onRemoveObject)
    transformButton.clicked.connect(self.showTranslationMenu)

    # Create labels
    inputText = QLabel()
    inputText.setText("insert points in format (x,y),(x,y),... " )
    inputText.setAutoFillBackground(True)
    inputText.adjustSize()
    inputNameText = QLabel()
    inputNameText.setText("insert object's name" )
    inputNameText.setAutoFillBackground(True)
    inputNameText.adjustSize()
    inputColorText = QLabel()
    inputColorText.setText("insert object's color" )
    inputColorText.setAutoFillBackground(True)
    inputColorText.adjustSize()

    # Create text field
    self.addObjectText = QLineEdit()
    self.addObjectText.adjustSize()
    self.addNameText = QLineEdit()
    self.addNameText.adjustSize()

    # Add widgets to layout
    layout.addWidget(self.objectList)
    layout.addWidget(loadFileButton)
    layout.addWidget(saveFileButton)
    layout.addWidget(inputText)
    layout.addWidget(self.addObjectText)
    layout.addWidget(inputNameText)
    layout.addWidget(self.addNameText)
    layout.addWidget(inputColorText)
    layout.addWidget(self.colorButton)
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
    buttons = QButtonGroup()

    parallelButton = QRadioButton("Parallel")
    parallelButton.clicked.connect(lambda: (self.worldWindow.activeCamera.setProjectionType(CameraProjection.PARALLEL), self.onWindowChange()))
    buttons.addButton(parallelButton)
    
    perspectiveButton = QRadioButton("Perspective")
    perspectiveButton.clicked.connect(lambda: (self.worldWindow.activeCamera.setProjectionType(CameraProjection.PERSPECTIVE), self.onWindowChange()))
    buttons.addButton(perspectiveButton)
    
    # Add widgets to layout
    layout.addWidget(proj_title)
    layout.addWidget(parallelButton)
    layout.addWidget(perspectiveButton)

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

  def setupZoomUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 25, 0, 25)

    # Create buttons
    zoom_in_btn = QPushButton("Zoom in")
    zoom_out_btn = QPushButton("Zoom out")
    zoom_in_btn.clicked.connect(self.onZoomIn)
    zoom_out_btn.clicked.connect(self.onZoomOut)

    # Create labels
    zoomText = QLabel()
    zoomText.setText("Window Zoom: " )
    zoomText.setAutoFillBackground(True)
    zoomText.adjustSize()

    # Create text field
    self.zoomTextField = QLineEdit()
    self.zoomTextField.adjustSize()
    self.zoomTextField.textChanged[str].connect(self.onZoomInput)

    # Add widgets to layout
    layout.addWidget(zoomText)
    layout.addWidget(self.zoomTextField)
    layout.addWidget(zoom_in_btn)
    layout.addWidget(zoom_out_btn)

    return layout

  def setupPanUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 25, 0, 25)

    # Create labels
    panText = QLabel()
    panText.setText("Window Pan: " )
    panText.setAutoFillBackground(True)
    panText.adjustSize()
    
    # Create text field
    self.panTextField = QLineEdit()
    self.panTextField.adjustSize()
    self.panTextField.textChanged[str].connect(self.onPanInput)

    # Create pan arrows
    arrows = ArrowsWidget(lambda: self.onPan(0, 1), lambda: self.onPan(0, -1), lambda: self.onPan(-1, 0), lambda: self.onPan(1, 0))

    # Add widgets to layout
    layout.addWidget(panText)
    layout.addWidget(self.panTextField)
    layout.addLayout(arrows.getLayout())

    return layout

  def onAxisInput(self, value):
    if(value == 'x'):
      self.rotate_axis = Axis.X
      print("Rotating window on axis: " + Axis.X.name)
    if(value == 'y'):
      self.rotate_axis = Axis.Y  
      print("Rotating window on axis: " + Axis.Y.name)
    if(value == 'z'):
      self.rotate_axis = Axis.Z
      print("Rotating window on axis: " + Axis.Z.name)

  def setupRotateUI(self) -> QVBoxLayout:
    # Create layout
    layout: QVBoxLayout = QVBoxLayout()
    layout.setContentsMargins(0, 25, 0, 25)

    # Create labels
    rotateText = QLabel()
    rotateText.setText("Window Rotation: " )
    rotateText.setAutoFillBackground(True)
    rotateText.adjustSize()
    
    # Create axis radio buttons
    axisRadio = AxisWidget(self.setRotateAxis)

    # Create text field
    self.rotateTextField = QLineEdit()
    self.rotateTextField.adjustSize()
    self.rotateTextField.textChanged[str].connect(self.onRotateInput)
 
    # Create buttons
    rotateButton = QPushButton("Rotate")
    rotateButton.clicked.connect(self.onRotate)

    # Add widgets to layout
    layout.addWidget(rotateText)
    layout.addLayout(axisRadio)
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

  def createInstance(self, points: list, name: str, objType: GraphicObjectType):
    self.colorButton.color
    self.viewport.addObject(instantiateObject(name, objType, points, self.colorButton.getColor()))

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
      saveToObj(self.viewport.displayFile, path[0], filename, [[self.worldWindow.xMin, self.worldWindow.yMin], [self.worldWindow.xMax, self.worldWindow.yMax]])

  def onAddObject(self):
    self.checkNameInput()
    self.checkCoordinatesInput(self.addNameText.text()) 
    self.updateObjectList()
    self.repaint()    
    self.addObjectText.clear()
    self.addNameText.clear()  

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
    self.zoom_value = self.onNumberFieldInput(value)  

  def onPanInput(self, value):
    self.pan_value = self.onNumberFieldInput(value)  
  
  def onRotateInput(self, value):
    self.rotate_value = self.onNumberFieldInput(value)  

  def onNumberFieldInput(self, value) -> float:
    try:
      value = (float(value))
      return value
    except:
      errorMessage = QMessageBox()
      errorMessage.setText('Your input should be a number')
      errorMessage.setWindowTitle('Wrong input format')
      errorMessage.setStyleSheet("background-color: #303030;"
                                  "color: white"
      )
      errorMessage.exec()     

  def checkNameInput(self):
    if(not self.addNameText.text() or self.addNameText.text().isspace()):
      self.raiseException("Add a name to this object", "Name Required")
    
  def raiseException(self, message: str, title: str):
    errorMessage = QMessageBox()
    errorMessage.setText(message)
    errorMessage.setWindowTitle(title)
    errorMessage.setStyleSheet("background-color: #303030;"
                                "color: white"
    )
    errorMessage.exec()     
  
  def checkCoordinatesInput(self, name: str):
    try:
      pointsString = self.addObjectText.text()
      listPoints = [literal_eval(f'({x})') for x in pointsString.strip('()').split('),(')]  
      self.countPoints(listPoints, name)
      return              
    except:
      self.raiseException('Your coordinates should be in format (x,y),(x,y),...', 'Wrong Format')  

  def showTranslationMenu(self):
    index = self.objectList.currentRow()
    if (index < 0): return
    self.translation = TransformationWidget(self.viewport.displayFile[index], self.worldWindow, self.repaint)
    self.translation.show()

  def countPoints(self, listPoints, name):
    numPoints = len(listPoints)
    if (numPoints <= 0): return

    if(numPoints < 4):
      self.createInstance(listPoints, name, getTypeByPoints(numPoints))
    else:
      self.selectObjectTypeWidget = SelectObjectTypeWidget(self.createInstance, name, listPoints, self.updateObjectList, self.repaint)
      self.selectObjectTypeWidget.show()

  def setRotateAxis(self, axis: Axis):
    self.rotate_axis = axis

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
