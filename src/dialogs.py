from PyQt5.QtWidgets import QDialog, QFormLayout, QComboBox, QDialogButtonBox
 
class AddObjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new object")
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout(self)
        self.object_type = QComboBox(self)
        self.object_type.addItems(["Point", "Line", "Polygon"])
        layout.addRow("Object Type:", self.object_type)

        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

    def get_selected_object_type(self):
        return self.object_type.currentText()