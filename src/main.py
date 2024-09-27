import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsItem, QListWidget, QGraphicsView, QGraphicsScene, QLabel, QAction
from GUI.widgets import ControlWidget
from GUI.dialogs import AddObjectDialog
from GUI.viewport import Viewport, ViewportLayout
from GUI.transform_widget import TransformationWidgets
from utils.formatObject import formatObject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Trabalho 1 CG")
        self.setGeometry(100, 100, 1000, 700)

        # Attributes
        self.poli_count = 0
        self.poli_list = []
        self.pan_scale = 50
        self.zoom_scale = 0.2

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

        # Add/Remove objects buttons
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Object")
        self.removeButton = QPushButton("Remove Object")
        self.addButton.clicked.connect(self.addObject)

        buttonLayout.addWidget(self.removeButton)
        buttonLayout.addWidget(self.addButton)
        left_layout.addLayout(buttonLayout)
        
        # Setup viewport
        self.viewport_layout = ViewportLayout(self, None, 720, 920)

        # Transformation Panel
        trans = TransformationWidgets(self, self.viewport_layout)
        trans_layout = trans.getLayout()
        
        # Control Panel
        controls = ControlWidget(self.on_up, self.on_down, self.on_left, self.on_right, self.zoom_in, self.zoom_out)
        control_layout = controls.getLayout()

        left_layout.addLayout(trans_layout)
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
        # insert_menu = menu_bar.addMenu("Insert")

        save_action = QAction("Save", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(save_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def addObject(self):
        dialog = AddObjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print('Add object')
            obj = formatObject(dialog.getPointData(), self.poli_count)
            self.viewport_layout.addObject(obj)
            self.viewport_layout.drawObjects()

    def drawViewport(self):
        self.viewport_layout.drawObjects()

    def on_up(self):
        print('Up')
        self.viewport_layout.addToPoints(0, -self.pan_scale)
        self.viewport_layout.drawObjects()
    
    def on_down(self):
        print('Down')
        self.viewport_layout.addToPoints(0, self.pan_scale)
        self.viewport_layout.drawObjects()

    def on_left(self):
        print('left')
        self.viewport_layout.addToPoints(-self.pan_scale, 0)
        self.viewport_layout.drawObjects()

    def on_right(self):
        print('right')
        self.viewport_layout.addToPoints(self.pan_scale, 0)
        self.viewport_layout.drawObjects()

    def zoom_in(self):
        # Calculate center and scale factor
        center_x = self.viewport_layout.width() / 2
        center_y = self.viewport_layout.width() / 2
        scale_factor = 1 + self.zoom_scale

        for obj in self.viewport_layout.viewport.getObjectList():
            updated_points = []
            for point in obj.getPoints():
                # Calculate the offset of the point from the center of the viewport
                offset_x = point[0] - center_x
                offset_y = point[1] - center_y

                # Apply the scaling factor to the offset
                new_x = center_x + offset_x * scale_factor
                new_y = center_y + offset_y * scale_factor

                updated_points.append((round(new_x), round(new_y)))
            print('Zoom in original points: ', obj.getPoints())
            print('Zoom in new points: ', updated_points)
            # Update the object's points
            obj.setPoints(updated_points)
        
        self.viewport_layout.drawObjects()

    def zoom_out(self):
        center_x = self.viewport_layout.width() / 2
        center_y = self.viewport_layout.width() / 2
        scale_factor = 1 - self.zoom_scale

        for obj in self.viewport_layout.viewport.getObjectList():
            updated_points = []
            for point in obj.getPoints():
                # Calculate the offset of the point from the center of the viewport
                offset_x = point[0] - center_x
                offset_y = point[1] - center_y

                # Apply the scaling factor to the offset
                new_x = center_x + offset_x * scale_factor
                new_y = center_y + offset_y * scale_factor

                updated_points.append((round(new_x), round(new_y)))
            print('Zoom out original points: ', obj.getPoints())
            print('Zoom out new points: ', updated_points)
            # Update the object's points
            obj.setPoints(updated_points)
        
        self.viewport_layout.drawObjects()

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
