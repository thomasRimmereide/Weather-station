# FMI script

import pickle
import socket
from MA.Help_functions import terminal_handler as th

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969


def show_request(weather_data):
    """Print the get request to terminal or error message if not in database"""
    if weather_data.empty:
        print("The requested data is not found in database")
        return []
    else:
        location_data = weather_data.iloc[0, 0]
        print("Weather data for %s  " % (location_data))
        print(weather_data.reset_index(drop=True))
        return location_data


def new_request_package():
    """Return a list containing all user request to the database as given by user in terminal"""
    request_packet_list = []
    weather_data_location = th.choose_location()
    amount_of_data = th.choose_amount()

    request_packet_list.append(weather_data_location)
    request_packet_list.append(amount_of_data)
    if amount_of_data == 'all':
        return create_data_request(weather_data_location)

    start_date = th.period("start")
    stop_date = th.period("stop")
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
    type_of_client = ["request_computer"]
    tcp_client_socket.send(pickle.dumps(type_of_client))


def run_tcp(request_data=None):
    # Get data from terminal if not sent as parameter
    if request_data is None:
        request_data = new_request_package()

    tcp_client_socket.send(pickle.dumps(request_data))
    database_response = tcp_client_socket.recv(16384)
    data = show_request(pickle.loads(database_response))
    return data


def storage_east_request(request_data=None):
    # Get data from terminal if not sent as parameter
    if request_data is None:
        request_data = new_request_package()

    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.bind(("localhost", 5555))
    udp_client_socket.sendto(pickle.dumps(request_data), ("localhost", 1337))
    response, addr = udp_client_socket.recvfrom(16384)
    received_weather_data = pickle.loads(response)
    print(received_weather_data)
    udp_client_socket.close()

    return received_weather_data


tcp_client_socket.connect((host, port))
choose_database = th.initial_user_input()
initialize_tcp()
while True:
    if choose_database.lower() == 'west':
        run_tcp()
    else:
        storage_east_request()

    choose_database = th.choose_next_move()
    if choose_database == "shutdown":
        shutdown = [choose_database]
        tcp_client_socket.send(pickle.dumps(shutdown))
        break
    else:
        continue


print("Client is disconnected")
tcp_client_socket.close()
