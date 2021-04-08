from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# /city/bergen
@app.route('/city/<city_name>')
def get_city_weather_data(city_name):
    print("City name is " + city_name)
    return render_template('city.html', city_name=city_name)


if __name__ == '__main__':
    app.run()
