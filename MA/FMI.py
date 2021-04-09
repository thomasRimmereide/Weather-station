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
from time import sleep

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969


def show_request(weather_data):
    """Print the get request to terminal or error message if not in database"""
    # TODO Move to storage
    if weather_data.empty:
        print("The requested data is not found in database")
    else:
        location_data = weather_data.iloc[0, 0]
        print("Weather data for %s  " % (location_data))
        print(weather_data.reset_index(drop=True))


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def request_packet():
    """Return a list containing all user request to the database"""
    request_packet_list = []
    weather_data_location = input("Enter location: ")
    request_packet_list.append(weather_data_location)
    amount_of_data = input("Do you want all the data or a period \n Type: all or period: ")
    request_packet_list.append(amount_of_data)
    if amount_of_data == 'all':
        return request_packet_list
    else:
        start_date = input("Enter start date for the period yyyy-mm-dd \n")
        request_packet_list.append(start_date)
        stop_date = input("Enter stop date for the period yyyy-mm-dd \n ")
        request_packet_list.append(stop_date)
        return request_packet_list

def new_request_package():
    """Return a list containing all user request to the database as given by user in terminal"""
    request_packet_list = []
    weather_data_location = input("Enter location: ")
    amount_of_data = input("Do you want all the data or a period \n Type: all or period: ")

    request_packet_list.append(weather_data_location)
    request_packet_list.append(amount_of_data)
    if amount_of_data == 'all':
        return create_data_request(weather_data_location)

    start_date = input("Enter start date for the period yyyy-mm-dd \n")
    stop_date = input("Enter stop date for the period yyyy-mm-dd \n ")
    return create_data_request(weather_data_location, amount_of_data, start_date, stop_date)


def create_data_request(location, amount_of_data="all", start_date="", stop_date=""):
    """Return a list containing all user request to the database"""
    request_data = [location, amount_of_data]
    if amount_of_data == "all":
        return request_data

    request_data.append(start_date)
    request_data.append(stop_date)
    return request_data


def initialize_tcp():
    # tcp_client_socket.connect((host, port))
    type_of_client = ["request_computer"]
    tcp_client_socket.send(pickle.dumps(type_of_client))
    # initial_response = tcp_client_socket.recv(1024)
    # print(initial_response.decode())


def run_tcp():
    tcp_client_socket.send(pickle.dumps(request_packet()))
    database_response = tcp_client_socket.recv(16384)
    print(show_request(pickle.loads(database_response)))


def storage_east_request():
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.bind(("localhost", 5555))
    udp_client_socket.sendto(pickle.dumps(request_packet()), ("localhost", 1337))
    response, addr = udp_client_socket.recvfrom(16384)
    received_weather_data = pickle.loads(response)
    print(received_weather_data)
    udp_client_socket.close()


# tcp_client_socket.connect((host, port))


choose_database = input("East or West database: ")
tcp_client_socket.connect((host, port))
while True:
    if choose_database.lower() == 'west':
        initialize_tcp()
        break
    elif choose_database.lower() == 'east':
        initialize_tcp()
        break
    else:
        continue

while True:
    if choose_database.lower() == 'west':

        run_tcp()
    else:
        storage_east_request()
    choose_database = input("choose west, east or shutdown \n")
    if choose_database == "shutdown":
        shutdown = [user_request]
        tcp_client_socket.send(pickle.dumps(shutdown))
        break
    else:
        continue
    # TODO test clear with terminal
    clear()

clear()
print("Client is disconnected")
tcp_client_socket.close()
