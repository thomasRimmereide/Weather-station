import pickle
from socket import AF_INET, SOCK_DGRAM, socket

host = "localhost"
port = 6969

ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_client(connection):

    while True:
        data, addr = ServerSock.recvfrom(2048)
        received_data = pickle.loads(data)
