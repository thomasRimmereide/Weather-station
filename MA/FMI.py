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
from socket import socket, AF_INET, SOCK_DGRAM
import pandas as pd
import os

import socket

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969

print('Waiting for connection')
ClientSocket.connect((host, port))
choose_database = input("Which location? ")
ClientSocket.send(str.encode(choose_database))
Response = ClientSocket.recv(1024)
while True:
    msg = input('Say Something: ')
    ClientSocket.send(str.encode(msg))
    response = ClientSocket.recv(4096)
    print(pickle.loads(response))

    #print(Response.decode('utf-8'))

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
