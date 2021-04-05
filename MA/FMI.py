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
from socket import socket
import storage


def welcome():
    print("tisstass")
    command = input("which data do you want")
    storage.get(command)


def tisstass():
    sock = socket()
    sock.connect(storage)
    request = input("Input: ")  # change variable name

    sock.send(request.encode())
    new_request = sock.recv(1024).decode()
    print(f"tisstass")
    sock.close()


welcome()
