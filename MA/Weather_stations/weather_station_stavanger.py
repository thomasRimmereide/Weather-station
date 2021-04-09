from MA.Help_functions.station import StationSimulator

from time import sleep
import socket
import pickle as pickle

"""
Leser info fra station.py, skal egentlig bare bruke info derfra, og sende det videre til storage_west.py i den formen vi syntes
er best. Tenker vi kan starte med å bruke en csv-fil til å lagre dataen, så hvis vi får tid kan vi bruke mongoDB,
men har aldri brukt det skikkelig til python.

Kan hende det er best å lagre i dictonary for å få det best inn i csv-filen, eller bruke list-in-list for å få verdiene
med riktig parameter. Parametrene ligger i en kommentar i station.py. Vi kan også bruke example.py som inspirasjon til denne.


"""

date_to_start_next_reading_on = {"day_stavanger": 1, "month_stavanger": "May", "year_stavanger": 1981}


def collect_weather_data(amount_of_days_to_log=10, simulation_interval=1):
    global date_to_start_next_reading_on

    date_to_start_next_reading_on = update_today_date()

    # Initializing data from station
    stavanger_station = StationSimulator(simulation_interval=simulation_interval)

    days_of_month = getattr(stavanger_station, "_days_of_month", None)

    # Sets the current date and month
    current_day = date_to_start_next_reading_on.get("day_stavanger")
    stavanger_station.month = date_to_start_next_reading_on.get("month_stavanger")
    current_year = date_to_start_next_reading_on.get("year_stavanger")

    stavanger_station.location = "Stavanger"

    # Dictionary to be sent to storage
    data_from_station = {"location": [], "date": [], "rain": [],
                         "temperature": []}

    stavanger_station.turn_on()

    for _ in range(1, amount_of_days_to_log + 1):
        sleep(simulation_interval)

        current_date = str(current_day) + "." + stavanger_station.month + "." + str(current_year)

        data_from_station["location"].append(stavanger_station.location)
        data_from_station["date"].append(current_date)
        data_from_station["rain"].append(stavanger_station.rain)
        data_from_station["temperature"].append(stavanger_station.temperature)

        if days_of_month.get(stavanger_station.month) == current_day:
            if stavanger_station.month == "December":
                stavanger_station.month = "January"
                current_year += 1
                current_day = 0
            else:
                find_next_month = list(days_of_month)
                next_month = find_next_month[find_next_month.index(stavanger_station.month) + 1]

                stavanger_station.month = next_month
                current_day = 0
        current_day += 1

    save_today_date(today_date={"day_stavanger": current_day, "month_stavanger": stavanger_station.month,
                                "year_stavanger": current_year})

    stavanger_station.shut_down()
    return data_from_station


def save_today_date(today_date):
    d = update_today_date()
    d.update(today_date)
    file = open("../Database_files/current_date.pickle", "wb")
    pickle.dump(d, file)
    file.close()


def update_today_date():
    with open("../Database_files/current_date.pickle", "rb") as data:
        today = data.read()
    d = pickle.loads(today)
    return d


ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6969

ClientSocket.connect((host, port))
location = "Stavanger_WS"
ClientSocket.sendall(pickle.dumps(location))
while True:
    data_string = pickle.dumps(collect_weather_data())
    ClientSocket.sendall(data_string)
    sleep(60)
ClientSocket.close()