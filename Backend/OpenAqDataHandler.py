import openaq
import pandas as pd

import models


class OpenAqDataHandler:
    def __init__(self):
        self.api = openaq.OpenAQ()


    def getCountries(self):
        countries = self.api.countries(df = True)
        countries = countries[countries['name'].notna()]

    def getCities(self, country):
        cities = self.api.countries(df=True, country=country)
        cities = cities[cities['name'].notna()]

    def getLocations(self, country):
        locations = self.api.locations(df=True, country=country, limit=10000)

    def getPM25valuesOfAllLocationsOfCountry(self, country):
        api = openaq.OpenAQ()
        try:
            resp, latest = api.latest(country=country, parameter="pm25", limit=1000)
            results = latest['results']

            if resp == 200:
                for el in results:
                    location = el['location']
                    country = el['country']
                    city = el['city']
                    measurements = el['measurements']
                    pm25_value = measurements[0]['value']
                    lastUpdated = measurements[0]['lastUpdated']
                    self.addDataPoint(city, country, location, pm25_value, lastUpdated)
            else:
                print("Problems due to following HTTP Error code ", resp)
        except:
            print("Something went wrong with getting data from country", country)

    def fetchLatestDataFromAllCountries(self):
        api = openaq.OpenAQ()
        countries = api.countries(df=True, limit=500)
        countries = countries[countries['name'].notna()]
        print("got countries")
        print(countries['name'], countries['code'])
        failed_countries = []
        for country in countries['code']:
            try:
                self.getPM25valuesOfAllLocationsOfCountry(country)
            except:
                print("Couldn't fetch country", country)
                failed_countries.append(country)

    def addDataPoint(self, city, country, location, pm25, lastUpdated):
        entry = {"city": city, "country": country, "location": location, "pm25":pm25, "lastUpdated": lastUpdated}
        models.DataPoint.create(**entry)
        print("entry created")


