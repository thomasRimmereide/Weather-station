# storage server process

"""
Denne skal lese inn fra weather_station_bergen.py, og lagre dataen i csv-filen.
Den skal også gi FMI tilgang til dataen som er lagret hvis den får en forespørsel om det.

Står også at alle filene skal kunne kjøres i localhost, litt usikker på hva det menes med, men kanskje bare på pcen?

Første omgang:

Kunne lagre data fra en dictonary (feltnavn står i station.py) til en CSV fil.

"""

import pickle

import socket
from MA.Help_functions import DBMS
from _thread import start_new_thread

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
tcp_port = 6969
sock_tcp.bind((host, tcp_port))

print('Storage west server has started')
sock_tcp.listen(5000)


def thread(this_connection):
    """This method decides whats to bee done in a thread
    if its a weather station it receive the data and adds it to the database.
    if its a user client it handle client requests and send a response packet"""
    start_package = this_connection.recv(2048)
    type_of_client = pickle.loads(start_package)
    try:
        while True:
            if type_of_client == 'Bergen_WS':
                received_package = this_connection.recv(2048)
                DBMS.put(pickle.loads(received_package), type_of_client)
            elif type_of_client == "Stavanger_WS":
                received_package = this_connection.recv(2048)
                DBMS.put(pickle.loads(received_package), type_of_client)
            else:
                received_package = this_connection.recv(2048)
                request = pickle.loads(received_package)
                response = DBMS.get_request(request)
                this_connection.sendall(pickle.dumps(response))
    except KeyboardInterrupt:
        print("Storage west has stopped")
    print("shutdown")
    this_connection.close()


while True:
    tcp_client, tcp_address = sock_tcp.accept()
    print('Connected to: ' + tcp_address[0] + ':' + str(tcp_address[1]))
    start_new_thread(thread, (tcp_client,))
sock_tcp.close()
socket.socket.shutdown(sock_tcp)
