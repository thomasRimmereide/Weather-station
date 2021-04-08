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


tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969


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
    else:
        _ = os.system('clear')


def request_packet():
    """Return a list containing all user request to the database"""
    request_packet_list = []
    weather_data_location = input("Enter location")
    request_packet_list.append(weather_data_location)
    amount_of_data = input("Do you want all the data or a period \n Type: all or period")
    request_packet_list.append(amount_of_data)
    if amount_of_data == 'all':
        return request_packet_list
    else:
        start_date = input("Enter start date for the period yyyy-mm-dd \n")
        request_packet_list.append(start_date)
        stop_date = input("Enter stop date for the period yyyy-mm-dd \n ")
        request_packet_list.append(stop_date)
        return request_packet_list


tcp_client_socket.connect((host, port))
type_of_client = "request_computer"
tcp_client_socket.send(str.encode(type_of_client))
initial_response = tcp_client_socket.recv(1024)
print(initial_response.decode())

while True:

    tcp_client_socket.send(pickle.dumps(request_packet()))
    database_response = tcp_client_socket.recv(16384)
    print(show_request(pickle.loads(database_response)))
    user_request = input("new data or shutdown? (new data/shutdown) \n")
    if user_request == "shutdown":
        shutdown = [user_request]
        tcp_client_socket.send(pickle.dumps(shutdown))
        break
    else:
        continue
    #TODO test clear with terminal
    clear()

clear()
print("Client is disconnected")
tcp_client_socket.close()


