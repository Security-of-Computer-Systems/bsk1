from PyQt5.QtWidgets import QApplication
import sys
import threading

from src import receiver
from src.GUI.AppWindow import AppWindow

def main():
    threading.Thread(target=receiver.listen).start()
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()