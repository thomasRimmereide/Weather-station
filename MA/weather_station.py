from station import StationSimulator

from time import sleep

"""
Leser info fra station.py, skal egentlig bare bruke info derfra, og sende det videre til storage.py i den formen vi syntes
er best. Tenker vi kan starte med å bruke en csv-fil til å lagre dataen, så hvis vi får tid kan vi bruke mongoDB,
men har aldri brukt det skikkelig til python.

Kan hende det er best å lagre i dictonary for å få det best inn i csv-filen, eller bruke list-in-list for å få verdiene
med riktig parameter. Parametrene ligger i en kommentar i station.py. Vi kan også bruke example.py som inspirasjon til denne.

Første omgang:

Kunne hente inn data fra station.py, og lagre det i en dictonary som skal kunne bli sendt over til storage
via nettverket.
"""


def collect_weather_data(amount_of_days_to_log=10):
    simulation_interval = 1

    # Initializing data from station
    bergen_station = StationSimulator(simulation_interval=simulation_interval)

    # Dictionary to be sent to storage
    data_from_station = {"location": [], "month": [], "rain": [],
                         "temperature": []}

    bergen_station.turn_on()

    for _ in range(1, amount_of_days_to_log+1):
        sleep(simulation_interval)

        data_from_station["location"].append(bergen_station.location)
        data_from_station["month"].append(bergen_station.month)
        data_from_station["rain"].append(bergen_station.rain)
        data_from_station["temperature"].append(bergen_station.temperature)

    bergen_station.shut_down()

