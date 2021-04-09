from MA.Help_functions.station import StationSimulator

from time import sleep
import pickle as pickle
import socket


global date_to_start_next_reading_on
date_to_start_next_reading_on = {"day_bergen": 1, "month_bergen": "May", "year_bergen": 1981}


def collect_weather_data(amount_of_days_to_log=10, simulation_interval=1):
    global date_to_start_next_reading_on

    date_to_start_next_reading_on = update_today_date()

    # Initializing data from station
    bergen_station = StationSimulator(simulation_interval=simulation_interval)

    days_of_month = getattr(bergen_station, "_days_of_month", None)

    # Sets the current date and month
    current_day = date_to_start_next_reading_on.get("day_bergen")
    bergen_station.month = date_to_start_next_reading_on.get("month_bergen")
    current_year = date_to_start_next_reading_on.get("year_bergen")

    # Dictionary to be sent to storage
    data_from_station = {"location": [], "date": [], "rain": [],
                         "temperature": []}

    bergen_station.turn_on()

    for _ in range(1, amount_of_days_to_log + 1):
        sleep(simulation_interval)

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

    save_today_date(today_date={"day_bergen": current_day, "month_bergen": bergen_station.month,
                                "year_bergen": current_year})
    bergen_station.shut_down()

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
location = "Bergen_WS"
ClientSocket.send(pickle.dumps(location))
while True:
    data_string = pickle.dumps(collect_weather_data())
    ClientSocket.sendall(data_string)
    sleep(60)
ClientSocket.close()
