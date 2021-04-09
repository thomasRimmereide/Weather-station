import pickle
import socket
from MA.Help_functions import terminal_handler as th

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_host = 'localhost'
tcp_port = 6969


def pretty_print_data(weather_data):
    """PP for data"""
    location_data = weather_data.iloc[0, 0]
    print("Weather data for %s  " % location_data)
    print(weather_data.reset_index(drop=True))


def new_request_package():
    """Return a list containing all user request to the database as given by user in terminal"""
    request_packet = []
    weather_data_location = th.choose_location()
    amount_of_data = th.choose_amount()

    request_packet.append(weather_data_location)
    request_packet.append(amount_of_data)
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


def send_receive_storage_west():
    tcp_client_socket.send(pickle.dumps(new_request_package()))
    database_response = tcp_client_socket.recv(65536)
    print(pretty_print_data(pickle.loads(database_response)))


def send_receive_storage_east():
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.bind(("localhost", 5555))
    udp_client_socket.sendto(pickle.dumps(new_request_package()), ("localhost", 1337))
    response, addr = udp_client_socket.recvfrom(65536)
    received_weather_data = pickle.loads(response)
    print(received_weather_data)
    udp_client_socket.close()


tcp_client_socket.connect((tcp_host, tcp_port))
choose_storage = th.initial_user_input()
initialize_tcp()
while True:
    if choose_storage.lower() == 'west':
        send_receive_storage_west()
    else:
        send_receive_storage_east()
    choose_storage = th.choose_next_move()
    if choose_storage == "shutdown":
        shutdown = [choose_storage]
        tcp_client_socket.send(pickle.dumps(shutdown))
        break
    else:
        continue


print("Client is disconnected")
tcp_client_socket.close()
