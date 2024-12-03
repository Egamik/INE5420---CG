import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QListWidget, QMessageBox, QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QButtonGroup
from PyQt5.QtWidgets import QLabel
from enumerators.axis_type import Axis

from model.base_object import GraphicObject
from utils.window_utils import getNormalPoint
from utils.transform_utils import translate, rotateAroundOrigin, rotateAroundPoint, scale, getCenterMatrixPoint
from utils.math_utils import Point3D
from utils.clipping import applyClipping
from widgets.axis_selector import AxisWidget

class TransformationWidget(QWidget):
    def __init__(self, obj: GraphicObject, window, repaint):
        self.object: GraphicObject = obj
        super().__init__()
        self.layout = self.setupAppWindowUI(600, 520)
        self.layout.addLayout(self.setupObjectsUI())
        self.transformations = []
        self.repaint = repaint
        self.window = window
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.axis = Axis.Z

    def setupObjectsUI(self) -> QVBoxLayout:    
        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 30, 0)
        layout.addLayout(self.setRotationMenu())
        layout.addLayout(self.setScaleMenu())
        layout.addLayout(self.setTranslationMenu())
        layout.addLayout(self.setWindowComponents())
        
        return layout 

    def setRotationMenu(self) -> QVBoxLayout:
        layout:QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        
        rotateText = QLabel()
        rotateText.setText("Rotate Object")
        
        axisRadio = AxisWidget(self.setRotationAxis)

        self.rotateCenterRadio = QRadioButton('Rotate Around Center')
        self.rotateCenterRadio.toggled.connect(self.enableFields)

        self.rotatePointRadio = QRadioButton('Rotate Around Point') 
        self.rotatePointRadio.toggled.connect(self.enableFields)

        self.rotateOriginRadio = QRadioButton('Rotate Around Origin')
        self.rotateOriginRadio.toggled.connect(self.enableFields)

        layout.addWidget(rotateText)
        layout.addLayout(axisRadio)
        layout.addWidget(self.rotateCenterRadio)
        layout.addWidget(self.rotatePointRadio)
        layout.addWidget(self.rotateOriginRadio)
        
        return layout
        
    def disableInputPoint(self):
        self.inputPoint.setDisabled(True)

    def disableInputAngle(self):
        self.inputAngle.setDisabled(True)

    def disableInputVector(self):
        self.inputVector.setDisabled(True)


    def enableInputPoint(self):
        self.inputPoint.setDisabled(False)

    def enableInputAngle(self):
        self.inputAngle.setDisabled(False)

    def enableInputVector(self):
        self.inputVector.setDisabled(False)        

    def enableFields(self):
        if(self.rotateCenterRadio.isChecked() or self.rotateOriginRadio.isChecked()):
            self.inputPoint.setDisabled(True)
            self.inputAngle.setDisabled(False)
            self.inputVector.setDisabled(True)

        if(self.rotatePointRadio.isChecked()):
            self.inputPoint.setDisabled(False)
            self.inputAngle.setDisabled(False)
            self.inputVector.setDisabled(True)

        if(self.translateRadio.isChecked() or self.scaleRadio.isChecked()):
            self.inputPoint.setDisabled(True)
            self.inputAngle.setDisabled(True)
            self.inputVector.setDisabled(False)


    def setScaleMenu(self) -> QVBoxLayout:
        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        self.scaleText = QLabel()
        self.scaleText.setText("Scale Object")
        self.scaleRadio = QRadioButton('Scale')
        self.scaleRadio.toggled.connect(self.enableFields)

        layout.addWidget(self.scaleText)
        layout.addWidget(self.scaleRadio)
        
        return layout

    def setTranslationMenu(self) -> QVBoxLayout:
        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        self.translateText = QLabel()
        self.translateText.setText("Translate Object")
        self.translateRadio = QRadioButton('Translate')
        self.translateRadio.toggled.connect(self.enableFields)

        layout.addWidget(self.translateText)
        layout.addWidget(self.translateRadio)
        return layout

    def setWindowComponents(self) -> QVBoxLayout:
        layout: QVBoxLayout = QVBoxLayout()

        self.transformList = QListWidget()
        self.addTransformationButton = QPushButton()
        self.addTransformationButton.setText("Add")
        self.addTransformationButton.setMaximumWidth(55)

        self.removeButton = QPushButton()
        self.removeButton.setText("Remove")
        self.removeButton.setMaximumWidth(70)

        self.transformButton = QPushButton()
        self.transformButton.setText("Transform")
        self.addTransformationButton.setMaximumWidth(85)

        self.angleLabel = QLabel()
        self.angleLabel.setText("Angle")
        self.angleLabel.setMaximumWidth(40)

        self.inputAngle = QLineEdit()
        self.inputAngle.adjustSize()
        self.inputAngle.setDisabled(True)
        
        self.vectorLabel = QLabel()
        self.vectorLabel.setText("Vector")
        self.vectorLabel.setMaximumWidth(40)

        self.inputVector = QLineEdit()
        self.inputVector.adjustSize()
        self.inputVector.setDisabled(True)

        self.pointLabel = QLabel()
        self.pointLabel.setText("Point")
        self.pointLabel.setMaximumWidth(40)

        self.inputPoint = QLineEdit()
        self.inputPoint.adjustSize()
        self.inputPoint.setDisabled(True)
        
        layout.addWidget(self.angleLabel)
        layout.addWidget(self.inputAngle)
        layout.addWidget(self.vectorLabel)
        layout.addWidget(self.inputVector)
        layout.addWidget(self.pointLabel)
        layout.addWidget(self.inputPoint)
        layout.addWidget(self.addTransformationButton)
        layout.addWidget(self.transformList)
        layout.addWidget(self.removeButton)
        layout.addWidget(self.transformButton)
        self.addTransformationButton.clicked.connect(self.checkSelection)
        self.transformButton.clicked.connect(self.executeOperations)
        self.removeButton.clicked.connect(self.removeFromList)

        return layout

    def setupAppWindowUI(self, width, height) -> QHBoxLayout:
        layout: QHBoxLayout = QHBoxLayout(self)
        self.resize(width, height)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #303030;"
                       "color: white"
        )
        self.setWindowTitle('Transformation Menu')

        return layout

    def checkSelection(self):
        if(self.rotateCenterRadio.isChecked()):
            self.checkAngleInput()
            self.transformations.append({"object": self.object, "operation": 1, "angle": self.angle, "axis": self.axis })
            self.transformList.addItem(self.object.name + " - Rotate " + str(self.angle) + " degrees" + " in " + self.axis.name)
        if(self.rotateOriginRadio.isChecked()):
            self.checkAngleInput()
            self.transformations.append({"object": self.object, "operation": 2, "angle": self.angle, "axis": self.axis })
            self.transformList.addItem(self.object.name + " - Rotate Around Origin " + str(self.angle) + " degrees" + "in" + self.axis.name)
        if(self.rotatePointRadio.isChecked()):
            self.checkAngleInput()
            self.checkPointInput()  
            self.transformations.append({"object": self.object, "operation": 3, "angle": self.angle, "point": self.point, "axis": self.axis })
            self.transformList.addItem(self.object.name + " - Rotate " + str(self.angle) + " degrees " + "around " + str(self.point) + "in" + self.axis.name)  
        if(self.scaleRadio.isChecked()):
            self.checkVectorInput()  
            self.transformations.append({"object": self.object, "operation": 4, "vector": self.vector, "axis": self.axis })
            self.transformList.addItem(self.object.name + " - Scale with vector"  + str(self.vector) + " in " + self.axis.name)  
        if(self.translateRadio.isChecked()):
            self.checkVectorInput()  
            self.transformations.append({"object": self.object, "operation": 5, "vector": self.vector, "axis": self.axis})
            self.transformList.addItem(self.object.name + " - Translation with vector " + str(self.vector) + " in" + self.axis.name)                 

    def raiseException(self, message, title):
        errorMessage = QMessageBox()
        errorMessage.setText(message)
        errorMessage.setWindowTitle(title)
        errorMessage.setStyleSheet("background-color: #303030;"
                                  "color: white"
        )
        errorMessage.exec()    


    def checkAngleInput(self):
        try:
            self.angle = float(self.inputAngle.text())
        except:
            self.raiseException("Your angle should be a number", "Wrong input")   

    def checkVectorInput(self):
        try:
            self.vector = self.stringToTuple(self.inputVector.text())
        except:
            self.raiseException("Yout input should bem in (x,y) format","Wrong input") 

    def checkPointInput(self):
            try:
                self.point = self.stringToTuple(self.inputPoint.text())
            except:
                self.raiseException("Yout input should bem in (x,y) format","Wrong input")

    def stringToTuple(self, input: str) -> tuple:
        return tuple(map(float, input.strip('()').split(',')))

    def executeOperations(self):
        normalPointMatrices = list(map(lambda p: np.matrix([p.x, p.y, p.z, 1]), self.object.points))

        for transformation in self.transformations:
            operation = transformation["operation"]
            if(operation == 1):
                centerPoint = getCenterMatrixPoint(normalPointMatrices)
                for i in range(len(normalPointMatrices)):
                    normalPointMatrices[i] = rotateAroundPoint(normalPointMatrices[i], transformation["angle"], centerPoint, transformation["axis"])
            elif(operation == 2):    
                for i in range(len(normalPointMatrices)):             
                    normalPointMatrices[i] = rotateAroundOrigin(normalPointMatrices[i], transformation["angle"], transformation["axis"])
            elif(operation == 3):   
                tP = transformation["point"]
                point = Point3D(tP[0], tP[1], tP[2]) if len(tP)>2 else Point3D(tP[0], tP[1], 0)
                for i in range(len(normalPointMatrices)):
                    normalPointMatrices[i] = rotateAroundPoint(normalPointMatrices[i], transformation["angle"], point, transformation["axis"])
            elif(operation == 4):   
                sV = transformation["vector"]
                sPoint = Point3D(sV[0], sV[1], sV[2]) if len(sV)>2 else Point3D(sV[0], sV[1], 1)

                centerPoint: Point3D = getCenterMatrixPoint(normalPointMatrices)
                for i in range(len(normalPointMatrices)):
                    normalPointMatrices[i] = translate(normalPointMatrices[i], Point3D(-centerPoint.x, -centerPoint.y, -centerPoint.z)) 
                    normalPointMatrices[i] = scale(normalPointMatrices[i], sPoint)    
                    normalPointMatrices[i] = translate(normalPointMatrices[i], centerPoint) 
                self.object.transform.scale = Point3D(self.object.transform.scale.x * sPoint.x, self.object.transform.scale.y * sPoint.y, self.object.transform.scale.z * sPoint.z)

            elif(operation == 5):     
                tV = transformation["vector"]
                tPoint = Point3D(tV[0], tV[1], tV[2]) if len(tV)>2 else Point3D(tV[0], tV[1], 0)
                for i in range(len(normalPointMatrices)):
                    normalPointMatrices[i] = translate(normalPointMatrices[i], tPoint)    
                self.object.updateTransform()    

        if(len(self.transformations) > 0):
            self.object.points = list(map(lambda x: Point3D(x.item(0), x.item(1), x.item(2)), normalPointMatrices))
            self.object.normalizedPoints = list(map(lambda point: getNormalPoint(point, self.window), self.object.points))
            self.object.renderPoints = applyClipping(self.object.type, self.object.normalizedPoints, self.window)
            self.repaint()
        
        self.close()    
        
    def removeFromList(self):  
        index = self.transformList.currentRow()
        if(index >= 0):
            self.transformations.pop(index)
            self.transformList.takeItem(index)

    def setRotationAxis(self, axis: Axis):
        self.axis = axis
    