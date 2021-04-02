#storage server process

"""
Denne skal lese inn fra weather_station.py, og lagre dataen i csv-filen.
Den skal også gi FMI tilgang til dataen som er lagret hvis den får en forespørsel om det.

Står også at alle filene skal kunne kjøres i localhost, litt usikker på hva det menes med, men kanskje bare på pcen?

Første omgang:

Kunne lagre data fra en dictonary (feltnavn står i station.py) til en CSV fil.

"""
import csv 
import pandas as pd
import weather_station as ws 

messurments = {
"month" : ["may"],
"day_of_month" : [1,2,3,4,5,6,7],
"voltage" : [5,2,6,3],
"amp" : [2]

}

def PUT(messurments : dict):
    liste =  messurments.get("month")
    month = liste[0]
    #col  = [liste[0] for i in range (len(messurments.get("day_of_month")))]
   # dataframe = pd.DataFrame.from_dict(messurments)#, columns = col)
    dataframe = pd.concat([pd.Series(v, name=k) for k, v in messurments.items()], axis=1)
    dataframe = dataframe.fillna("-")
    #dataframe = dataframe.drop(index = "month")
    dataframe.to_csv("database\%s.csv" % (month), encoding='utf-8' ,index = False)
 

def GET(month : str):
    data = pd.read_csv("database\%s.csv" % (month))
    location_data = data.iloc[0,0]
    month_data = data.iloc[0,1]
    data = data.drop(columns = ['location','month'])
    print("Weather data for %s in %s " %(location_data, month_data))
    dictionary = pd.DataFrame.to_dict(data)
    print(data)
    return dictionary

    

#PUT(messurments)
data= ws.collect_weather_data(30)
PUT(data)
GET("may")
