from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QColorDialog
from PyQt5.QtGui import QColor

class ColorPickerWidget(QPushButton):
  def __init__(self):
    super(ColorPickerWidget, self).__init__(None)
    self.setAutoFillBackground(True)
    self.setColor(QColor("black"))
    self.clicked.connect(self.pickColor)

  def pickColor(self):
    self.setColor(QColorDialog.getColor())

  def setColor(self, color):
    self.color: QColor = color
    self.setStyleSheet("background-color: " + self.color.name())

  def getColor(self) -> QColor:
    return self.color