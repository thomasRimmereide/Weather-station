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
import terminal_handler as th


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



def new_request_package():
    """Return a list containing all user request to the database as given by user in terminal"""
    request_packet_list = []
    weather_data_location = th.choose_location()#input("Enter location: ")
    amount_of_data = th.choose_amount() #input("Do you want all the data or a period \n Type: all or period: ")

    request_packet_list.append(weather_data_location)
    request_packet_list.append(amount_of_data)
    if amount_of_data == 'all':
        return create_data_request(weather_data_location)
    start_date = th.period("start") # input("Enter start date for the period yyyy-mm-dd \n")
    stop_date = th.period("stop") # input("Enter stop date for the period yyyy-mm-dd \n ")
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


def run_tcp():
    tcp_client_socket.send(pickle.dumps(new_request_package()))
    database_response = tcp_client_socket.recv(16384)
    print(show_request(pickle.loads(database_response)))


def storage_east_request():
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.bind(("localhost", 5555))
    udp_client_socket.sendto(pickle.dumps(new_request_package()), ("localhost", 1337))
    response, addr = udp_client_socket.recvfrom(16384)
    received_weather_data = pickle.loads(response)
    print(received_weather_data)
    udp_client_socket.close()


tcp_client_socket.connect((host, port))
choose_database = th.initial_user_input() #= input_from_user("East or West database: ", 'west', 'east')
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
