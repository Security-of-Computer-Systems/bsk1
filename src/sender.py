import socket


def send_message():

    TCP_IP = '192.168.56.1'
    TCP_PORT = 23
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World!"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(bytes(MESSAGE,"utf-8"))
    data = s.recv(BUFFER_SIZE)
    s.close()
    print("c" + str(data))