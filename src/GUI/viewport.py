from typing import List, Tuple

from PyQt5.QtGui import QPainter, QColor, QImage, QPen
from PyQt5.QtWidgets import QLabel

from graphic_obj import GraphicObject

class Viewport:
    def __init__(self, x: int, y: int, width: int, height: int):
        # Canva center
        self.x:int = int(x)
        self.y:int = int(y)
        # Canva dimensions
        self.width:int = int(width)
        self.height:int = int(height)
        self.objList: List[GraphicObject] = []

    def formatPoints(self, points: List[Tuple]):
        f_points : List[Tuple] = []
        for point in points:
            point_x = point[0] + self.x
            point_y = point[1] + self.y
            f_points.append((point_x, point_y))
        return f_points

    def addObject(self, obj: GraphicObject):
        updated_points = self.formatPoints(obj.getPoints())
        obj.setPoints(updated_points)
        self.objList.append(obj)
        print('Add object to scene: ', obj.name)

    def removeObject(self, obj: GraphicObject):
        self.objList.remove(obj)
        print('Remove object from scene: ', obj.name)

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

    def __init__(self, parent, window, width, height):
        super().__init__(parent=parent)
        self.window = window
        # Padding
        self.x_min = 60
        self.y_min = 80
        self.view_w = width - (2 * self.x_min)
        self.view_h = height - (2 * self.y_min)
        self.viewport = Viewport(int(self.view_w / 2), int(self.view_h / 2), self.view_w, self.view_h)
        
        self.resize(int(width), int(height))
        self.image = QImage(int(width), int(height), QImage.Format_ARGB32)
        self.image.fill(QColor("white"))  # White background
        
        painter = QPainter(self.image)
        self.drawBoundingRect(painter)
        painter.end()
        self.update()

    def addObject(self, object: GraphicObject):
        self.viewport.addObject(object)

    def removeObject(self, object: GraphicObject):
        self.viewport.removeObject(object)

    def addToPoints(self, x: int, y: int):
        self.viewport.addToPoints(x, y)

    # Returns boundary points clockwise
    def getBoundaries(self):
        
        bounds: List[Tuple] = []
        top_l    =  (self.x_min, self.y_min)
        bottom_r =  (self.x_min + self.view_w, self.y_min + self.view_h)
        
        bounds.append(top_l)
        bounds.append(bottom_r)
        return bounds

    def clearCanva(self):
        # Clear the canvas by filling white
        print('Clear canvas')
        self.image.fill(QColor("white"))
        self.viewport.clear()
        painter = QPainter(self.image)  
        painter.setPen(QPen(QColor("black")))  
        self.drawBoundingRect(painter)
        painter.end()
        self.update()  # Repaint

    def drawBoundingRect(self, painter: QPainter):
        rect_x = self.image.width() - self.x_min
        rect_y = self.image.height() - self.y_min
        print('DrawObjects view bounds x: ', rect_x, '  Y:', rect_y)
        painter.drawRect(int(self.x_min/2), int(self.y_min/2), rect_x, rect_y) # 20 padding

    def drawObjects(self):
        # Redraw the objects after clearing or updating the canvas
        self.image.fill(QColor("white"))  # Clear the image before drawing
        painter = QPainter(self.image)  # Use QPainter to draw on the QImage
        painter.setPen(QPen(QColor("black")))  # Set pen color for drawing
        # Draw clipping bounds
        self.drawBoundingRect(painter)
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
                painter.drawLine(points[0][0], points[0][1], last_point[0], last_point[1])
        painter.end()
        self.update()  # Request a repaint to show the changes

  # Override the paintEvent to display the QImage on the widget
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image)
        painter.end()

    def resizeEvent(self, event):
        # Get new size from the event
        new_width = event.size().width()
        new_height = event.size().height()

        # Update the size of the image
        self.image = QImage(new_width, new_height, QImage.Format_ARGB32)
        self.image.fill(QColor("white"))

        # Adjust the viewport size accordingly
        self.viewport.width = new_width - (2 * self.x_min)
        self.viewport.height = new_height - (2 * self.y_min)
        # print(f"Resized: image to {new_width}x{new_height}, viewport to {self.viewport.width}x{self.viewport.height}")
        self.drawObjects()

        # Call the parent class's resize event handler (important for layout managers)
        super().resizeEvent(event)