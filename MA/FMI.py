# FMI script

"""

Skal kjøres i CLI! Skal kunne vise all data som ligger i csv-filen, altså hente det fra en metode i storage.

Første omgang Nettverk:

Få inn basic nettverk kode, med TCP port og UDP porter, sikkert bind, skal bruke localhost.

FMI -               user agent
storage -           server
weather_station -   client

Gjerne se på tidligere oppgaver:)
"""
import pickle
import socket

def request():
    req = []
    amount = input("Do you want all the data or a period \n Type: all or period")
    req.append(amount)
    if amount == 'all':
        return req
    else:
        start = input("Enter start date for the period yyyy-mm-dd \n")
        req.append(start)
        stop = input("Enter stop date for the period yyyy-mm-dd \n ")
        req.append(stop)
        return req


ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969

ClientSocket.connect((host, port))
choose_database = "request_computer"
ClientSocket.send(str.encode(choose_database))
response = ClientSocket.recv(1024)
print(response.decode())

while True:

    ClientSocket.send(pickle.dumps(request()))
    response = ClientSocket.recv(4096)
    print(pickle.loads(response))

ClientSocket.close()

