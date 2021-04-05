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
    """Get the requested data from database
    'all' - prints the entire database
    'month' - prints the selected month
    int year - print the selected year """
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

# move to put
def dateTime():
    df = pd.read_csv("Data.csv")

    df['date'] = df['date'] = pd.to_datetime(df['date'])
    '''snu etter søk ellers funker ikke den Amrikanske dritten'''
    #df['date'] = df['date'].dt.strftime('%d/%m/%Y')
    print(df)
    print(df['date'].between('01-05-1981', '05-05-1981'))
    print(df.loc[df['date'].between('1981-05-01','1981-05-05')])

#dateTime()
#data = ws.collect_weather_data(180)
#put(data)
#new_database()
#get('all')

from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('localhost', 55555))

while True:

    ##recieve message and address with the sock.recvfrom
    msg, addr = sock.recvfrom(2048)
    ##decode message
    text = msg.decode()
    print(text)

    ##checks for spaces, if it is just spaces it wont save this
    if text.strip():
        ##Get date and time
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        ##Opens a file and writes to it
        f = open('notebook.txt','a') ##use append instead of write, wont overwrite, just add to the end.
        ##write the user address, timestamp and the text
        f.write(f'User: {addr[0]} : Timestamp: {date} \n' + '- ' + text + '\n\n')
        f.close()

        ##print what he wrote
        print(f'{addr[0]} wrote {msg.decode()}')
        ##send acknowledgement to client that you have connected to the server
        sock.sendto((f'Server: ACK'.encode()), addr)
    else:
        ##
        sock.sendto(('Server: You have to write something buddy!'.encode()), addr)
