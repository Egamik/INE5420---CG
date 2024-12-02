from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QToolButton, QVBoxLayout, QHBoxLayout

class ArrowsWidget(QWidget):
  def __init__(self, onUp, onDown, onLeft, onRight):
    super(ArrowsWidget, self).__init__(None)

    self.upButton = QToolButton()
    self.upButton.setArrowType(QtCore.Qt.UpArrow)
    self.upButton.clicked.connect(onUp)
    self.upButton.setFixedWidth(75)
    self.downButton = QToolButton()
    self.downButton.setArrowType(QtCore.Qt.DownArrow)
    self.downButton.clicked.connect(onDown)
    self.downButton.setFixedWidth(75)
    self.leftButton = QToolButton()
    self.leftButton.setArrowType(QtCore.Qt.LeftArrow)
    self.leftButton.clicked.connect(onLeft)
    self.leftButton.setFixedWidth(75)
    self.rightButton = QToolButton()
    self.rightButton.setArrowType(QtCore.Qt.RightArrow)
    self.rightButton.clicked.connect(onRight)
    self.rightButton.setFixedWidth(75)

    self.layout: QVBoxLayout = QVBoxLayout()
    self.layout.addWidget(self.upButton,alignment=QtCore.Qt.AlignCenter)
    row = QHBoxLayout()
    row.addWidget(self.leftButton)
    row.addWidget(self.rightButton)
    self.layout.addLayout(row)
    self.layout.addWidget(self.downButton,alignment=QtCore.Qt.AlignCenter)

  def getLayout(self) -> QVBoxLayout:
      return self.layout
