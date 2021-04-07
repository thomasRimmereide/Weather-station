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

import socket

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969

print('Waiting for connection')
ClientSocket.connect((host, port))

Response = ClientSocket.recv(1024)
while True:
    msg = input('Say Something: ')
    ClientSocket.send(str.encode(msg))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()


