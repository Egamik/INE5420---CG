from typing import List

from PyQt5.QtGui import QPainter, QColor, QImage, QPen
from PyQt5.QtWidgets import QLabel

from graphic_obj import GraphicObject

class Viewport:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x:int = int(x)
        self.y:int = int(y)
        self.width:int = int(width)
        self.height:int = int(height)
        self.objList: List[GraphicObject] = []

    def addObject(self, obj: GraphicObject):
        self.objList.append(obj)
        print('Add object to scene: ', obj.name, obj.getPoints())

    def removeObject(self, obj: GraphicObject):
        self.objList.remove(obj)
        print('Remove object from scene: ', obj.name, obj.getPoints())

    def getObjectList(self):
        return self.objList
    
    def setObjectList(self, objects: List[GraphicObject]):
        self.objList = objects

    def addToPoints(self, x: int, y: int):
        for obj in self.objList:
            updated_pts = []
            for point in obj.getPoints():
                point_l = list(point)
                point_l[0] = point_l[0] + x
                point_l[1] = point_l[1] + y
                point = tuple(point_l)
                updated_pts.append(point)
            obj.setPoints(updated_pts)

    def multPoints(self, x: int, y: int):
        for obj in self.objList:
            updated_pts = []
            for point in obj.getPoints():
                point_l = list(point)
                point_l[0] = point_l[0] * x
                point_l[1] = point_l[1] * y
                point = tuple(point_l)
                updated_pts.append(point)
            obj.setPoints(updated_pts)

    def clear(self):
        self.objList.clear()


class ViewportLayout(QLabel):

    def __init__(self, parent, viewport: Viewport, window, width, height):
        super().__init__(parent=parent)
        self.window = window
        self.viewport = viewport
        self.resize(int(width), int(height))
        self.image = QImage(int(width), int(height), QImage.Format_ARGB32)
        self.image.fill(QColor("white"))  # White background

    def clearCanva(self):
        # Clear the canvas by filling white
        print('Clear canvas')
        self.image.fill(QColor("white"))
        self.viewport.clear()
        self.update()  # Repaint

    def drawObjects(self):
        # Redraw the objects after clearing or updating the canvas
        self.image.fill(QColor("white"))  # Clear the image before drawing
        painter = QPainter(self.image)  # Use QPainter to draw on the QImage
        painter.setPen(QPen(QColor("black")))  # Set pen color for drawing
        for obj in self.viewport.objList:
            points = obj.getPoints()
            print('Draw object: ', points)
            if len(points) == 1:
                painter.drawPoint(points[0][0], points[0][1])
            elif len(points) == 2:
                painter.drawLine(points[0][0], points[0][1], points[1][0], points[1][1])
            elif len(points) >= 3:
                last_point = points[0]
                for point in points[1:]:
                    painter.drawLine(last_point[0], last_point[1], point[0], point[1])
                    last_point = point
                painter.drawLine(last_point[0], last_point[1], points[0][0], points[0][1])
        painter.end()
        self.update()  # Request a repaint to show the changes

  # Override the paintEvent to display the QImage on the widget
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image)
        painter.end()