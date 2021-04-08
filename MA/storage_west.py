# storage server process

"""
Denne skal lese inn fra weather_station_bergen.py, og lagre dataen i csv-filen.
Den skal også gi FMI tilgang til dataen som er lagret hvis den får en forespørsel om det.

Står også at alle filene skal kunne kjøres i localhost, litt usikker på hva det menes med, men kanskje bare på pcen?

Første omgang:

Kunne lagre data fra en dictonary (feltnavn står i station.py) til en CSV fil.

"""

import pickle

import pandas as pd
from pandas.errors import EmptyDataError
import socket
import os
import DBMS
from _thread import start_new_thread

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
tcp_port = 6969
sock_tcp.bind((host, tcp_port))

print('Server is running')
sock_tcp.listen(5000)


def get_request(com_request: list):
    entire_database = pd.read_csv("Data.csv")
    if 'all' in com_request:
        return entire_database
    else:
        return DBMS.get_period(com_request[-2], com_request[-1], entire_database)


def thread(connection):
    connection.send(str.encode('Connected to Database Bergen'))
    data = connection.recv(2048)
    connected_client = data.decode()

    while True:
        if connected_client == 'Bergen WS':
            data = connection.recv(2048)
            print(pickle.loads(data))
            DBMS.put(pickle.loads(data))

        elif connected_client == 'request_computer':
            data = connection.recv(2048)
            req = pickle.loads(data)
            if req[0] != 's':
                print("!=s")
                resp = get_request(req)
                connection.sendall(pickle.dumps(resp))
        if req[0] == 's':
            break
    print("shutdown")
    connection.close()


while True:
    tcp_client, tcp_address = sock_tcp.accept()
    print('Connected to: ' + tcp_address[0] + ':' + str(tcp_address[1]))
    start_new_thread(thread, (tcp_client,))
sock_tcp.close()
socket.socket.shutdown(sock_tcp)