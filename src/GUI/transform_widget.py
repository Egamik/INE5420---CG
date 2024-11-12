from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QRadioButton,
    QLabel, QSpinBox, QPushButton, QButtonGroup, QFrame, QMessageBox
)
from GUI.canva import Viewport
from base.axis import Axis
from base.graphic_obj import GraphicObject
from utils.matrix_utils import getCenterPointMatrix
from utils.transform_utils import normalizePoint, rotateAroundOrigin, rotateAroundPoint
from base.point import Point3D

class TransformationWidgets(QWidget):
    def __init__(self, parent, getObject, viewport: Viewport, repaintView):
        super().__init__(parent)
        
        # Object to be used in transformations
        self.object: GraphicObject # Has to be initialized before usage
        self.point = Point3D(0, 0, 0)
        self.axis = Axis.Z
        self.getSelectedObject = getObject
        self.repaintView = repaintView
        
        # Title Label
        title = QLabel('Transformation Controls')
        title.setStyleSheet("font-weight: bold; font-size: 16px")
        rotate_label = QLabel('Rotate Around:')
        rotate_label.setStyleSheet("font-size: 14px;")
        
        # Layouts
        self.main_layout = QVBoxLayout()
        self.axis_layout = QHBoxLayout()
        self.radial_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.input_layout = QFormLayout()
        self.input_frame = QFrame()
        self.input_frame.setLayout(self.input_layout)
        
        # Radio Buttons
        self.axis_x = QRadioButton('X')
        self.axis_y = QRadioButton('Y')
        self.axis_z = QRadioButton('Z')
        self.axis_z.setChecked(True)
        self.rotate_zero = QRadioButton('Origin')
        self.rotate_point = QRadioButton('Point')
        self.rotate_center = QRadioButton('Center')
        self.rotate_zero.setChecked(True)  # Default selection
        
        # Button Group for mutual exclusivity
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.rotate_zero)
        self.radio_group.addButton(self.rotate_point)
        self.radio_group.addButton(self.rotate_center)
        self.radio_group.buttonClicked.connect(self.onRadioButtonClicked)
        
        # Add Radio Buttons to Layout
        self.radial_layout.addWidget(self.rotate_zero)
        self.radial_layout.addWidget(self.rotate_point)
        self.radial_layout.addWidget(self.rotate_center)
        
        # Button Group for axis selection
        self.axis_group = QButtonGroup()
        self.axis_group.addButton(self.axis_x)
        self.axis_group.addButton(self.axis_y)
        self.axis_group.addButton(self.axis_z)
        self.axis_group.buttonClicked.connect(self.onAxisClicked)
        
        self.axis_layout.addWidget(self.axis_x)
        self.axis_layout.addWidget(self.axis_y)
        self.axis_layout.addWidget(self.axis_z)
        
        # Spin Boxes for Point Coordinates
        self.x_input = QSpinBox()
        self.y_input = QSpinBox()
        self.z_input = QSpinBox()
        self.x_input.setValue(0)        
        self.y_input.setValue(0)        
        self.z_input.setValue(0)
        
        # Labels
        x_label = QLabel('X:')
        y_label = QLabel('Y:')
        z_label = QLabel('Z:')
        
        # Add Spin Boxes to Form Layout
        self.input_layout.addRow(x_label, self.x_input)
        self.input_layout.addRow(y_label, self.y_input)
        self.input_layout.addRow(z_label, self.z_input)
        
        # Initially hide spin boxes if not "Point" is selected
        self.input_frame.hide()
        
        # Rotate Buttons
        self.rotate_left_btn = QPushButton('Rotate Left')
        self.rotate_right_btn = QPushButton('Rotate Right')
        
        # Connect Buttons to Handlers
        self.rotate_left_btn.clicked.connect(self.rotateLeft)
        self.rotate_right_btn.clicked.connect(self.rotateRight)
        
        # Add Rotate Buttons to Layout
        self.button_layout.addWidget(self.rotate_left_btn)
        self.button_layout.addWidget(self.rotate_right_btn)
        
        # Assemble Main Layout
        self.main_layout.addWidget(title)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addWidget(rotate_label)
        self.main_layout.addLayout(self.radial_layout)
        self.main_layout.addWidget(self.input_frame)
        self.main_layout.addLayout(self.button_layout)
        
        
    def getLayout(self):
        return self.main_layout

    def setSelectedObject(self, object: GraphicObject):
        print('Selected object: ', object.name)
        self.object = object

    def onAxisClicked(self, button):
        if button == self.axis_x:
            self.axis = Axis.X
        elif button == self.axis_y:
            self.axis = Axis.Y
        else:
            self.axis = Axis.Z  
        
    def onRadioButtonClicked(self, button):
        """Show or hide spin boxes based on the selected radio button."""
        if button == self.rotate_point:
            self.input_frame.show()
        else:
            self.input_frame.hide()
        self.input_frame.repaint()

    def rotateLeft(self):
        """Handle the rotate left action based on selected option."""
        selected_obj: GraphicObject = self.getSelectedObject()
        if (selected_obj == None):
            QMessageBox.warning(self, "Selection Error", "Select object before operations")
            return
        self.setSelectedObject(selected_obj)
        
        if self.rotate_zero.isChecked():
            self.rotateAroundOrigin('left')
        
        elif self.rotate_point.isChecked():
            self.point = self.getPoint()
            self.rotateAroundPoint('left')
            
        elif self.rotate_center.isChecked():
            self.rotateAroundCenter('left')
        
        self.repaintView()

    def rotateRight(self):
        """Handle the rotate right action based on selected option."""
        selected_obj = self.getSelectedObject()
        if (selected_obj == None):
            QMessageBox.warning(self, "Selection Error", "Select object before operations")
            return
        self.setSelectedObject(selected_obj)
        
        if self.rotate_zero.isChecked():
            self.rotateAroundOrigin('right')

        elif self.rotate_point.isChecked():
            self.rotateAroundPoint('right')

        elif self.rotate_center.isChecked():
            self.rotateAroundCenter('right')
        
        self.repaintView()
    
    def getPoint(self) -> Point3D:
        """Retrieve the (x, y, z) coordinates from spin boxes."""
        
        x = self.x_input.value()
        y = self.y_input.value()
        z = self.z_input.value()
        
        return Point3D(x, y, z)
    
    def rotateAroundOrigin(self, direction):
        print(f"Rotating around origin to the {direction}.")
        
        obj: GraphicObject = self.getSelectedObject()
        normal_matrices = obj.getNormalizedPoints()
        angle = 10 if (direction == 'left') else 350
        
        for i in range(len(normal_matrices)):
            normal_matrices[i] = rotateAroundOrigin(normal_matrices[i], angle, self.axis)
            
        obj.setPoints(list(map(lambda x: Point3D(x.item(0), x.item(1), x.item(2)), normal_matrices)))
        self.repaintView()
    
    def rotateAroundPoint(self, direction):
        print(f"Rotating around point {self.point} to the {direction}.")
        
        ref_point = Point3D(self.point.x, self.point.y, self.point.z)
        obj: GraphicObject = self.getSelectedObject()        
        normal_matrices = obj.getNormalizedPoints()
        angle: int = 10 if (direction == 'left') else 350
        
        for i in range(len(normal_matrices)):
            normal_matrices[i] = rotateAroundPoint(normal_matrices[i], angle, ref_point, self.axis)
            
        obj.setPoints(list(map(lambda x: Point3D(x.item(0), x.item(1), x.item(2)), normal_matrices)))
        
        self.repaintView()

    def rotateAroundCenter(self, direction):
        print(f"Rotating around center to the {direction}.")
        obj: GraphicObject = self.getSelectedObject()
        
        normal_matrices = obj.getNormalizedPoints()
        center_point = getCenterPointMatrix(normal_matrices)        
        angle: int = 10 if (direction == 'left') else 350
        
        for i in range(len(normal_matrices)):
            normal_matrices[i] = rotateAroundPoint(normal_matrices[i],  angle, center_point, self.axis)
        
        obj.setPoints(list(map(lambda x: Point3D(x.item(0), x.item(1), x.item(2)), normal_matrices)))
        
        self.repaintView()

