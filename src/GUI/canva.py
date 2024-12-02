from typing import List
from math import radians as rad, tan

from PyQt5.QtGui import QPainter, QColor, QImage, QPen
from PyQt5.QtWidgets import QLabel
from base.graphic_obj import GraphicObject, GraphicObjectType
from base.point import Point3D, Point2D
from base.viewport import Viewport
from utils.clipping import applyClipping
from utils.transform_utils import normalizePoint

class Canva(QLabel):

    def __init__(self, parent, width, height, getClipType):
        super().__init__(parent=parent)
        self.resize(int(width), int(height))
        self.image = QImage(int(width), int(height), QImage.Format_ARGB32)
        self.image.fill(QColor("white"))  # White background
        
        self.getClipType = getClipType
        # Padding
        self.x_padding = 20
        self.y_padding = 20
        # QImage's coordinates
        self.x_min = self.x_padding
        self.y_min = self.image.height() - self.y_padding
        self.x_max = self.image.width() - self.x_padding
        self.y_max = self.y_padding
        # View width and height
        self.view_w = self.image.width() - (2 * self.x_padding)
        self.view_h = self.image.height() - (2 * self.y_padding)
        # Window center. 
        self.center_x = self.x_padding + (self.image.width() / 2)
        self.center_y = self.y_padding + (self.image.height() / 2)
        
        # Projection data
        self.focal_angle = 20
        self.focal_distance = 100
        # Set up focal point for perspective projection
        self.viewport = Viewport(0, 0, self.view_w, self.view_h)
        cameraPosition = Point3D(self.viewport.transformations.position.x, self.viewport.transformations.position.y - (tan(rad(self.focal_angle)) * self.focal_distance), self.viewport.transformations.position.z + self.focal_distance)
        self.viewport.camera_position = cameraPosition
        
        painter = QPainter(self.image)
        self.drawBoundingRect(painter)
        painter.end()
        self.update()

        
    def addObject(self, object: GraphicObject):
        self.viewport.addObject(object)

    def removeObject(self, object: GraphicObject):
        self.viewport.removeObject(object)

    def getObjectList(self):
        return self.viewport.getObjectList()
    
    def setObjectList(self, obj_list: List[GraphicObject]):
        self.viewport.setObjectList(obj_list)
    
    def onPan(self, x: int, y: int):
        self.viewport.transformations.position.x += x
        self.viewport.transformations.position.y += y
        return
    
    def onZoom(self, value: float):
        self.viewport.transformations.scale += value
    
    # Returns boundary points clockwise
    def getBoundaries(self) -> List[Point2D]:
        """ Get points for top left and bottom right in cartesian coordiantes. """
        bounds: List[Point2D] = []
        update_x = - self.image.width() // 2 + self.x_padding
        update_y = - self.image.height() // 2 + self.y_padding
        self.center_x = update_x
        self.center_y = update_y
        top_l = Point2D(update_x, -update_y)
        bottom_r = Point2D(-update_x, update_y)
        print('Get bounds. Cartesian coordinates')
        print('x_left: ', top_l.x, ' y_left: ', top_l.y)
        print('x_right: ', bottom_r.x, ' y_right: ', bottom_r.y)
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
        
    # Transforms point from Cartesian to QImage's coordinates
    def transformToCanva(self, point: Point3D) -> Point2D:
        x_wmin, y_wmin, x_wmax, y_wmax = (self.x_min, self.y_min, self.x_max, self.y_max)
        x_vmin, y_vmin, x_vmax, y_vmax = (
            self.viewport.x_min,
            self.viewport.y_min,
            self.viewport.x_max,
            self.viewport.y_max
        )
        
        xN = (point.x - x_vmin) / (x_vmax - x_vmin)
        yN = (point.y - y_vmin) / (y_vmax - y_vmin)
        
        xW = xN * (x_wmax - x_wmin) + x_wmin
        yW = yN * (y_wmax - y_wmin) + y_wmin
        
        print('Canva::TransformToCanva input X: ', point.x, ' Y: ', point.y)
        print('Canva::TransformToCanva output X: ', xW, ' Y: ', yW)
        
        return Point2D(int(xW), int(yW))

    def drawBoundingRect(self, painter: QPainter):
        rect_x = self.image.width() - 2 * self.x_padding
        rect_y = self.image.height() - 2 * self.y_padding
        painter.drawRect(self.x_padding, self.y_padding, rect_x, rect_y) 

    def drawObjects(self):
        """ Redraw the objects after clearing or updating the canvas """
        print('Canva::drawObjects')
        self.image.fill(QColor("white"))  # Clear the image before drawing
        painter = QPainter(self.image)  # Use QPainter to draw on the QImage
        painter.setPen(QPen(QColor("black")))  # Set pen color for drawing
        # Draw clipping bounds
        self.drawBoundingRect(painter)

        for obj in self.viewport.objList:
            
            points = obj.getPoints()
            render_points: List[Point2D] = []
            clipped_points: List[Point2D] = None
            print('Draw object: ', obj.name, ' type: ', obj.type)
            # n_points = list(map(lambda p: normalizePoint(p, self.viewport), points))
            # obj.normailzedPoints = n_points
            
            t_points = []
            if (obj.type == GraphicObjectType.Object3D):
                # Use first point as reference
                # Transform points
                for edge in obj.edges:
                    p1 = edge[0]
                    p2 = edge[1]
                    n1 = normalizePoint(p1, self.viewport)
                    n2 = normalizePoint(p2, self.viewport)
                    t_points.append(n1)
                    t_points.append(n2)
                obj.normailzedPoints = t_points
            elif (obj.type == GraphicObjectType.BSpline):
                obj.setUpLines()
                for point in obj.render_points:
                    n_point = normalizePoint(point, self.viewport)
                    t_points.append(n_point)
                obj.normailzedPoints = t_points
            else:
                for point in points:
                    # n_point = transformParallelProjection(point, self.viewport.vpr, self.viewport.rot_angle, self.viewport.rot_angle, self.viewport.rot_angle)
                    n_point = normalizePoint(point, self.viewport)
                    t_points.append(n_point)
                obj.normailzedPoints = t_points
            
            clipped_points = applyClipping(obj.normailzedPoints, self.getBoundaries(), self.getClipType())
            
            if clipped_points == None:
                continue
            else:
                for point in clipped_points:
                    p = self.transformToCanva(point)
                    print('Canva coordinates. X: ', p.x, ' Y: ', p.y)
                    render_points.append(p)
            
            # print('Clipped points')
            # for f in clipped_points:
            #     print('x: ', f.x, ' y: ', f.y)
            painter.setPen(QPen(obj.color))
            if len(render_points) == 1:
                painter.drawPoint(round(render_points[0].x), render_points[0].y)

            elif len(render_points) == 2:
                print('Draw line')
                painter.drawLine(render_points[0].x, render_points[0].y, render_points[1].x, render_points[1].y)

            elif len(render_points) >= 3:
                # Primeiro ponto
                last_point = render_points[0]
                for point in render_points[1:]:
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
        self.viewport.width = new_width - (2 * self.x_padding)
        self.viewport.height = new_height - (2 * self.y_padding)
        self.viewport.updateBounds()
        # print(f"Resized: image to {new_width}x{new_height}, viewport to {self.viewport.width}x{self.viewport.height}")
        self.drawObjects()

        # Call the parent class's resize event handler (important for layout managers)
        super().resizeEvent(event)