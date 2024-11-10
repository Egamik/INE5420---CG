from typing import List, Tuple
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QLabel,
    QSpinBox, QLineEdit, QCheckBox, QHBoxLayout, QVBoxLayout
)
from base.graphic_obj import GraphicObjectType
from base.point import Point3D

class AddObjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new object")
        self.setGeometry(100, 100, 300, 200)

        # Dialog box layout
        self.main_layout = QVBoxLayout(self)

        # Curve and 3D checkboxes
        self.curve = False
        self.spline = False
        self.obj3D = False
        
        checkboxes = QHBoxLayout()
        is_curve = QCheckBox("Bezier")
        is_spline = QCheckBox("BSpline")
        is_3D = QCheckBox("3D Object")
        
        is_curve.stateChanged.connect(self.curveSelected)
        is_spline.stateChanged.connect(self.splineSelected)
        is_3D.stateChanged.connect(self.selected3d)
        
        checkboxes.addWidget(is_curve)
        checkboxes.addWidget(is_3D)
        self.main_layout.addLayout(checkboxes)
        
        # Input for number of points
        self.main_layout.addWidget(QLabel("Number of Points or Edges:"))
        self.num_points_spinbox = QSpinBox(self)
        self.num_points_spinbox.setMinimum(1)  # At least 1 point/edge
        self.num_points_spinbox.valueChanged.connect(self.update_point_inputs)
        self.main_layout.addWidget(self.num_points_spinbox)

        # Placeholder for coordinate input forms
        self.point_inputs_layout = QVBoxLayout()
        self.main_layout.addLayout(self.point_inputs_layout)

        # Add Ok/Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        # Store input fields for the coordinates or edges
        self.point_inputs: List = []
        self.edge_inputs: List[Tuple] = []
        self.update_point_inputs()

    def curveSelected(self):
        print('toggle curve')
        self.curve = not self.curve
        self.num_points_spinbox.setMinimum(4)
        
    def splineSelected(self):
        self.spline = not self.spline
        self.num_points_spinbox.setMinimum(4)
    
    def selected3d(self):
        print('toggle 3D')
        self.obj3D = not self.obj3D
        self.update_point_inputs()
        
    def update_point_inputs(self):
        # Clear current input fields
        for i in reversed(range(self.point_inputs_layout.count())):
            widget_item = self.point_inputs_layout.itemAt(i)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    # If it's a layout, clear its widgets
                    layout = widget_item.layout()
                    if layout is not None:
                        while layout.count():
                            child = layout.takeAt(0)
                            if child.widget():
                                child.widget().deleteLater()

        # Get the number of points/edges
        num_points = self.num_points_spinbox.value()

        # Create new input fields
        self.point_inputs = []
        self.edge_inputs = []
        
        if self.obj3D:
            # Edge input mode for 3D objects
            for i in range(num_points):
                # Inputs for Point 1
                p1_x_input = QLineEdit(self)
                p1_y_input = QLineEdit(self)
                p1_z_input = QLineEdit(self)
                
                # Inputs for Point 2
                p2_x_input = QLineEdit(self)
                p2_y_input = QLineEdit(self)
                p2_z_input = QLineEdit(self)
                
                # Layout for an edge row
                edge_layout = QHBoxLayout()
                edge_layout.addWidget(QLabel(f"Edge {i + 1} P1 (X, Y, Z):"))
                edge_layout.addWidget(p1_x_input)
                edge_layout.addWidget(p1_y_input)
                edge_layout.addWidget(p1_z_input)
                edge_layout.addWidget(QLabel("P2 (X, Y, Z):"))
                edge_layout.addWidget(p2_x_input)
                edge_layout.addWidget(p2_y_input)
                edge_layout.addWidget(p2_z_input)
                
                # Add layout to main layout
                self.point_inputs_layout.addLayout(edge_layout)
                
                # Append inputs as a tuple of tuples for an edge
                self.edge_inputs.append(((p1_x_input, p1_y_input, p1_z_input),
                                         (p2_x_input, p2_y_input, p2_z_input)))
        else:
            # 2D points input mode
            for i in range(num_points):
                x_input = QLineEdit(self)
                y_input = QLineEdit(self)
                
                # Layout for a point row
                l_input = QHBoxLayout()
                l_input.addWidget(QLabel(f"Point {i + 1} X:"))
                l_input.addWidget(x_input)
                l_input.addWidget(QLabel("Y:"))
                l_input.addWidget(y_input)
                
                self.point_inputs_layout.addLayout(l_input)
                
                self.point_inputs.append((x_input, y_input, None))

    def getPointData(self) -> List[Point3D]:
        # Retrieve data from input fields
        points = []
        if self.obj3D:
            # Return edges as tuples of Point3D
            for (p1_inputs, p2_inputs) in self.edge_inputs:
                try:
                    p1_x, p1_y, p1_z = [int(field.text()) for field in p1_inputs]
                    p2_x, p2_y, p2_z = [int(field.text()) for field in p2_inputs]
                    points.append((Point3D(p1_x, p1_y, p1_z), Point3D(p2_x, p2_y, p2_z)))
                except ValueError:
                    # Handle cases where input is invalid
                    pass
        else:
            # Return individual points
            for x_input, y_input, _ in self.point_inputs:
                try:
                    x = int(x_input.text())
                    y = int(y_input.text())
                    points.append(Point3D(x, y, 0))
                except ValueError:
                    # Handle cases where input is invalid
                    pass
        return points

    def getObjectType(self) -> GraphicObjectType:
        if self.curve:
            return GraphicObjectType.BezierCurve
        
        if self.spline:
            return GraphicObjectType.BSpline
        
        if self.obj3D:
            return GraphicObjectType.Object3D
        
        if len(self.point_inputs) == 1 and not self.obj3D:
            return GraphicObjectType.Point
        elif len(self.point_inputs) == 2 and not self.obj3D:
            return GraphicObjectType.Line
        else:
            return GraphicObjectType.Polygon
