from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QRadioButton,
    QLabel, QSpinBox, QPushButton, QButtonGroup, QFrame
)
from GUI.viewport import ViewportLayout

class TransformationWidgets(QWidget):
    def __init__(self, parent, viewport: ViewportLayout):
        super().__init__(parent)
        
        # Title Label
        title = QLabel('Rotate Around:')
        # title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.viewport = viewport
        # Layouts
        self.main_layout = QVBoxLayout()
        self.radial_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.input_layout = QFormLayout()
        self.input_frame = QFrame()
        self.input_frame.setLayout(self.input_layout)
        
        # Radio Buttons
        self.rotate_zero = QRadioButton('Origin')
        self.rotate_point = QRadioButton('Point')
        self.rotate_center = QRadioButton('Center')
        self.rotate_zero.setChecked(True)  # Default selection
        
        # Button Group for mutual exclusivity
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.rotate_zero)
        self.radio_group.addButton(self.rotate_point)
        self.radio_group.addButton(self.rotate_center)
        self.radio_group.buttonClicked.connect(self.on_radio_button_clicked)
        
        # Add Radio Buttons to Layout
        self.radial_layout.addWidget(self.rotate_zero)
        self.radial_layout.addWidget(self.rotate_point)
        self.radial_layout.addWidget(self.rotate_center)
        
        # Spin Boxes for Point Coordinates
        self.x_input = QSpinBox()
        # self.x_input.setRange(-1000, 1000)
        self.x_input.setValue(0)
        
        self.y_input = QSpinBox()
        # self.y_input.setRange(-1000, 1000)
        self.y_input.setValue(0)
        
        self.z_input = QSpinBox()
        # self.z_input.setRange(-1000, 1000)
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
        self.rotate_left_btn.clicked.connect(self.rotate_left)
        self.rotate_right_btn.clicked.connect(self.rotate_right)
        
        # Add Rotate Buttons to Layout
        self.button_layout.addWidget(self.rotate_left_btn)
        self.button_layout.addWidget(self.rotate_right_btn)
        
        # Assemble Main Layout
        self.main_layout.addWidget(title)
        self.main_layout.addLayout(self.radial_layout)
        self.main_layout.addWidget(self.input_frame)
        self.main_layout.addLayout(self.button_layout)
        
        
    def getLayout(self):
        return self.main_layout
        
    def on_radio_button_clicked(self, button):
        """Show or hide spin boxes based on the selected radio button."""
        if button == self.rotate_point:
            self.input_frame.show()
            self.input_frame.repaint()
        else:
            self.input_frame.hide()
            self.input_frame.repaint()

    
    def rotate_left(self):
        """Handle the rotate left action based on selected option."""
        if self.rotate_zero.isChecked():
            self.rotate_around_origin(direction='left')
        elif self.rotate_point.isChecked():
            point = self.get_point()
            self.rotate_around_point(point, direction='left')
        elif self.rotate_center.isChecked():
            self.rotate_around_center(direction='left')
    
    def rotate_right(self):
        """Handle the rotate right action based on selected option."""
        if self.rotate_zero.isChecked():
            self.rotate_around_origin(direction='right')
        elif self.rotate_point.isChecked():
            point = self.get_point()
            self.rotate_around_point(point, direction='right')
        elif self.rotate_center.isChecked():
            self.rotate_around_center(direction='right')
    
    def get_point(self):
        """Retrieve the (x, y, z) coordinates from spin boxes."""
        x = self.x_input.value()
        y = self.y_input.value()
        z = self.z_input.value()
        return (x, y, z)
    
    # Placeholder methods for rotation actions
    def rotate_around_origin(self, direction):
        print(f"Rotating around origin to the {direction}.")
        # Implement your rotation logic here
    
    def rotate_around_point(self, point, direction):
        print(f"Rotating around point {point} to the {direction}.")
        # Implement your rotation logic here
    
    def rotate_around_center(self, direction):
        print(f"Rotating around center to the {direction}.")
        # Implement your rotation logic here

# Example usage:
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TransformationWidgets()
    window.setWindowTitle("Transformation Widget")
    window.show()
    sys.exit(app.exec_())
