# storage server process

"""
Denne skal lese inn fra weather_station_bergen.py, og lagre dataen i csv-filen.
Den skal også gi FMI tilgang til dataen som er lagret hvis den får en forespørsel om det.

Står også at alle filene skal kunne kjøres i localhost, litt usikker på hva det menes med, men kanskje bare på pcen?

Første omgang:

Kunne lagre data fra en dictonary (feltnavn står i station.py) til en CSV fil.

"""
import pickle

import pandas as pd
from pandas.errors import EmptyDataError

from io import BufferedReader
import socket
import os
from _thread import start_new_thread

# Dummy data for development
measurements = {
    "month": ["May", "May", "June"],
    "location": ["bergen"],
    "date": ["01.may.2012", "02.may.2012", "03.may.2012", "01.jun.2012", "02.june.2012", "03.june.2012", "01.aug.2012"],
    "voltage": [5, 2, 6, 3],
    "amp": [2]
}


def put(weather_station_data: dict):
    """Put data from weather_station into database"""
    dataframe = pd.concat([pd.Series(v, name=k) for k, v in weather_station_data.items()], axis=1)
    dataframe = dataframe.fillna("-")
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    # use the python tell function to check if the "database" is empty. if so we add headers if false we dont
    with open("Data.csv", 'a') as database:
        dataframe.to_csv("Data.csv", mode='a', encoding='utf-8', index=False, header=database.tell() == 0)


''''
def get(request):
    """Get the requested data from database
    'all' - prints the entire database
    'month' - prints the selected month
    int year - print the selected year """
    try:
        weather_data = pd.read_csv("Data.csv")
        if request == "all":
            show_request(weather_data)
            return weather_data
        else:
            get_period()
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
'''


def get_month(weather_data, month: str):
    """Return all data in database for chosen month """
    print(weather_data.loc[weather_data['date'].dt.month])
    return weather_data[
        weather_data['date'].dt.month.str.contains(month)]  # weather_data[weather_data['month'].str.contains(month)]


def get_year(weather_data, day: int):
    """Return all data in database for chosen year"""
    return weather_data[weather_data['year'].astype(str).str.contains(str(str(day)))]


def get_period(start_date: str, end_data: str, database):
    return database.loc[database['date'].between(start_date, end_data)]


def new_database():
    """Emptying the database"""
    database = open("Data.csv", 'r+')
    database.truncate(0)
    database.close()

# move to put
def dateTime():
    df = pd.read_csv("Data.csv")

    # df['date'] = df['date'] = pd.to_datetime(df['date'])

    '''snu etter søk ellers funker ikke den Amrikanske dritten'''
    print(get_period('2012-05-01', '2012-06-05', df), "return")
    # df['date'] = df['date'].dt.strftime('%d/%m/%Y')
    # print(df)
    # print(df['date'].between('01-05-1981', '05-05-1981'))
    # print(df.loc[df['date'].between('01.05.1981', '05.05.1981')])

#print(get_period('2012-05-02', '2012-05-20',pd.read_csv("Data.csv")))

# dateTime()
# data = ws.collect_weather_data()
# put(measurements)
# new_database()
# get('may')


sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
tcp_port = 6969
sock_tcp.bind((host, tcp_port))

print('Server is running')
sock_tcp.listen(5000)


def get_request(com_request: list):
    entire_database = pd.read_csv("Data.csv")
    print("getrequest")
    if 'all' in com_request:
        return entire_database
    else:
        return get_period(com_request[-2], com_request[-1], entire_database)


def thread(connection):
    connection.send(str.encode('Connected to Database Bergen'))
    data = connection.recv(2048)
    connected_client = data.decode()

    while True:
        if connected_client == 'Bergen WS':
            data = connection.recv(2048)
            print(pickle.loads(data))
        elif connected_client == 'request_computer':
            data = connection.recv(2048)
            req = pickle.loads(data)
            resp = get_request(req)
            connection.sendall(pickle.dumps(resp))
        # TODO add stop
        if data == 'stop':
            break
    connection.close()


while True:
    tcp_client, tcp_address = sock_tcp.accept()
    print('Connected to: ' + tcp_address[0] + ':' + str(tcp_address[1]))
    start_new_thread(thread, (tcp_client,))

ServerSocket.close()
