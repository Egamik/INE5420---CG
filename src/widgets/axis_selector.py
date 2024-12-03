from PyQt5.QtWidgets import QHBoxLayout, QRadioButton

from enumerators.axis_type import Axis

class   AxisWidget(QHBoxLayout):

    def __init__(self, onChange):
        super(AxisWidget, self).__init__(None)
        
        self.setContentsMargins(0, 0, 0, 15)
       
        axis_x_radio = QRadioButton('Axis X')
        axis_y_radio = QRadioButton('Axis Y')
        axis_z_radio = QRadioButton('Axis Z')

        axis_x_radio.clicked.connect(lambda: onChange(Axis.X) )
        axis_y_radio.clicked.connect(lambda: onChange(Axis.Y) )
        axis_z_radio.clicked.connect(lambda: onChange(Axis.Z) )

        self.addWidget(axis_x_radio)
        self.addWidget(axis_y_radio)
        self.addWidget(axis_z_radio)