import os
from PyQt5.QtGui import QColor
from base.bezier import BezierCurve
from base.graphic_obj import GraphicObjectType, Line, Point, Polygon
from utils import formatObject

class ObjWavefront:
  def __init__( self ):
    self.mtllibs   = []                
    self.mtls      = False    
    self.vertices  = []                  
    self.window    = []                 
    self.objectsName = []
    self.objectsType = []              
    self.usemtl = []
    self.newMtl = []
    self.kdParams = []
    self.objects = {}
    self.filled = []
    self.faces = []
    
  def getVerticesList(self, objectList):
    verticesList = []
    for obj in objectList:
      for vertice in obj.points:
        if vertice not in verticesList:
          verticesList.append([vertice.x, vertice.y, vertice.z])
    return verticesList

  def mapVerticesToObject(self, objectList, verticesList):
    return map(lambda object : {object : self.getAllVerticesIndexesInObject(object, verticesList)}, objectList)

  def getAllVerticesIndexesInObject(self, object, verticesList):
    return list(map(lambda objVertice : verticesList.index(objVertice) + 1 if objVertice in verticesList else -1, object.points))

  def mapVerticesToWindow(self, windowVertices, verticesList):
    return list(map(lambda vertice: self.getVerticeIndex(vertice, verticesList), windowVertices))

  def getVerticeIndex(self, vertice, verticesList):
    for v in verticesList:
      if vertice == v:
        return verticesList.index(v) + 1  

def loadFromObj(objFilePath, mtlFilePath):
  objects = []
  with open(objFilePath, 'r' ) as objf:
    wavefrontObj = ObjWavefront()
    for line in objf:
      splittedLine = line.split()

      if not splittedLine:
        continue

      # Handle MTL lib
      if splittedLine[0] == 'mtllib':
        wavefrontObj.mtls = True
        parseMtl(wavefrontObj, mtlFilePath)

      if splittedLine[0] == 'v':
        t = []
        for v in splittedLine[1:]:
          if '-' in v:
            t.append(float(v.replace('\U00002013', '-')))
          else:
            t.append(float(v))
        wavefrontObj.vertices.append(t)

      elif splittedLine[0] == 'w':
        indices = [float(v)-1 for v in splittedLine[1:]]
        nameType = 'window'
        wavefrontObj.objectsType.append(nameType)
        for i in indices:
          wavefrontObj.window.append( wavefrontObj.vertices[int(i)] )
          

      elif splittedLine[0] == 'o':
        wavefrontObj.objectsName.append( splittedLine[1] )
                

      elif splittedLine[0] == 'p':
        nameType =GraphicObjectType.Point
        wavefrontObj.objectsType.append(nameType)
        wavefrontObj.objects[wavefrontObj.objectsName[-1]] = [wavefrontObj.vertices[int(splittedLine[1]) -1]]
        wavefrontObj.filled.append(False)                

      elif splittedLine[0] == 'l':
        indices = [float(v)-1 for v in splittedLine[1:]]
        temp = []
        for i in indices:
          temp.append(wavefrontObj.vertices[int(i)]) 
        nameType = GraphicObjectType.Line  
        if(len(temp) > 2):                            
          nameType = GraphicObjectType.Polygon
        wavefrontObj.objectsType.append(nameType)
        wavefrontObj.objects[wavefrontObj.objectsName[-1]] = temp
        wavefrontObj.filled.append(False)             
      elif splittedLine[0] == 'f':
        indices = [ float(v)-1 for v in splittedLine[1:]]
        temp = []
        for i in indices:
          temp.append(wavefrontObj.vertices[int(i)])    
        nameType = GraphicObjectType.Polygon
        wavefrontObj.objectsType.append(nameType)
        wavefrontObj.faces.append(temp)
        wavefrontObj.objects[wavefrontObj.objectsName[-1]] = temp
        wavefrontObj.filled.append(False)  
      elif splittedLine[0] == 'curv':
        indices = [float(v)-1 for v in splittedLine[1:]]
        temp = []
        for i in indices:
          temp.append(wavefrontObj.vertices[int(i)])
        nameType = GraphicObjectType.BSpline
        wavefrontObj.objectsType.append(nameType)
        wavefrontObj.objects[wavefrontObj.objectsName[-1]] = temp
        wavefrontObj.filled.append(False)
      elif splittedLine[0] == 'usemtl':
        wavefrontObj.usemtl.append(splittedLine[1])

    objIndex = 0
    for obj in wavefrontObj.objects:
      color = QColor('black')
      if (objIndex < len(wavefrontObj.usemtl)):
        material = wavefrontObj.usemtl[objIndex]
        materialIndex = wavefrontObj.newMtl.index(material)
        rgb = wavefrontObj.kdParams[materialIndex]
        color.setRgb(int(float(rgb[0])*255), int(float(rgb[1])*255), int(float(rgb[2])*255))  
      objects.append(formatObject(obj, wavefrontObj.objectsType[objIndex+1], wavefrontObj.objects[obj], color))
      objIndex += 1


  
  return (objects,  wavefrontObj.window)

def saveToObj(objects, filePath, filename, window_vertices):
  wavefrontObj = ObjWavefront()
  verticesList = wavefrontObj.getVerticesList(objects)
  objects_colors = []
  objectsByVerticesLineNumbers = wavefrontObj.mapVerticesToObject(objects, verticesList)
  with open(filePath, 'w') as file:
    # append window vertices
    for v in window_vertices:
      if v not in verticesList:
        verticesList.append(v)   
    # Write vertices
    for vertice in verticesList:
      file.write('v ' + ' '.join([str(elem) for elem in vertice]) + '\n')

    # Write mtlib
    file.write('mtllib ' + filename + '.mtl' + '\n')

    #Write window
    file.write('o window' + '\n')
    file.write('w ' + ''.join([str(index)  + ' ' for index in wavefrontObj.mapVerticesToWindow(window_vertices, verticesList)]) + '\n' )
    # Write objects
    for object in list(objectsByVerticesLineNumbers):
      file.write('o ' + next(iter(object)).name + '\n')
      objects_colors.append(next(iter(object)).color)
      file.write('usemtl ' + next(iter(object)).color.name() + '\n')
      if (isinstance(next(iter(object)) , Point)):
        file.write('p ' + ' '.join([str(elem) for elem in object.get(next(iter(object)))]) + '\n')
      if (isinstance(next(iter(object)) , Line)):
        file.write('l ' + ' '.join([str(elem) for elem in object.get(next(iter(object)))]) + '\n')
      if (isinstance(next(iter(object)) , Polygon)):
        file.write('f ' + ' '.join([str(elem) for elem in object.get(next(iter(object)))]) + '\n')
      if (isinstance(next(iter(object)) , BezierCurve)):
        file.write('curv ' + ' '.join([str(elem) for elem in object.get(next(iter(object)))]) + '\n')  
    #   if (isinstance(next(iter(object)) , BSpline)):
    #     file.write('curv ' + ' '.join([str(elem) for elem in object.get(next(iter(object)))]) + '\n')   

    saveMtl(objects_colors, filePath, filename)  



def parseMtl(wavefrontObj, fileNameMtl ):
    if not os.path.exists(fileNameMtl):
      wavefrontObj.mtls = False 
      return
    with open(fileNameMtl, 'r') as objm:
      for line in objm:
        splittedLine = line.split()
        if not splittedLine:
          continue
        if splittedLine[0] == 'newmtl':
          wavefrontObj.newMtl.append(splittedLine[1])
        elif splittedLine[0] == 'Kd':
          wavefrontObj.kdParams.append(splittedLine[1:])       

def saveMtl(color_list, filepath, filename):
  with open(filepath.split('.obj')[0] + '.mtl', 'w' ) as file:               
    for c in color_list:
        file.write(f'newmtl {c.name()}\n')
        color = c.getRgb()
        file.write('Kd '+' '.join('{:0.6f}'.format(clr/255) for clr in color)+'\n')       
