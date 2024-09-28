import sys
from typing import List
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsItem, QListWidget, QGraphicsView, QGraphicsScene, QLabel, QAction
from GUI.widgets import ControlWidget
from GUI.dialogs import AddObjectDialog
from GUI.viewport import Viewport, ViewportLayout
from GUI.transform_widget import TransformationWidgets
from GUI.object_viewer import ObjectTableWidget
from graphic_obj import GraphicObject
from utils.formatObject import formatObject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Trabalho 1 CG")
        self.setGeometry(100, 100, 1000, 700)

        # Attributes
        self.poli_count: int = 0
        self.poli_list: List[GraphicObject] = []
        self.pan_scale: int = 50
        self.zoom_scale: float = 0.2

        # Create Menu bar
        self.createMenuBar()

        # Main Layout
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        # GUI components
        self.viewport_layout = ViewportLayout(self, None, 720, 450)
        self.object_list = ObjectTableWidget(self)
        self.trans_controls = TransformationWidgets(self, self.object_list.getSelectedObject, self.viewport_layout.drawObjects)
        self.controls = ControlWidget(self, self.object_list.getSelectedObject, self.viewport_layout.drawObjects)
        trans_layout = self.trans_controls.getLayout()
        control_layout = self.controls.getLayout()

        # Left components
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Object")
        self.removeButton = QPushButton("Remove Object")
        self.addButton.clicked.connect(self.addObject)
 

        # Object List
        buttonLayout.addWidget(self.removeButton)
        buttonLayout.addWidget(self.addButton)
        left_layout.addWidget(QLabel("Object List"))
        left_layout.addWidget(self.object_list.table)
        left_layout.addLayout(buttonLayout)
        left_layout.addLayout(trans_layout)
        left_layout.addLayout(control_layout)
        
        # Add Left Layout to Main Layout
        main_layout.addLayout(left_layout, 1)

        # Setup viewport
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
            self.object_list.addObject(obj)
            self.viewport_layout.addObject(obj)
            self.viewport_layout.drawObjects()
    
    def removeObject(self):
        print('Remove object')
        self.viewport_layout.drawObjects()

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
