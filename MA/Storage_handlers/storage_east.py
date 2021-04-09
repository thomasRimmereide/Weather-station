import pickle
from socket import AF_INET, SOCK_DGRAM, socket
from _thread import start_new_thread
import MA.Help_functions.DBMS as db


host = "localhost"
port = 1337
ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_server(connected_client):
    received = pickle.loads(connected_client)
    if isinstance(received, dict):
        db.put(received, "Oslo_WS")
    elif isinstance(received, list):
        response = db.get_request(received)
        ServerSock.sendto(pickle.dumps(response), ("localhost", 5555))
    else:
        print("error, do not recognize type")


print("Storage east server has started")

while True:
    try:
        data, addr = ServerSock.recvfrom(2048)
        start_new_thread(threaded_server, (data,))
    except KeyboardInterrupt:
        print("Storage east has stopped")
ServerSock.close()
socket.shutdown(ServerSock)
