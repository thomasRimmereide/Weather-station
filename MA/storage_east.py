import pickle
from socket import AF_INET, SOCK_DGRAM, socket
from _thread import start_new_thread
import DBMS as db


host = "localhost"
port = 1337

ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_server(connected_client):
    print(connected_client)
    received = pickle.loads(connected_client)
    print(type(received))
    if isinstance(received, dict):
        db.put(received, "Oslo_WS")
    elif isinstance(received, list):
        print("inni liste")
        ser = "Connected to storage east"
        ServerSock.sendto(str.encode(ser), ("localhost", 5555))
        print("sendt respons")
    else:
        print("error, do not recognize type")



while True:
    print("vildesintisstass")
    data, addr = ServerSock.recvfrom(2048)
    start_new_thread(threaded_server, (data,))
    print("erlendsintisstass")

ServerSock.close()
socket.shutdown(ServerSock)
