import datetime
import requests
import openaq
import pandas as pd
from peewee import *

DATABASE = SqliteDatabase('datapoints.sqlite')


class DataPoint(Model):



#    geo_data = CharField()
    location = CharField()
    city = CharField()
    country = CharField()
    lastUpdated = CharField(default="N/A")
    pm25 = IntegerField(default=-1)

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([DataPoint], safe=True)
    DATABASE.close()