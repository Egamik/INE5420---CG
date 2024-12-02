from enum import Enum

class ClippingLineAlgorithm(Enum):
  CohenSutherland = 'CohenSutherland'
  LiangBarsky = 'LiangBarsky'

class ClippingCurveAlgorithm(Enum):
  Bezier = 'Bezier'