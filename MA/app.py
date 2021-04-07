from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    webpage = \
        stylesheet + \
        header() + \
        body() + \
        footer()
    return webpage


def header():
    return f'''
        <h2>
        <img src="weather.jpg" alt="weather">
           test
        </h2>
        <br/>
        <hr/>
    '''


def body():
    return '''
        <h3>Test</h3>
        <br/>
        <hr/>
        <p>
            test
        </p>
        <hr/>
    '''

def footer():
    return '''
        <footer>
            test
        </footer>
    '''


stylesheet = '''
    <style>
        body {
            font-size: 24px;
        }
        footer {
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid black;
        }
    </style>
'''