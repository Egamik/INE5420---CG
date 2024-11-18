from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QRadioButton
from GUI.canva import Viewport
from base.point import Point3D
from base.graphic_obj import GraphicObject
from utils.transform_utils import normalizePoint, transform

class ControlWidget(QWidget):
    def __init__(self, parent, getSelectedObject, viewport: Viewport, repaintView):
        super().__init__(parent)
        
        self.viewport = viewport

        self.main_layout = QVBoxLayout()
        self.control_layout = QGridLayout()
        self.radio_layout = QHBoxLayout()
        self.getSelectedObject = getSelectedObject
        self.repaintView = repaintView

        # Transformation selection
        self.is_vp_trans = False
        self.vp_trans_radio = QRadioButton("Viewport")
        self.obj_trans_radio = QRadioButton("Object")
        self.vp_trans_radio.toggled.connect(self.setTransType(True))
        self.obj_trans_radio.toggled.connect(self.setTransType(False))
        self.radio_layout.addWidget(self.vp_trans_radio)
        self.radio_layout.addWidget(self.obj_trans_radio)
        
        # Control buttons
        self.zoomin_button = QPushButton("+🔍")
        self.zoomout_button = QPushButton("-🔍")
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.left_button = QPushButton("←")
        self.right_button = QPushButton("→")
        
        # self.zoomin_button.clicked.connect(zoom_in)
        # self.zoomout_button.clicked.connect(zoom_out)
        self.up_button.clicked.connect(self.onUp)
        self.down_button.clicked.connect(self.onDown)
        self.left_button.clicked.connect(self.onLeft)
        self.right_button.clicked.connect(self.onRight)

        self.control_layout.addWidget(self.zoomin_button, 1, 0)
        self.control_layout.addWidget(self.zoomout_button, 1, 2)
        self.control_layout.addWidget(self.up_button, 1, 1)
        self.control_layout.addWidget(self.down_button, 3, 1)
        self.control_layout.addWidget(self.left_button, 2, 0)
        self.control_layout.addWidget(self.right_button, 2, 2)
        
        self.main_layout.addLayout(self.radio_layout)
        self.main_layout.addLayout(self.control_layout)
    
    def getLayout(self):
        return self.main_layout

    def setTransType(self, type: bool):
        self.is_vp_trans = type
            
        
    def onUp(self):
        if not self.is_vp_trans:
            obj: GraphicObject = self.getSelectedObject()
            if (obj == None):
                print('No object selected')
                return

            n_points = obj.getNormalizedPoints()
            t_point = Point3D(0, 10, 0)

            for i in range(len(n_points)):
                n_points[i] = transform(n_points[i], t_point)

            updated_points = list(map(lambda x: Point3D(x.item(0), x.item(1), 1), n_points))
            obj.setPoints(updated_points)
        # else:
        #     self.viewport.
        self.repaintView()
    
    def onDown(self):
        if not self.is_vp_trans:
            obj: GraphicObject = self.getSelectedObject()
            if (obj == None):
                return
            
            n_points = obj.getNormalizedPoints()
            t_point = Point3D(0, -10, 0)
            
            for i in range(len(n_points)):
                n_points[i] = transform(n_points[i], t_point)

            updated_points = list(map(lambda x: Point3D(x.item(0), x.item(1), 1), n_points))
            obj.setPoints(updated_points)
        self.repaintView()
        
    def onLeft(self):
        if not self.is_vp_trans:
            obj: GraphicObject = self.getSelectedObject()
            if (obj == None):
                return
            
            n_points = obj.getNormalizedPoints()
            t_point = Point3D(-10, 0, 0)
            
            for i in range(len(n_points)):
                n_points[i] = transform(n_points[i], t_point)

            updated_points = list(map(lambda x: Point3D(x.item(0), x.item(1), 1), n_points))
            obj.setPoints(updated_points)
        self.repaintView()
        
    def onRight(self):
        if not self.is_vp_trans:
            obj: GraphicObject = self.getSelectedObject()
            if (obj == None):
                return
            
            n_points = obj.getNormalizedPoints()
            t_point = Point3D(10, 0, 0)
            
            for i in range(len(n_points)):
                n_points[i] = transform(n_points[i], t_point)

            updated_points = list(map(lambda x: Point3D(x.item(0), x.item(1), 1), n_points))
            obj.setPoints(updated_points)
        self.repaintView()