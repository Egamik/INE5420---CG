from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout

class ArrowsWidget(QWidget):
	def __init__(self, onUp, onDown, onLeft, onRight):
		super(ArrowsWidget, self).__init__(None)

		self.up_button = QPushButton("↑")
		self.down_button = QPushButton("↓")
		self.left_button = QPushButton("←")
		self.right_button = QPushButton("→")
		self.up_button.clicked.connect(onUp)
		self.down_button.clicked.connect(onDown)
		self.left_button.clicked.connect(onLeft)
		self.right_button.clicked.connect(onRight)
    
    
		self.layout: QGridLayout = QGridLayout()
    
		self.layout.addWidget(self.up_button, 0, 1)
		self.layout.addWidget(self.down_button, 2, 1)
		self.layout.addWidget(self.left_button, 1, 0)
		self.layout.addWidget(self.right_button, 1, 2)
    
    
	def getLayout(self) -> QGridLayout:
		return self.layout
