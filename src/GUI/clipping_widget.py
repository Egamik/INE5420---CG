from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton

class LineClippingWidget(QWidget):
    def __init__(self, setClipType):
        super().__init__()

        # Set up the layout
        self.main_layout = QVBoxLayout()
        radio_layout = QHBoxLayout()
        
        self.setClipType = setClipType

        # Create and add the label
        label = QLabel("Line Clipping")
        self.main_layout.addWidget(label)

        # Create radio buttons
        self.radio1 = QRadioButton("Cohen-Sutherland")
        self.radio2 = QRadioButton("Liang-Barsky")
        self.radio1.toggled.connect(self.setType)
        self.radio2.toggled.connect(self.setType)

        # Add radio buttons to the layout
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        self.main_layout.addLayout(radio_layout)

    def getLayout(self):
        return self.main_layout
    
    def setType(self):
        if self.radio1.isChecked():
            self.setClipType(True)
        elif self.radio2.isChecked():
            self.setClipType(False)