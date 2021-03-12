import socket
from pathlib import Path


def send_file(ip, file_path, mode, progress_bar):
    port = 10000
    buffer_size = 512
    file_name = file_path.split("/")[-1]
    file_size = Path(file_path).stat().st_size # w bajtach przed szyfrowaniem
    sended_bytes = 0

    if mode == "ecb":
        print("ecb()")
    elif mode == "cbc":
        print("cbc()")
    elif mode == "cfb":
        print("cfb()")
    elif mode == "ofb":
        print("ofb()")

    # Plik znajduje się teraz w folderze tmp
    # plik ma nowy rozmiar
    # file_size = Path("tmp/" + file_name).stat().st_size ################################

    message = "|file|" + file_name + "|" + mode

    #session_key = create_session_key()#########################################

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # send header
    s.send(bytes(message, "utf-8"))

    # send session key
    # s.send(session_key)##############################################################

    # start sending the file
    # file_path -> tmp/file_name ############################################################
    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(buffer_size)
            sended_bytes += len(bytes_read)

            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)

            # update the progress bar
            progress_bar.setValue(sended_bytes/file_size*100)
            print(sended_bytes/file_size*100)

    s.close()

    # data = s.recv(BUFFER_SIZE)



def send_key(ip, file_path):
    port = 10000
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


