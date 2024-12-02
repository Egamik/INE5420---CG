from PyQt5.QtWidgets import QHBoxLayout, QRadioButton

from enumerators.axis_type import Axis

class   AxisWidget(QHBoxLayout):

    def __init__(self, onChange: ()):
        super(AxisWidget, self).__init__(None)
        
        self.setContentsMargins(0, 0, 0, 15)
       
        axisXRadio = QRadioButton('Axis X')
        axisYRadio = QRadioButton('Axis Y')
        axisZRadio = QRadioButton('Axis Z')

        axisXRadio.clicked.connect(lambda: onChange(Axis.X) )
        axisYRadio.clicked.connect(lambda: onChange(Axis.Y) )
        axisZRadio.clicked.connect(lambda: onChange(Axis.Z) )

        self.addWidget(axisXRadio)
        self.addWidget(axisYRadio)
        self.addWidget(axisZRadio)