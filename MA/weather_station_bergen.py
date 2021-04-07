from station import StationSimulator

from time import sleep
import socket
import pickle as pickle

"""
Leser info fra station.py, skal egentlig bare bruke info derfra, og sende det videre til storage.py i den formen vi syntes
er best. Tenker vi kan starte med å bruke en csv-fil til å lagre dataen, så hvis vi får tid kan vi bruke mongoDB,
men har aldri brukt det skikkelig til python.

Kan hende det er best å lagre i dictonary for å få det best inn i csv-filen, eller bruke list-in-list for å få verdiene
med riktig parameter. Parametrene ligger i en kommentar i station.py. Vi kan også bruke example.py som inspirasjon til denne.


"""
global date_to_start_next_reading_on

date_to_start_next_reading_on = {"day": 1, "month": "May", "year": 1981}


def collect_weather_data(amount_of_days_to_log=10):
    global date_to_start_next_reading_on

    date_to_start_next_reading_on = update_today_date()

    # Initializing data from station
    bergen_station = StationSimulator(simulation_interval=1)

    days_of_month = getattr(bergen_station, "_days_of_month", None)

    # Sets the current date and month
    current_day = date_to_start_next_reading_on.get("day")
    bergen_station.month = date_to_start_next_reading_on.get("month")
    current_year = date_to_start_next_reading_on.get("year")

    # Dictionary to be sent to storage
    data_from_station = {"location": [], "date": [], "rain": [],
                         "temperature": []}

    bergen_station.turn_on()

    for _ in range(1, amount_of_days_to_log + 1):
        sleep(1)

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

    save_today_date(today_date={"day": current_day, "month": bergen_station.month, "year": current_year})
    bergen_station.shut_down()
    return data_from_station


def save_today_date(today_date=dict()):
    file = open("current_date.txt", "wb")
    pickle.dump(today_date, file)
    file.close()


def update_today_date():
    with open("current_date.txt", "rb") as data:
        today = data.read()
    d = pickle.loads(today)
    return d


print(collect_weather_data(20))
print(collect_weather_data(20))










"""
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969

ClientSocket.connect((host, port))
Response = ClientSocket.recv(1024)

while True:
    msg = "weather_staation her!!"
    data_string = pickle.dumps(collect_weather_data())
    ClientSocket.send(data_string)

    ClientSocket.send(str.encode(msg))
    Response = ClientSocket.recv(1024)
    print(Response.decode())
    time.sleep(5)
ClientSocket.close()
"""
"""
while {(text := input('> ').lower()) != 'shut down'}:
    socket.sendto(text.encode(), ('localhost', 55555))
    msg, addr = socket.recvfrom(2048)
    print(msg.decode())


# print(collect_weather_data(90, 1999, "November", 25))
"""