import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsItem, QListWidget, QGraphicsView, QGraphicsScene, QLabel, QAction
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPointF
from widgets import ControlWidget
from dialogs import AddObjectDialog
from graphic_obj import Point, Line, Polygon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Trabalho 1 CG")
        self.setGeometry(100, 100, 1000, 700)
        # Attributes
        self.poli_count = 0

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

        # Control Panel
        controls = ControlWidget(self.onPanUp, self.onPanDown, self.onPanLeft, self.onPanRight, self.onZoomIn, self.onZoomOut)
        control_layout = controls.getLayout()

        left_layout.addLayout(control_layout)

        # Add Left Layout to Main Layout
        main_layout.addLayout(left_layout, 1)

        right_layout = QGridLayout()
        right_layout.addWidget(QLabel("Viewport"))

        # Graphics Viewport
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        right_layout.addWidget(self.graphics_view)

        main_layout.addLayout(right_layout, 2)

        # Central Widget setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Menu")
        insert_menu = menu_bar.addMenu("Insert")

        exit_action = QAction("Exit", self)
        add_action = QAction("Add Object", self)
        add_action.triggered.connect(self.add2DObject)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)
        insert_menu.addAction(add_action)

    def add2DObject(self):
        dialog = AddObjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # Corrected dialog response comparison
            point_count = dialog.getSelectedObjectType()
            points = dialog.getPointData()
            if point_count == 1:
                # Store item on list
                item = Point("P", points[0][0], points[0][1])
                self.scene.addEllipse(points[0][0] - 2.5, points[0][1] - 2.5, 5, 5, QPen(Qt.black), QBrush(Qt.black))
            elif point_count == 2:
                # Draw Line
                item = Line("L", points[0][0], points[0][1], points[1][0], points[1][1])
                self.scene.addLine(item.points[0][0], item.points[0][1], item.points[1][0], item.points[1][1], QPen(Qt.black, 2))
            else:
                # Draw Polygon
                item = Polygon("Pol", points)
                polygon = QPolygonF([QPointF(p[0], p[1]) for p in item.points])
                self.scene.addPolygon(polygon, QPen(Qt.black, 2), QBrush(Qt.NoBrush))
            print(f'Add {point_count}!')

    # def drawObject(self, item: QGraphicsItem):
    #     print('Draw Object')
    #     if isinstance(item, Point):
    #         self.scene.addEllipse(item.points[0][0] - 2.5, item.points[0][1] - 2.5, 5, 5, QPen(Qt.black), QBrush(Qt.black))

    def onZoomIn(self):
        print('Zoom in')
        self.graphics_view.scale(1.2, 1.2)

    def onZoomOut(self):
        print('Zoom out')
        self.graphics_view.scale(0.8, 0.8)

    def onPanUp(self):
        print('Pan up')
        self.graphics_view.translate(0, -50)
    
    def onPanDown(self):
        print('Pan down')
        self.graphics_view.translate(0, 50)

    def onPanLeft(self):
        print('Pan left')
        self.graphics_view.translate(-50, 0)

    def onPanRight(self):
        print('Pan right')
        self.graphics_view.translate(50, 0)

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
