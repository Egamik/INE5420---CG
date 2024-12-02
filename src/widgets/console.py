from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPainter, QFontMetrics
from stream import EmittingStream
import sys


class ConsoleWidget(QVBoxLayout):
  def __init__(self):
    super(ConsoleWidget, self).__init__(None)
    sys.stdout = EmittingStream(textWritten=self.updateText)
    
    self.label = QLabel()
    self.label.setAutoFillBackground(True)
    self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
    self.label.setStyleSheet("background-color: #202020; padding-left: 10px; padding-right: 10px; bottom: 0px")
    self.label.setWordWrap(True)

    self.scroll = QScrollArea()
    self.scroll.setWidgetResizable(True)
    self.scroll.setWidget(self.label)
    self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.verticalScroll = self.scroll.verticalScrollBar()
    
    self.addWidget(self.scroll)

  def updateText(self, text):
    self.label.setText(self.label.text() + text)
    self.verticalScroll.setValue(self.verticalScroll.maximum())
    