from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox
from GUI.viewport import Viewport, ViewportLayout

class ControlWidget(QWidget):
    def __init__(self, on_up, on_down, on_left, on_right, zoom_in, zoom_out):
        super().__init__(None)

        self.control_layout = QGridLayout()
        # self.zoom_scale = 0.5
        # self.pan_scale = 100

        # Control buttons
        self.zoomin_button = QPushButton("+🔍")
        self.zoomout_button = QPushButton("-🔍")
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.left_button = QPushButton("←")
        self.right_button = QPushButton("→")
        
        self.zoomin_button.clicked.connect(zoom_in)
        self.zoomout_button.clicked.connect(zoom_out)
        self.up_button.clicked.connect(on_up)
        self.down_button.clicked.connect(on_down)
        self.left_button.clicked.connect(on_left)
        self.right_button.clicked.connect(on_right)

        self.control_layout.addWidget(self.zoomin_button, 1, 0)
        self.control_layout.addWidget(self.zoomout_button, 1, 2)
        self.control_layout.addWidget(self.up_button, 1, 1)
        self.control_layout.addWidget(self.down_button, 3, 1)
        self.control_layout.addWidget(self.left_button, 2, 0)
        self.control_layout.addWidget(self.right_button, 2, 2)
    
    def getLayout(self):
        return self.control_layout

