from station import StationSimulator

from time import sleep

from socket import socket, AF_INET, SOCK_DGRAM
import socket

"""
Leser info fra station.py, skal egentlig bare bruke info derfra, og sende det videre til storage.py i den formen vi syntes
er best. Tenker vi kan starte med å bruke en csv-fil til å lagre dataen, så hvis vi får tid kan vi bruke mongoDB,
men har aldri brukt det skikkelig til python.

Kan hende det er best å lagre i dictonary for å få det best inn i csv-filen, eller bruke list-in-list for å få verdiene
med riktig parameter. Parametrene ligger i en kommentar i station.py. Vi kan også bruke example.py som inspirasjon til denne.


"""


def collect_weather_data(amount_of_days_to_log=10, year=1981, month="May", day=1):
    simulation_interval = 1

    # Initializing data from station
    bergen_station = StationSimulator(simulation_interval=simulation_interval)

    days_of_month = getattr(bergen_station, "_days_of_month", None)

    # Sets the current date and month
    current_day = day
    bergen_station.month = month
    current_year = year

    # Dictionary to be sent to storage
    data_from_station = {"location": [], "date": [], "rain": [],
                         "temperature": []}

    bergen_station.turn_on()

    for _ in range(1, amount_of_days_to_log + 1):
        #sleep(simulation_interval)

        current_date = str(current_day) + "." + bergen_station.month + "." + str(current_year)

        data_from_station["location"].append(bergen_station.location)
        data_from_station["date"].append(current_date)
        data_from_station["rain"].append(bergen_station.rain)
        data_from_station["temperature"].append(bergen_station.temperature)

        if days_of_month.get(bergen_station.month) == current_day:
            if bergen_station.month == "December":
                bergen_station.month = "January"
                current_year += 1
                current_day = 0
            else:
                find_next_month = list(days_of_month)
                next_month = find_next_month[find_next_month.index(bergen_station.month) + 1]

                bergen_station.month = next_month
                current_day = 0
        current_day += 1
    bergen_station.shut_down()
    return data_from_station


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


socket = socket(AF_INET, SOCK_DGRAM)
"""
while {(text := input('> ').lower()) != 'shut down'}:
    socket.sendto(text.encode(), ('localhost', 55555))
    msg, addr = socket.recvfrom(2048)
    print(msg.decode())


# print(collect_weather_data(90, 1999, "November", 25))
"""