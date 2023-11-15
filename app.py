from flask import Flask, render_template, request
from mbta_helper import find_stop_near
from wtforms import Form


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("hello.html")

@app.route('/findstation/', methods = ['GET', 'POST'])
def find_station(query=None):
    if request.method == 'POST':
        query = request.form['query']
        nearest_station_info = find_stop_near(query)
        return render_template('result.html', nearest_station_info)
    else:  
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
