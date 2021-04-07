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
import os

def show_request(weather_data):
    """Print the get request to terminal or error message if not in database"""
    #TODO Move to storage
    if weather_data.empty:
        print("The requested data is not found in database")
    else:
        location_data = weather_data.iloc[0, 0]
        print("Weather data for %s  " % (location_data))
        print(weather_data.reset_index(drop=True))


def clear():
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


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
    print(show_request(pickle.loads(response)))
    ## new data ?? clear()


ClientSocket.close()

