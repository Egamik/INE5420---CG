from typing import Tuple
from PyQt5.QtWidgets import QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget
from enumerators.graphic_object_type import GraphicObjectType 
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

class SelectObjectTypeWidget(QWidget):
    def __init__(self, createInstance, name, listPoints, updateObjectList, repaint):
        super().__init__()
        self.listPoints = listPoints
        self.objectName = name
        self.createInstance = createInstance
        self.updateObjectList = updateObjectList
        self.repaint = repaint
        self.layout = self.setupAppWindowUI(525, 250)
        self.layout.addLayout(self.setupObjectsUI())
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupObjectsUI(self) -> QVBoxLayout:    
        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 30, 0)
       
        layout.addLayout(self.setRadioButtons())
        layout.addLayout(self.setSelectButton())
        layout.addLayout(self.layout)
        return layout 

    def setRadioButtons(self) -> QVBoxLayout:
        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        self.selectObjectType = QLabel()

        self.selectObjectType.setText("Select Object Type")

        self.polygonRadio = QRadioButton('Polygon')
        self.bezierCurveRadio = QRadioButton('Bezier Curve')
        self.bSplineRadio = QRadioButton('B Spline')


        layout.addWidget(self.selectObjectType)
        layout.addWidget(self.polygonRadio)
        layout.addWidget(self.bezierCurveRadio)
        layout.addWidget(self.bSplineRadio)
        
        return layout

    def setSelectButton(self) -> QVBoxLayout:
        layout: QVBoxLayout = QVBoxLayout()

        self.selectButton = QPushButton()
        self.selectButton.setText("Select")
        self.selectButton.setMaximumWidth(55)

       
        layout.addWidget(self.selectButton)
        self.selectButton.clicked.connect(self.checkSelection)
       
        return layout

    def setupAppWindowUI(self, width, height) -> QHBoxLayout:
        layout: QHBoxLayout = QHBoxLayout(self)
        self.resize(width, height)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #303030;"
                       "color: white"
        )
        self.setWindowTitle('Select Object Type Menu')

        return layout

    def checkSelection(self):
        if(self.bezierCurveRadio.isChecked()):
            self.createInstance(self.listPoints, self.objectName, GraphicObjectType.BezierCurve)
            self.updateObjectList()
            self.repaint()
            self.close()
        elif(self.bSplineRadio.isChecked()):
            self.createInstance(self.listPoints, self.objectName, GraphicObjectType.BSpline)     
            self.updateObjectList()
            self.repaint()    
            self.close()
        else:
            self.createInstance(self.listPoints, self.objectName, GraphicObjectType.Polygon)
            self.updateObjectList()
            self.repaint() 
            self.close()
            
      

               

            
