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