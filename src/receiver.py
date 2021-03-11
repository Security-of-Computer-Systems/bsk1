from time import sleep

import socket


def listen():

    TCP_IP = '192.168.56.1'
    TCP_PORT = 23

    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    BUFFER_SIZE = 20

    conn, addr = s.accept()
    print('s: Connection address:', addr)

    while 1:

        data = conn.recv(BUFFER_SIZE)

        if not data: break

        print("s: received data:", data)
        conn.send(bytes("wiadomosc dostarczona","utf-8") ) # echo
    conn.close()