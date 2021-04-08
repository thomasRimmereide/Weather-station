import pickle
from socket import AF_INET, SOCK_DGRAM, socket
from _thread import start_new_thread
import DBMS as db


host = "localhost"
port = 6969

ServerSock = socket(AF_INET, SOCK_DGRAM)
ServerSock.bind((host, port))


def threaded_server(connected_client):
    ServerSock.sendall(str.encode('Connected to Database East'), (host, port))
    print(connected_client)
    try:
        while True:
            if connected_client == 'Oslo WS':
                data_t, addr_t = ServerSock.recvfrom(2048)
                received_data = pickle.loads(data_t)
                print(received_data)
            elif connected_client == "request_computer":
                data_t = ServerSock.recvfrom(2048)
                req = pickle.loads(data_t)
                if req[0] != "s":
                    print("!=s")
                    resp = db.get_request(req)
                    ServerSock.sendall(pickle.dumps(resp))
    except KeyboardInterrupt:
        print("Storage region East is stopped!")


while True:
    data, addr = ServerSock.recvfrom(2048)
    start_new_thread(threaded_server, (addr,))

ServerSock.close()
socket.shutdown(ServerSock)
