import socket
import sys
from pathlib import Path

from src.encryption import *


def send_file(ip, file_path, mode, progress_bar, public_key_path):
    port = 8081
    buffer_size = 512
    file_name = file_path.split("/")[-1]
    bytes_sent = 0

    # encryption
    ct, session_key, iv = encrypt(file_path, mode)

    file_size = sys.getsizeof(ct)
    encrypted_session_key = encrypt_session_key(session_key, public_key_path)
    # save bytes to file
    with open("tmp/" + file_name, "wb") as f:
        f.write(ct)


    # message header
    message = bytes("||file||", "utf-8") + bytes(file_name, "utf-8") + bytes("||", "utf-8") + bytes(mode, "utf-8") + bytes("||", "utf-8") + encrypted_session_key + bytes("||", "utf-8") + iv

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # send header
    s.send(message)

    # start sending the file
    with open("tmp/" + file_name, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(buffer_size)

            bytes_sent += len(bytes_read)

            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)

            # update the progress bar
            progress_bar.setValue(bytes_sent/file_size*100)

    s.close()

    # data = s.recv(BUFFER_SIZE)



def send_key(ip, file_path):
    port = 8081
    buffer_size = 512
    file_name = file_path.split("/")[-1]

    message = "|key|"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # send header
    s.send(bytes(message, "utf-8"))


    # start sending the file
    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(buffer_size)

            if not bytes_read: break
            s.sendall(bytes_read)

            # update the progress bar

    s.close()

