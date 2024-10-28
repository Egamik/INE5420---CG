from typing import List
from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QLabel, QSpinBox, QLineEdit, QCheckBox
from base.graphic_obj import GraphicObjectType
from base.point import Point3D
 
class AddObjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new object")
        self.setGeometry(100, 100, 300, 200)

        # Dialog box layout
        self.main_layout = QVBoxLayout(self)

        # Curve
        self.main_layout.addWidget(QLabel("Curve"))
        self.curve = False
        is_curve = QCheckBox("Bezier")
        is_curve.stateChanged.connect(self.curveSelected)
        self.main_layout.addWidget(is_curve)
        
        # Input for number of points
        self.main_layout.addWidget(QLabel("Number of Points:"))
        self.num_points_spinbox = QSpinBox(self)
        self.num_points_spinbox.setMinimum(1)  # At least 1 point
        self.num_points_spinbox.valueChanged.connect(self.update_point_inputs)
        self.main_layout.addWidget(self.num_points_spinbox)

        # Placeholder for coordinate input forms
        self.point_inputs_layout = QFormLayout()
        self.main_layout.addLayout(self.point_inputs_layout)

        # Add Ok/Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        # Store input fields for the coordinates
        self.point_inputs = []
        self.update_point_inputs()

    def curveSelected(self):
        print('toggle curve')
        self.curve = not self.curve
        self.num_points_spinbox.setMinimum(4)
        
    def update_point_inputs(self):
        # Clear current input fields
        for i in reversed(range(self.point_inputs_layout.count())):
            widget_item = self.point_inputs_layout.itemAt(i)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.deleteLater()

        # Get the number of points
        num_points = self.num_points_spinbox.value()

        # Create new input fields for each point (X, Y)
        self.point_inputs = []
        for i in range(num_points):
            x_input = QLineEdit(self)
            y_input = QLineEdit(self)
            z_input = QLineEdit(self)
            self.point_inputs_layout.addRow(f"Point {i + 1} X:", x_input)
            self.point_inputs_layout.addRow(f"Point {i + 1} Y:", y_input)
            self.point_inputs_layout.addRow(f"Point {i + 1} Z:", z_input)
            self.point_inputs.append((x_input, y_input, z_input))

    def getPointData(self) -> List[Point3D]:
        # Retrieve data from the input fields
        points = []
        for x_input, y_input, z_input in self.point_inputs:
            try:
                x = int(x_input.text())
                y = int(y_input.text())
                z = int(z_input.text())
                points.append(Point3D(x, y, z))
            except ValueError:
                # Handle cases where the input is not a valid number
                pass
        return points

    def getObjectType(self) -> GraphicObjectType:
        if (self.curve):
            return GraphicObjectType.BezierCurve
        if (len(self.point_inputs) == 1):
            return GraphicObjectType.Point
        elif(len(self.point_inputs) == 2):
            return GraphicObjectType.Line
        else:
            return GraphicObjectType.Polygon