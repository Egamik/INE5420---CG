from PyQt5.QtWidgets import QApplication
import sys
from core.main_window import MainWindow

def main():
  app = QApplication(sys.argv)
  win = MainWindow()
  win.show()
  sys.exit(app.exec_())

main()
