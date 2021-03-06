import pandas as pd


def put(weather_station_data, type_of_client):
    database_name = "../Database_files/"+type_of_client+".csv"
    dataframe = pd.concat([pd.Series(v, name=k) for k, v in weather_station_data.items()], axis=1)
    dataframe = dataframe.fillna("-")
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    with open(database_name, 'a') as database:
        dataframe.to_csv(database_name, mode='a', encoding='utf-8', index=False, header=database.tell() == 0)


def get_month(weather_data, month: str):
    """Return all data in database for chosen month """
    print(weather_data.loc[weather_data['date'].dt.month])
    return weather_data[
        weather_data['date'].dt.month.str.contains(month)]


def get_year(weather_data, day: int):
    """Return all data in database for chosen year"""
    return weather_data[weather_data['year'].astype(str).str.contains(str(str(day)))]


def get_period(start_date: str, end_data: str, database):
    """Get data from a specified period"""
    return database.loc[database['date'].between(start_date, end_data)]


def get_request(com_request: list):
    """Return requested data"""
    database_name = "../Database_files/"+com_request[0].capitalize()+"_WS.csv"
    entire_database = pd.read_csv(database_name)
    if 'all' in com_request:
        return entire_database
    else:
        return get_period(com_request[-2], com_request[-1], entire_database)
