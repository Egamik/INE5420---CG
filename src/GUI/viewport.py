from typing import List, Tuple

from PyQt5.QtGui import QPainter, QColor, QImage, QPen
from PyQt5.QtWidgets import QLabel

from graphic_obj import GraphicObject
from base.point import Point3D, Point2D
from utils.clipping import applyClipping

class Viewport:
    def __init__(self, x: int, y: int, width: int, height: int):
        # Canva center
        self.x:int = int(x)
        self.y:int = int(y)
        # Canva dimensions
        self.width:int = int(width)
        self.height:int = int(height)
        self.objList: List[GraphicObject] = []

    def formatPoints(self, points: List[Point3D]):
        f_points : List[Point3D] = []
        for point in points:
            point_x = point[0] + self.x
            point_y = point[1] + self.y
            f_points.append(Point3D(point_x, point_y, 1))
        return f_points

    def addObject(self, obj: GraphicObject):
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
                new_point = Point3D(point.x + x, point.y + y, point.z)
                updated_pts.append(new_point)
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
        self.resize(int(width), int(height))
        self.image = QImage(int(width), int(height), QImage.Format_ARGB32)
        self.image.fill(QColor("white"))  # White background
        # Padding
        self.x_min = 20
        self.y_min = 20
        self.view_w = self.image.width() - (2 * self.x_min)
        self.view_h = self.image.height() - (2 * self.y_min)
        self.center_x = self.x_min + (self.image.width() / 2)
        self.center_y = self.y_min + (self.image.height() / 2)
        
        self.viewport = Viewport(int(self.view_w / 2), int(self.view_h / 2), self.view_w, self.view_h)
        
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

    def getObjectList(self):
        return self.viewport.getObjectList()
    
    def setObjectList(self, obj_list: List[GraphicObject]):
        self.viewport.setObjectList(obj_list)
    
    # Returns boundary points clockwise
    def getBoundaries(self) -> List[Point2D]:
        """ Get points for top left and bottom right """
        bounds: List[Point2D] = []
        top_l    =  Point2D(self.x_min, self.y_min)
        bottom_r =  Point2D(self.x_min + self.view_w, self.y_min + self.view_h)
        
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
        rect_x = self.image.width() - 2 * self.x_min
        rect_y = self.image.height() - 2 * self.y_min
        painter.drawRect(self.x_min, self.y_min, rect_x, rect_y) 

    def drawObjects(self):
        """ Redraw the objects after clearing or updating the canvas """
        print('Viewport::drawObjects')
        self.image.fill(QColor("white"))  # Clear the image before drawing
        painter = QPainter(self.image)  # Use QPainter to draw on the QImage
        painter.setPen(QPen(QColor("black")))  # Set pen color for drawing
        # Draw clipping bounds
        self.drawBoundingRect(painter)

        for obj in self.viewport.objList:
            
            points = obj.getPoints()
            render_points: List[Point3D] = []
            print('Draw object: ', obj.name, '  color: ', obj.color)
            
            # Transform points
            for point in points:
                x = round(point.x + self.center_x)
                y = round(point.y + self.center_y)
                render_points.append(Point3D(x, y, 1))
            
            clipped_points = applyClipping(render_points, self.getBoundaries())
            
            if clipped_points == None:
                continue
            
            print('Clipped points')
            for f in clipped_points:
                print('x: ', f.x, ' y: ', f.y)
            if len(clipped_points) == 1:
                painter.drawPoint(clipped_points[0].x, clipped_points[0].y)

            elif len(clipped_points) == 2:
                print('Draw line')
                painter.drawLine(clipped_points[0].x, clipped_points[0].y, clipped_points[1].x, clipped_points[1].y)

            elif len(clipped_points) >= 3:
                last_point = clipped_points[0]
                for point in clipped_points[1:]:
                    painter.drawLine(last_point.x, last_point.y, point.x, point.y)
                    last_point = point
        
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