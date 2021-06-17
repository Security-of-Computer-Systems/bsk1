import socket
from shutil import copyfile
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QListWidgetItem

from src.encryption import decrypt_session_key, decrypt


class ListenThread(QThread):

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.buffer_size = 1024

    def setArguments(self, logs, ip, private_key_path, password):
        self.logs = logs
        self.ip = ip
        self.private_key_path = private_key_path
        self.private_key_password = password
    def run(self):
        TCP_PORT = 8086

        # Create a TCP/IP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        s.bind((self.ip, TCP_PORT))
        s.listen(1)

        while 1:

            conn, addr = s.accept()

            print(str(addr[0]) + " started sending file")
            item = QListWidgetItem(str(addr[0]) + " started sending file")
            self.logs.addItem(item)

            header = conn.recv(self.buffer_size)

            message_type = str(header).split("||")[1]

            if message_type == "file":
                file_name = str(header).split("||")[2]
                mode = str(header).split("||")[3]
                self.encrypted_session_key = header.split(b'||')[4]
                iv = header.split(b'||')[5]
                self.file_begin = header.split(b'||')[6]

                self.download_file(conn, file_name, mode, iv)

                print(str(addr[0]) + " sent file: " + file_name)
                item = QListWidgetItem(str(addr[0]) + " sent file: " + file_name)
                self.logs.addItem(item)

            elif message_type == "key":
                self.download_key(addr, conn)

                print(str(addr) + "send key")
                item = QListWidgetItem(str(addr[0]) + " sent key")
                self.logs.addItem(item)



    def download_file(self, conn, file_name, mode, iv):

        #session_key = conn.recv(self.buffer_size) ##################################
        with open("encrypted_files/"+file_name, "wb") as f:
            f.write(self.file_begin)
            while 1:

                bytes_read = conn.recv(self.buffer_size)

                if not bytes_read: break

                f.write(bytes_read)

                # conn.send(bytes("wiadomosc dostarczona","utf-8") ) # echo
            conn.close()

        # decrypt data
        try:
            with open("decrypted_files/" + file_name, "wb") as f:
                f.write(decrypt("encrypted_files/" + file_name, mode, self.private_key_path, self.private_key_password,
                                self.encrypted_session_key, iv))
        except:

            copyfile("encrypted_files/" + file_name, "decrypted_files/" + file_name)



    def download_key(self, addr, conn):
        with open("other_keys/"+str(addr[0]) + ".pub", "wb") as f:
            while 1:

                bytes_read = conn.recv(self.buffer_size)
                if not bytes_read: break

                f.write(bytes_read)
            conn.close()
