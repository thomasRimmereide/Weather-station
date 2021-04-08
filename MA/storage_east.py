import pickle
from socket import AF_INET, SOCK_DGRAM, socket
from _thread import start_new_thread

host = "localhost"
port = 6969

ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_server(connection):
    try:
        while True:
            data, addr = connection.recvfrom(2048)
            received_data = pickle.loads(data)
            print(received_data)
    except KeyboardInterrupt:
        print("Storage region East is stopped!")


threaded_server(ServerSock)
