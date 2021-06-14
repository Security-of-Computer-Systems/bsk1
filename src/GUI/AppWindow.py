from PyQt5.QtCore import QSize, QDir
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from math import floor

from src import sender, receiver
from src.encryption import create_RSA_keys
from src.receiver import ListenThread


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
        self.thread = ListenThread()
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
        self.choose_public_key_button.clicked.connect(lambda: self.chooseFile(self.public_key))
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
        # Ip Label
        self.sender_ip_label = QLabel(self)
        self.sender_ip_label.setText('Ip')
        self.sender_ip_label.move(self.padding, floor(self.window_height / 10 * 2) - 32)

        # Ip Line Edit
        self.sender_ip = QLineEdit("localhost", self)
        self.sender_ip.move(self.padding, floor(self.window_height / 10 * 2))
        self.sender_ip.resize(floor(self.window_width / 3), 32)

        # File label
        self.file_label = QLabel(self)
        self.file_label.setText('File')
        self.file_label.move(self.padding, floor(self.window_height / 10 * 4) - 32)

        # File Line Edit
        self.file = QLineEdit(self)
        self.file.move(self.padding, floor(self.window_height / 10 * 4))
        self.file.resize(floor(self.window_width / 3), 32)

        # Choose  file
        self.choose_file_button = QPushButton('Choose file', self)
        self.choose_file_button.clicked.connect(lambda: self.chooseFile(self.file))
        self.choose_file_button.resize(floor(self.window_width / 3), 32)
        self.choose_file_button.move(floor(self.window_width / 3) + self.padding,
                                           floor(self.window_height / 10 * 4))

        self.ecb = QRadioButton("ECB",self)
        self.ecb.move(self.padding, floor(self.window_height / 10 * 5))

        self.cbc = QRadioButton("CBC", self)
        self.cbc.move(self.padding+70, floor(self.window_height / 10 * 5))

        self.cfb = QRadioButton("CFB", self)
        self.cfb.move(self.padding+70*2, floor(self.window_height / 10 * 5))

        self.ofb = QRadioButton("OFB", self)
        self.ofb.move(self.padding + 70*3, floor(self.window_height / 10 * 5))

        # Public key label
        self.public_key_label2 = QLabel(self)
        self.public_key_label2.setText('Public Key')
        self.public_key_label2.move(self.padding, floor(self.window_height / 10 * 6) - 32)

        # Public Key Line Edit
        self.public_key2 = QLineEdit(self)
        self.public_key2.move(self.padding, floor(self.window_height / 10 * 6))
        self.public_key2.resize(floor(self.window_width / 3), 32)

        # Choose Public key file
        self.choose_public_key_button2 = QPushButton('Choose file', self)
        self.choose_public_key_button2.clicked.connect(lambda: self.chooseFile(self.public_key2))
        self.choose_public_key_button2.resize(floor(self.window_width / 3), 32)
        self.choose_public_key_button2.move(floor(self.window_width / 3) + self.padding,
                                           floor(self.window_height / 10 * 6))

        # Send button
        self.send_file = QPushButton('Send', self)
        self.send_file.clicked.connect(self.sendFile)
        self.send_file.resize(floor(self.window_width / 3), 32)
        self.send_file.move(floor(self.window_width / 3), floor(self.window_height / 10 * 8))

        # Send Label
        self.send_file_label = QLabel(self)
        self.send_file_label.setText('Ok')
        self.send_file_label.move(floor(self.window_width / 3 * 2), floor(self.window_height / 10 * 8))

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.resize(self.window_width-25*2, 20)
        self.progress_bar.move(50, floor(self.window_height / 10 * 7))


    def receiverUI(self):
        # Ip Label
        self.receiver_ip_label = QLabel(self)
        self.receiver_ip_label.setText('Ip')
        self.receiver_ip_label.move(self.padding, floor(self.window_height / 10 * 2) - 32)

        # Ip Line Edit
        self.receiver_ip = QLineEdit("localhost" ,self)
        self.receiver_ip.move(self.padding, floor(self.window_height / 10 * 2))
        self.receiver_ip.resize(floor(self.window_width / 3), 32)

        # Listen button
        self.listen_button = QPushButton('Connect', self)
        self.listen_button.clicked.connect(self.clickListenButton)
        self.listen_button.resize(floor(self.window_width / 3), 32)
        self.listen_button.move(self.padding+floor(self.window_width / 3), floor(self.window_height / 10 * 2))

        # Ok Label
        self.receiver_ok_label = QLabel(self)
        self.receiver_ok_label.setText('Ok')
        self.receiver_ok_label.move(floor(self.window_width / 3)*2 + self.padding, floor(self.window_height / 10 * 2))

        #Logs
        self.logs = QListWidget(self)
        item1 = QListWidgetItem("Logs:")
        self.logs .addItem(item1)
        scroll_bar = QScrollBar(self)
        self.logs.setGeometry(self.padding, self.padding+110, self.window_width-2*self.padding, self.window_height-2*self.padding-100)
        self.logs.setVerticalScrollBar(scroll_bar)


    def hideAll(self):
        self.keys_ok_label.hide()
        self.generate_keys_button.hide()
        self.keys_ip_label.hide()
        self.keys_ip.hide()
        self.public_key_label.hide()
        self.public_key.hide()
        self.choose_public_key_button.hide()
        self.public_key_label2.hide()
        self.public_key2.hide()
        self.choose_public_key_button2.hide()
        self.send_key_button.hide()
        self.send_key_label.hide()
        self.sender_ip.hide()
        self.sender_ip_label.hide()
        self.file_label.hide()
        self.file.hide()
        self.choose_file_button.hide()
        self.ecb.hide()
        self.cbc.hide()
        self.cfb.hide()
        self.ofb.hide()
        self.send_file.hide()
        self.progress_bar.hide()
        self.send_file_label.hide()
        self.logs.hide()
        self.receiver_ip_label.hide()
        self.receiver_ip.hide()
        self.listen_button.hide()
        self.receiver_ok_label.hide()

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
        self.sender_ip.show()
        self.sender_ip_label.show()
        self.file_label.show()
        self.file.show()
        self.choose_file_button.show()
        self.ecb.show()
        self.cbc.show()
        self.cfb.show()
        self.ofb.show()
        self.send_file.show()
        self.progress_bar.show()
        self.public_key_label2.show()
        self.public_key2.show()
        self.choose_public_key_button2.show()

    def clickReceiverButton(self):
        self.hideAll()
        self.receiver_button.setStyleSheet("background-color : #2C93C7")
        self.sender_button.setStyleSheet("background-color : #21B0F7")
        self.keys_button.setStyleSheet("background-color : #21B0F7")
        self.logs.show()
        self.receiver_ip_label.show()
        self.receiver_ip.show()
        self.listen_button.show()

    def chooseFile(self, line_edit):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)

        if dialog.exec_():
            line_edit.setText(dialog.selectedFiles()[0])

    def clickGenerateKeysButton(self):
        create_RSA_keys()
        print("Wygenerowałem klucz publiczny i prywatny")
        self.keys_ok_label.show()

    def sendKey(self):
        sender.send_key(self.keys_ip.text(), self.public_key.text())
        self.send_key_label.show()
        print("wysłałem")

    def sendFile(self):

        if self.ofb.isChecked():
            mode = "ofb"
        elif self.cbc.isChecked():
            mode = "cbc"
        elif self.cfb.isChecked():
            mode = "cfb"
        else:
            mode = "ecb"

        sender.send_file(self.sender_ip.text(), self.file.text(), mode, self.progress_bar, self.public_key2.text())
        self.send_file_label.show()
        print("wysłałem")

    def clickListenButton(self):
        self.thread.setArguments(self.logs, self.receiver_ip.text())
        self.thread.start()

        self.receiver_ok_label.show()