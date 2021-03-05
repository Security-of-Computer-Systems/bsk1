from PyQt5.QtCore import QSize, QDir
from PyQt5.QtWidgets import *
from math import floor


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.window_width = 600
        self.window_height = 400
        self.padding = 30
        self.mainUI()
        self.keysUI()
        self.senderUI()
        self.receiverUI()
        self.show()
        self.clickKeysButton()

    def mainUI(self):
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowTitle("BSK")

        self.keys_button = QPushButton('Keys', self)
        self.keys_button.clicked.connect(self.clickKeysButton)
        self.keys_button.resize(floor(self.window_width / 3), 32)
        self.keys_button.move(0, 0)
        self.keys_button.setStyleSheet("background-color : #21B0F7")

        self.sender_button = QPushButton('Sender', self)
        self.sender_button.clicked.connect(self.clickSenderButton)
        self.sender_button.resize(floor(self.window_width / 3), 32)
        self.sender_button.move(floor(self.window_width / 3), 0)
        self.sender_button.setStyleSheet("background-color : #21B0F7")

        self.receiver_button = QPushButton('Receiver', self)
        self.receiver_button.clicked.connect(self.clickReceiverButton)
        self.receiver_button.resize(floor(self.window_width / 3), 32)
        self.receiver_button.move(floor(self.window_width / 3 * 2), 0)
        self.receiver_button.setStyleSheet("background-color : #21B0F7")

        self.show()

    def keysUI(self):

        # Ok Label
        self.keys_ok_label = QLabel(self)
        self.keys_ok_label.setText('Ok')
        self.keys_ok_label.move(floor(self.window_width / 3)+self.padding, floor(self.window_height / 10 * 2))

        # Generate keys button
        self.generate_keys_button = QPushButton('Generate Keys', self)
        self.generate_keys_button.clicked.connect(self.clickGenerateKeysButton)
        self.generate_keys_button.resize(floor(self.window_width / 3), 32)
        self.generate_keys_button.move(self.padding, floor(self.window_height / 10 * 2))

        # Ip Label
        self.keys_ip_label = QLabel(self)
        self.keys_ip_label.setText('Ip')
        self.keys_ip_label.move(self.padding, floor(self.window_height / 10 * 4)-32)

        # Ip Line Edit
        self.keys_ip = QLineEdit(self)
        self.keys_ip.move(self.padding, floor(self.window_height / 10 * 4))
        self.keys_ip.resize(floor(self.window_width / 3), 32)

        # Public key label
        self.public_key_label = QLabel(self)
        self.public_key_label.setText('Public Key')
        self.public_key_label.move(self.padding, floor(self.window_height / 10 * 6)-32)

        # Public Key Line Edit
        self.public_key = QLineEdit(self)
        self.public_key.move(self.padding, floor(self.window_height / 10 * 6))
        self.public_key.resize(floor(self.window_width / 3), 32)

        # Choose Public key file
        self.choose_public_key_button = QPushButton('Choose file', self)
        self.choose_public_key_button.clicked.connect(self.choosePublicKey)
        self.choose_public_key_button.resize(floor(self.window_width / 3), 32)
        self.choose_public_key_button.move(floor(self.window_width / 3)+self.padding, floor(self.window_height / 10 * 6))

        # Send button
        self.send_key_button = QPushButton('Send', self)
        self.send_key_button.clicked.connect(self.sendKey)
        self.send_key_button.resize(floor(self.window_width / 3), 32)
        self.send_key_button.move(floor(self.window_width / 3), floor(self.window_height / 10 * 8))

        # Send Label
        self.send_key_label = QLabel(self)
        self.send_key_label.setText('Ok')
        self.send_key_label.move(floor(self.window_width / 3*2), floor(self.window_height / 10 * 8))

    def senderUI(self):
        self.sender_label = QLabel(self)
        self.sender_label.setText('Sender')
        self.sender_label.move(80, 100)
        self.sender_label.resize(700, 32)

    def receiverUI(self):
        self.receiver_label = QLabel(self)
        self.receiver_label.setText('Receiver')
        self.receiver_label.move(80, 100)
        self.receiver_label.resize(700, 32)

    def hideAll(self):
        self.keys_ok_label.hide()
        self.sender_label.hide()
        self.receiver_label.hide()
        self.generate_keys_button.hide()
        self.keys_ip_label.hide()
        self.keys_ip.hide()
        self.public_key_label.hide()
        self.public_key.hide()
        self.choose_public_key_button.hide()
        self.send_key_button.hide()
        self.send_key_label.hide()

    def clickKeysButton(self):
        self.hideAll()
        self.keys_button.setStyleSheet("background-color : #2C93C7")
        self.sender_button.setStyleSheet("background-color : #21B0F7")
        self.receiver_button.setStyleSheet("background-color : #21B0F7")
        self.generate_keys_button.show()
        self.keys_ip_label.show()
        self.keys_ip.show()
        self.public_key_label.show()
        self.public_key.show()
        self.choose_public_key_button.show()
        self.send_key_button.show()


    def clickSenderButton(self):
        self.hideAll()
        self.sender_button.setStyleSheet("background-color : #2C93C7")
        self.keys_button.setStyleSheet("background-color : #21B0F7")
        self.receiver_button.setStyleSheet("background-color : #21B0F7")
        self.sender_label.show()

    def clickReceiverButton(self):
        self.hideAll()
        self.receiver_button.setStyleSheet("background-color : #2C93C7")
        self.sender_button.setStyleSheet("background-color : #21B0F7")
        self.keys_button.setStyleSheet("background-color : #21B0F7")
        self.receiver_label.show()

    def clickGenerateKeysButton(self):
        ##########################
        # wygeneruj_klucze()
        ##########################
        print("wygenerowałem")
        self.keys_ok_label.show()

    def choosePublicKey(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        public_key_path = " "
        if dialog.exec_():
            public_key_path = dialog.selectedFiles()[0]
        self.public_key.setText(public_key_path)

    def sendKey(self):
        ##########################
        # wyślij_klucz()
        ##########################
        self.send_key_label.show()
        print("wysłałem")
