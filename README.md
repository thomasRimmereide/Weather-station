# Library's needed to run the code  
    - pickle  - Is used to code and decode data fro transmission througt the socket
    - socket  - Is used to create and handle python sockets 
    - _thread - Is used to thread clients
    - time    - Is used to send data periodically from weather stations 
    - Flask   - Is used to develop web application

# How it works 

![alt text](https://github.com/thomasRimmereide/INF142-Mandatory-Assignment-VET/blob/main/MA/system_overview.png?raw=true)
    
    Storage_west is a database that recivie data periodically from weather_station Bergen and Stavanger.
    It stores the recived data to the file Bergen_WS.csv and Stavanger_WS.csv using the DMBS.
    It also recive data request from FMI and app, finds the requested data and returns it to the client asking for data.
    Both the user clients and the weather stations communicate with Storage_west over TCP

    Storage_east works in a similar way only difference is it recive weather_data from Oslo
    It also uses UDP insted of TCP to communicate.

# How to run code using terminal

    1. You need to start the servers first, to do so: 
       Start storage_east.py and storage_west.py. Located in the folder ..MA/Storage_handlers
    2. Then start the weather_stations to start the data collection, to do so:     
       Start weather_station_bergen.py, weather_station_stavanger.py, weather_station_oslo.py 
       located in ..MA/Weather_stations.
    3. Then start the user client which is the file FMI.py located in ..MA/FMI.py
       Then follow the instructions in the terminal.

# How to run code using web application 
    
    1. You need to start the servers first, to do so: 
       Start storage_east.py and storage_west.py. Located in the folder ..MA/Storage_handlers
    2. Then navigate to the GUI directory in the terminal using the command "cd GUI".
    3. In the terminal, write the command "flask run".
    4. Press the link recieved in the terminal, this will open a web browser window. 
    5. On the webpage, choose a location. Here, all available data will be presented in a table. 
       You can scroll down this table or choose only to view data within a specific time period.

    The webpage have been tested on multiple web browsers, however, Chrome is recommended if possible. 

###Authors 
    - Erlend Osland Nytveit
    - Thomas Rimmereide
    - Vilde Emilie Søvik Haugstad
        
 
