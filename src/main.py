import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsItem, QListWidget, QGraphicsView, QGraphicsScene, QLabel, QAction
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPointF
from GUI.widgets import ControlWidget
from GUI.dialogs import AddObjectDialog
from GUI.viewport import Viewport, ViewportLayout
from graphic_obj import Point, Line, Polygon
from utils.formatObject import formatObject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Trabalho 1 CG")
        self.setGeometry(100, 100, 1000, 700)

        # Attributes
        self.poli_count = 0
        self.view_center = [0, 0]
        self.poli_list = []
        self.pan_scale = 100
        self.zoom_scale = 1.2

        # Create Menu bar
        self.createMenuBar()

        # Main Layout
        main_layout = QHBoxLayout()

        # Object List/Controls Layout
        left_layout = QVBoxLayout()

        # Object List
        left_layout.addWidget(QLabel("Object List"))
        self.object_list = QListWidget(self)
        left_layout.addWidget(self.object_list)

        # Setup viewport
        posMultiplier = 0.2/2
        self.viewport = Viewport(posMultiplier*720, posMultiplier*900, 720, 900)
        self.viewport_layout = ViewportLayout(self, self.viewport, None, 720, 900)
        # self.viewport_layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Control Panel
        controls = ControlWidget(self.on_up, self.on_down, self.on_left, self.on_right, self.zoom_in, self.zoom_out)
        control_layout = controls.getLayout()

        left_layout.addLayout(control_layout)

        # Add Left Layout to Main Layout
        main_layout.addLayout(left_layout, 1)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Viewport"))
        right_layout.addWidget(self.viewport_layout, 3)
        right_layout.addStretch(1)

        main_layout.addLayout(right_layout, 3)

        # Central Widget setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Menu")
        insert_menu = menu_bar.addMenu("Insert")

        save_action = QAction("Save", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        add_action = QAction("Add Object", self)
        add_action.triggered.connect(self.addObject)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(save_action)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        insert_menu.addAction(add_action)

    def addObject(self):
        dialog = AddObjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print('Add object')
            obj = formatObject(dialog.getPointData(), self.poli_count)
            self.viewport.addObject(obj)
            self.viewport_layout.drawObjects()

    def drawViewport(self):
        self.viewport_layout.drawObjects()

    def on_up(self):
        print('Up')
        self.viewport.addToPoints(0, self.pan_scale)
        self.viewport_layout.drawObjects()
    
    def on_down(self):
        print('Down')
        self.viewport.addToPoints(0, -self.pan_scale)
        self.viewport_layout.drawObjects()

    def on_left(self):
        print('left')
        self.viewport.addToPoints(-self.pan_scale, 0)
        self.viewport_layout.drawObjects()

    def on_right(self):
        print('right')
        self.viewport.addToPoints(self.pan_scale, 0)
        self.viewport_layout.drawObjects()

    def zoom_in(self):
        print('Zoom in')
        self.viewport.multPoints(self.zoom_scale, self.zoom_scale)
        self.viewport_layout.drawObjects()

    def zoom_out(self):
        print('Zoom out')
        self.viewport.multPoints(self.zoom_scale, self.zoom_scale)
        self.viewport_layout.drawObjects()

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
