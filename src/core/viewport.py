from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPen
from PyQt5.QtWidgets import QWidget, QLabel

from model.base_object import GraphicObject

class Viewport:
  def __init__(self, x: int, y: int, width: int, height: int):
    self.x:int = int(x)
    self.y:int = int(y)
    self.width:int = int(width)
    self.height:int = int(height)
    self.displayFile: List[GraphicObject] = []

  def addObject(self, obj: GraphicObject):
    self.displayFile.append(obj)
    print('Add object to scene: ', obj.name, obj.getPoints())
    
  def removeObject(self, obj: GraphicObject):
    self.displayFile.remove(obj)
    print('Remove object from scene: ', obj.name, obj.getPoints())

class ViewportLayout(QLabel):
  def __init__(self, parent, viewport, window, width, height):
    super().__init__(parent=parent)
    self.window = window
    self.viewport = viewport
    self.resize(int(width), int(height))
    canvas = QPixmap(int(width), int(height))
    self.setPixmap(canvas)

  def paintEvent(self, e):
    canvas = self.pixmap()
    painter = QPainter(self)
    painter.drawPixmap(canvas.rect(), canvas)
    painter.end()

  def drawDisplayFile(self):
    canvas = self.pixmap()
    canvas.fill(QColor("white"))
    painter = QPainter(canvas)
    for obj in self.viewport.displayFile:
      painter.setPen(obj.color)
      obj.draw(painter, self.viewport, self.window)
    painter.setPen(QColor("black"))
    painter.drawRect(self.viewport.x, self.viewport.y, self.viewport.width, self.viewport.height)
    painter.end()