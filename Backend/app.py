from flask import Flask
import models
from resources.datapoint import datapoints_api
from flask_cors import CORS, cross_origin
import requests
import openaq
import pandas as pd
from OpenAqDataHandler import OpenAqDataHandler

DEBUG = True

app = Flask(__name__)
app.register_blueprint(datapoints_api, url_prefix='/api/v1')
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello_World'


def init_database():
    api = openaq.OpenAQ()

    resp = api.countries()
    print(resp)

def addSomeEntries():
    print("are we here?")
    entry = {"city": "Heidelberg", "country": "DE", "location": "Alter Muehle", "pm25": 156}
    for i in range(0, 100):
        models.DataPoint.create(**entry)
    print(entry)



# print(api.latest())
# print(requests.get("https://api.openaq.org/v1/locationscity[]=Lisboa&city[]=Porto"))


if __name__ == '__main__':

    models.initialize()
    openaqDataHandler = OpenAqDataHandler()
    #openaqDataHandler.fetchLatestDataFromAllCountries()
    app.run(debug=DEBUG)
    #init_database()

