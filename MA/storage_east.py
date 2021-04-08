import pickle
from socket import AF_INET, SOCK_DGRAM, socket
from _thread import start_new_thread
from time import sleep
import DBMS as db


host = "localhost"
port = 1337

ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_server(connected_client):
    received_data = pickle.loads(connected_client)
    db.put(received_data, "Oslo_WS")
    print(received_data)


while True:
    data, addr = ServerSock.recvfrom(2048)
    start_new_thread(threaded_server, (data,))

ServerSock.close()
socket.shutdown(ServerSock)
