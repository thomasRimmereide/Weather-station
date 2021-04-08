import pandas as pd


def put(weather_station_data):
    """Put data from weather_station into database"""
    dataframe = pd.concat([pd.Series(v, name=k) for k, v in weather_station_data.items()], axis=1)
    dataframe = dataframe.fillna("-")
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    """Use the python tell function to check if the "database" is empty. if so we add headers if false we dont"""
    with open("Data.csv", 'a') as database:
        dataframe.to_csv("Data.csv", mode='a', encoding='utf-8', index=False, header=database.tell() == 0)


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
