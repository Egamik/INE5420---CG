from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QWidget, QFormLayout, QPushButton, QLineEdit
)

from GUI.viewport import ViewportLayout

class ViewportDialog(QDialog):
    def __init__(self, viewport: ViewportLayout) -> None:
        super().__init__()
        self.viewport = viewport
        self.translations = []
        self.rotations = []
        self.scales = []
        self.setWindowTitle("Viewport Transformations")
        
    def setupTabs(self) -> QTabWidget:
        tabs = QTabWidget()
        
        self.trans_tab = QWidget()
        self.rot_tab = QWidget()
        self.scale_tab = QWidget()
        
        tabs.addTab(self.trans_tab, "Translate")
        tabs.addTab(self.rot_tab, "Rotate")
        tabs.addTab(self.scale_tab, "Scale")
    # def addRotation(self)
    
    def translateLayout(self):
        layout = QFormLayout()
        x = QLineEdit()
        y = QLineEdit()
        z = QLineEdit()
        add_btn = QPushButton("Add")
        