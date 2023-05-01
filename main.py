from PySide6.QtWidgets import QApplication
from app import MainWindow
import sys

app = QApplication(sys.argv)

window = MainWindow(app)
window.setMinimumSize(400, 300)
window.setWindowTitle('Every Good Endeavor')

window.show()

app.exec()
