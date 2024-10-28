from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from base.point import Point3D
from base.graphic_obj import GraphicObject
from utils.transform_utils import transform

class ControlWidget(QWidget):
    def __init__(self, parent, getSelectedObject, repaintView):
        super().__init__(parent)

        self.control_layout = QGridLayout()
        self.getSelectedObject = getSelectedObject
        self.repaintView = repaintView

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
    
    def getLayout(self):
        return self.control_layout

    def onUp(self):
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
        self.repaintView()
    
    def onDown(self):
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