from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QApplication, QMessageBox
)
from typing import List
from graphic_obj import GraphicObject

class ObjectTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Store objects in a list
        self.objects: List[GraphicObject] = []
        
        # Create the QTableWidget
        self.table = QTableWidget()
        self.table.setRowCount(len(self.objects))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Name', 'Color'])
        self.populateTable()
        
    def populateTable(self):
        """Populate the table with the current object data."""
        self.table.setRowCount(len(self.objects))  # Update row count
        for row, obj in enumerate(self.objects):
            self.table.setItem(row, 0, QTableWidgetItem(str(obj.name)))
            self.table.setItem(row, 1, QTableWidgetItem(str(obj.color)))
    
    def addObject(self, object: GraphicObject):
        """Add a new object to the table."""
        self.objects.append(object)
        self.populateTable()

    def removeObject(self, id):
        """Remove the selected object from the table."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.row
            # Remove the object from the list
            for i in range(len(self.objects)):
                if self.objects[i].name == id:
                    self.objects.pop(i)
            # Refresh the table
            self.populateTable()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a row to remove.")

# Example usage:
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Example objects to display in the table
    objects = [
        {'id': 1, 'name': 'Object 1', 'value': 100},
        {'id': 2, 'name': 'Object 2', 'value': 200},
        {'id': 3, 'name': 'Object 3', 'value': 300}
    ]
    
    # Create the widget
    table_widget = ObjectTableWidget(objects)
    table_widget.setWindowTitle("Objects Table with Add/Remove")
    table_widget.show()

    sys.exit(app.exec_())