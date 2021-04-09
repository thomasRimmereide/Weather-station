from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# /city/bergen
@app.route('/city/<city_name>')
def get_city_weather_data(city_name):
    file = open("../MA/Database_files/Oslo_WS.csv", "r")

    test_data = []
    for line in file.readlines()[1:]:
        test_data.append(line.split(","))

    return render_template('city.html', city_name=city_name, data=test_data)

# @app.route('/city/<city_name>/from/<fromDate>/to/<toDate>')

if __name__ == '__main__':
    app.run()
