import socket

from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QListWidgetItem


class ListenThread(QThread):

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.buffer_size = 1024

    def setArguments(self, logs, ip):
        self.logs = logs
        self.ip = ip

    def run(self):
        TCP_PORT = 10000

        # Create a TCP/IP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        s.bind((self.ip, TCP_PORT))
        s.listen(1)

        while 1:

            conn, addr = s.accept()

            print('Connection address:', addr)
            item = QListWidgetItem('Connection address:' + str(addr))
            self.logs.addItem(item)

            header = conn.recv(self.buffer_size)

            message_type = str(header).split("|")[1]

            if message_type == "file":
                file_name = str(header).split("|")[2]
                mode = str(header).split("|")[3]

                self.download_file(conn, file_name, mode)

                print(str(addr) + "send file: " + file_name)
                item = QListWidgetItem(str(addr) + "send file: " + file_name)
                self.logs.addItem(item)
            elif message_type == "key":
                self.download_key(addr, conn)
                print(str(addr) + "send key")
                item = QListWidgetItem(str(addr) + "send key")
                self.logs.addItem(item)



    def download_file(self, conn, file_name, mode):

        #session_key = conn.recv(self.buffer_size) ##################################
        with open("Files/"+file_name, "wb") as f:
            while 1:

                bytes_read = conn.recv(self.buffer_size)

                if not bytes_read: break

                f.write(bytes_read)

                # conn.send(bytes("wiadomosc dostarczona","utf-8") ) # echo
            conn.close()

        # rozszyfruj_plik(file_name, mode, session_key) #############################################################################

    def download_key(self, addr, conn):
        with open("Keys/"+str(addr) + ".pub", "wb") as f:
            while 1:

                bytes_read = conn.recv(self.buffer_size)

                if not bytes_read: break

                f.write(bytes_read)
            conn.close()
