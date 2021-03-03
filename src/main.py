from PyQt5.QtWidgets import QApplication
import sys

from src.GUI.AppWindow import AppWindow

app = QApplication(sys.argv)
window = AppWindow()
window.show()
app.exec_()