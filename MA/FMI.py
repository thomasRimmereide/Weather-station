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
from socket import socket, AF_INET, SOCK_DGRAM


# import storage

import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()


"""
def welcome():
    command = input("which data do you want")
    storage.get(command)
"

socket = socket(AF_INET, SOCK_DGRAM)

while {(text := input('> ').lower()) != 'shut down'}:
    socket.sendto(text.encode(), ('localhost', 55555))
    msg, addr = socket.recvfrom(2048)
    print(msg.decode())




def tisstass():
    sock = socket()
    sock.connect(storage)
    request = input("Input: ")  # change variable name

    sock.send(request.encode())
    new_request = sock.recv(1024).decode()
    print(f"tisstass")
    sock.close()
"""

# welcome()
