# storage server process

"""
Denne skal lese inn fra weather_station.py, og lagre dataen i csv-filen.
Den skal også gi FMI tilgang til dataen som er lagret hvis den får en forespørsel om det.

Står også at alle filene skal kunne kjøres i localhost, litt usikker på hva det menes med, men kanskje bare på pcen?

Første omgang:

Kunne lagre data fra en dictonary (feltnavn står i station.py) til en CSV fil.

"""

import pandas as pd
from pandas.errors import EmptyDataError
import weather_station as ws

# Dummy data for development
measurements = {
    "month": ["May", "May", "June"],
    "location": ["bergen"],
    "year": [2012, 2013, 2013, 2014, 2015, 2016, 2017],
    "voltage": [5, 2, 6, 3],
    "amp": [2]
}


def put(weather_station_data: dict):
    """Put data from weather_station into database"""
    dataframe = pd.concat([pd.Series(v, name=k) for k, v in weather_station_data.items()], axis=1)
    dataframe = dataframe.fillna("-")
    # use the python tell function to check if the "database" is empty. if so we add headers if false we dont
    with open("Data.csv", 'a') as database:
        dataframe.to_csv("Data.csv", mode='a', encoding='utf-8', index=False, header=database.tell() == 0)


def get(request):
    """Get the requested data from database"""
    try:
        weather_data = pd.read_csv("Data.csv")
        if request == "all":
            show_request(weather_data)
        elif isinstance(request, int):
            show_request(get_year(weather_data, request))
        else:
            show_request(get_month(weather_data, request.capitalize()))
    except EmptyDataError:
        print("database is empty")


def show_request(weather_data):
    """Print the get request to terminal or error message if not in database"""
    if weather_data.empty:
        print("The requested data is not found in database")
    else:
        location_data = weather_data.iloc[0, 0]
        month_data = weather_data.iloc[0, 1]
        print("Weather data for %s in %s " % (location_data, month_data))
        print(weather_data.reset_index(drop=True))


def get_month(weather_data, month: str):
    """Return all data in database for chosen month """
    return weather_data[weather_data['month'].str.contains(month)]


def get_year(weather_data, day: int):
    """Return all data in database for chosen year"""
    return weather_data[weather_data['year'].astype(str).str.contains(str(str(day)))]


def new_database():
    """Emptying the database"""
    database = open("Data.csv", 'r+')
    database.truncate(0)
    database.close()


# data = ws.collect_weather_data(60)
# put(measurements)
# new_database()
get('all')
