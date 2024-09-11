import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, QGraphicsView, QGraphicsScene, QLabel, QAction, QComboBox, QFormLayout, QDialogButtonBox
from widgets import ControlWidget

# class AddObjectDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add new object")
#         self.setGeometry(100, 100, 300, 200)

#         layout = QFormLayout(self)
#         self.object_type = QComboBox(self)
#         self.object_type.addItems(["Point", "Line", "Polygon"])
#         layout.addRow("Object Type:", self.object_type)

#         # Dialog buttons
#         self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         self.button_box.accepted.connect(self.accept)
#         self.button_box.rejected.connect(self.reject)

#         layout.addWidget(self.button_box)

#     def get_selected_object_type(self):
#         return self.object_type.currentText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Trabalho 1 CG")
        self.setGeometry(100, 100, 1000, 700)

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

        # # Control Panel
        controls = ControlWidget(self.onPanUp, self.onPanDown, self.onPanLeft, self.onPanRight, self.onZoomIn, self.onZoomOut)
        control_layout = controls.getLayout()

        left_layout.addLayout(control_layout)

        # Add Left Layout to Main Layout
        main_layout.addLayout(left_layout)

        right_layout = QGridLayout()
        right_layout.addWidget(QLabel("Viewport"))

        # Graphics Viewport
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        right_layout.addWidget(self.graphics_view)

        main_layout.addLayout(right_layout)

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
            object_type = dialog.get_selected_object_type()
            print(f'Add {object_type}!')

    def drawObject(self, data):
        print('Draw Object')
        self.scene.addPolygon()

    def onZoomIn(self):
        print('Zoom in')

    def onZoomOut(self):
        print('Zoom out')

    def onPanUp(self):
        print('Pan up')
    
    def onPanDown(self):
        print('Pan down')

    def onPanLeft(self):
        print('Pan left')

    def onPanRight(self):
        print('Pan right')

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
