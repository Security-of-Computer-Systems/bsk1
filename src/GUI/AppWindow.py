import sys
from PyQt5 import *
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from math import floor


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.window_width = 500
        self.window_height = 400
        self.mainUI()
        self.keysUI()
        self.senderUI()
        self.recipientUI()
        self.show()
        self.clickKeysButton()

    def mainUI(self):
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowTitle("BSK")

        keys_button = QPushButton('Klucze', self)
        keys_button.clicked.connect(self.clickKeysButton)
        keys_button.resize(floor(self.window_width / 3), 32)
        keys_button.move(0, 0)

        sender_button = QPushButton('Nadawca', self)
        sender_button.clicked.connect(self.clickSenderButton)
        sender_button.resize(floor(self.window_width / 3), 32)
        sender_button.move(floor(self.window_width / 3), 0)

        recipient_button = QPushButton('Odbiorca', self)
        recipient_button.clicked.connect(self.clickRecipientButton)
        recipient_button.resize(floor(self.window_width / 3), 32)
        recipient_button.move(floor(self.window_width / 3 * 2), 0)

        self.show()

    def keysUI(self):
        self.keysLabel = QLabel(self)
        self.keysLabel.setText('Keys')
        self.keysLabel.move(80, 100)
        self.keysLabel.resize(700, 32)

    def senderUI(self):
        self.senderLabel = QLabel(self)
        self.senderLabel.setText('Sender')
        self.senderLabel.move(80, 100)
        self.senderLabel.resize(700, 32)

    def recipientUI(self):
        self.recipientLabel = QLabel(self)
        self.recipientLabel.setText('Recipent')
        self.recipientLabel.move(80, 100)
        self.recipientLabel.resize(700, 32)

    def hideAll(self):
        self.keysLabel.hide()
        self.senderLabel.hide()
        self.recipientLabel.hide()

    def clickKeysButton(self):
        self.hideAll()
        self.keysLabel.show()

    def clickSenderButton(self):
        self.hideAll()
        self.senderLabel.show()

    def clickRecipientButton(self):
        self.hideAll()
        self.recipientLabel.show()