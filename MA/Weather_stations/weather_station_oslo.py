from MA.Help_functions.station import StationSimulator

from time import sleep
import socket
import pickle as pickle


global date_to_start_next_reading_on
date_to_start_next_reading_on = {"day_oslo": 1, "month_oslo": "May", "year_oslo": 1981}


def collect_weather_data(amount_of_days_to_log=1, simulation_interval=1):
    global date_to_start_next_reading_on
    date_to_start_next_reading_on = update_today_date()

    oslo_station = StationSimulator(simulation_interval=simulation_interval)

    days_of_month = getattr(oslo_station, "_days_of_month", None)
    current_day = date_to_start_next_reading_on.get("day_oslo")
    oslo_station.month = date_to_start_next_reading_on.get("month_oslo")
    current_year = date_to_start_next_reading_on.get("year_oslo")
    oslo_station.location = "Oslo"

    data_from_station = {"location": [], "date": [], "rain": [],
                         "temperature": []}
    oslo_station.turn_on()

    for _ in range(1, amount_of_days_to_log + 1):
        sleep(simulation_interval)

        current_date = str(current_day) + "." + str(oslo_station.month) + "." + str(current_year)

        data_from_station["location"].append(oslo_station.location)
        data_from_station["date"].append(current_date)
        data_from_station["rain"].append(oslo_station.rain)
        data_from_station["temperature"].append(oslo_station.temperature)

        if days_of_month.get(oslo_station.month) == current_day:
            if oslo_station.month == "December":
                oslo_station.month = "January"
                current_year += 1
                current_day = 0
            else:
                find_next_month = list(days_of_month)
                next_month = find_next_month[find_next_month.index(oslo_station.month) + 1]

                oslo_station.month = next_month
                current_day = 0
        current_day += 1

    save_today_date(today_date={"day_oslo": current_day, "month_oslo": oslo_station.month, "year_oslo": current_year})
    oslo_station.shut_down()
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


ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 1337


try:
    while True:
        data_string = pickle.dumps(collect_weather_data())
        ClientSocket.sendto(data_string, (host, port))
        sleep(60)
except KeyboardInterrupt:
    print("Weather station Oslo has stopped!")

ClientSocket.close()
