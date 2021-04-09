from flask import Flask, render_template
import pickle
import socket

app = Flask(__name__)


def get_data(request_data):
    ''' Get data from storage with UDP '''
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.bind(("localhost", 5555))
    udp_client_socket.sendto(pickle.dumps(request_data), ("localhost", 1337))
    response, addr = udp_client_socket.recvfrom(16384)
    return pickle.loads(response).values.tolist()


@app.route('/')
def index():
    return render_template('index.html')


# /city/bergen
@app.route('/city/<city_name>')
def get_city_weather_data(city_name):
    request_data = [city_name, "all"]
    data = get_data(request_data)
    print(data)

    min_date = ""
    max_date = ""
    if len(data) > 0:
        min_date = data[0][1]
        max_date = data[-1][1]

    return render_template(
        'city.html',
        city_name=city_name,
        data=data,
        min_date=min_date,
        max_date=max_date,
    )


@app.route('/city/<city_name>/from/<from_date>/to/<to_date>')
def get_city_weather_data_for_period(city_name, from_date, to_date):
    request_data = [city_name, "period", from_date, to_date]
    data = get_data(request_data)
    return render_template('city.html', city_name=city_name, data=data)


if __name__ == '__main__':
    app.run()
