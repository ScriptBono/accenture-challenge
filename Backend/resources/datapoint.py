from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal_with, marshal
import requests
import requests
import openaq
import pandas as pd

import models

datapoint_fields = {
    'id': fields.Integer,
    'location': fields.String,
    'city': fields.String,
    'country': fields.String,
    'pm25': fields.Integer,
    'lastUpdated': fields.String
}

class DataPointList(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'location',
            required=True,
            help='No location provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'city',
            required=True,
            help='No city provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'country',
            required=True,
            help='No country provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'pm25',
            required=False,
            type=inputs.positive,
            default=-1,
            help='No pm25 value provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'lastUpdated',
            required=False,
            default="N/A",
            help='No lastUpdated value provided',
            location=['form', 'json']
        )
        super().__init__()



    def get(self):
        datapoints = [marshal(datapoint, datapoint_fields) for datapoint in models.DataPoint.select()]
        return {'Datapoints': datapoints}
    # def get(self):
    #
    #     # models.initialize()
    #     # app.run(debug=DEBUG)
    #     api = openaq.OpenAQ()
    #     status, resp = api.measurements(city='Delhi', location='Anand Vihar', limit=10000)
    #     # status, resp = api.cities()
    #     # print(status)
    #     print(resp)
    #     return resp

    # def get(self):
    #     return jsonify({"results": [
    #         {"location": " 淮河道", "city": "天津市", "country": "CN", "distance": 6362943.410902514, "measurements": [
    #             {"parameter": "o3", "value": 191, "lastUpdated": "2019-03-19T07:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "no2", "value": 23, "lastUpdated": "2019-03-19T06:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "so2", "value": 19, "lastUpdated": "2019-03-19T06:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "pm25", "value": 76, "lastUpdated": "2019-03-19T06:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "pm10", "value": 110, "lastUpdated": "2019-03-19T06:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "co", "value": 600, "lastUpdated": "2019-03-19T07:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "ChinaAQIData", "averagingPeriod": {"value": 1, "unit": "hours"}}],
    #          "coordinates": {"latitude": 39.2133, "longitude": 117.1837}},
    #         {"location": "(Folkungagatan tillfälligt avstängd)", "city": "Stockholm", "country": "SE", "measurements": [
    #             {"parameter": "pm10", "value": -99, "lastUpdated": "2018-04-04T15:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "Sweden", "averagingPeriod": {"value": 1, "unit": "hours"}},
    #             {"parameter": "no2", "value": -99, "lastUpdated": "2018-04-04T15:00:00.000Z", "unit": "µg/m³",
    #              "sourceName": "Sweden", "averagingPeriod": {"value": 1, "unit": "hours"}}]}
    #
    #     ]})

    def post(self):
        args = self.reqparse.parse_args()
        models.DataPoint.create(**args)
        return jsonify(args)

    def addSomeEntries(self):
        entry = {"city": "Heidelberg", "country": "DE", "location": "Alter Muehle", "pm25": 156}
        args = self.reqparse.parse_args()
        models.DataPoint.create(**args)
        return jsonify(args)

class DataPoint(Resource):

    def get(self, id):
        return jsonify({'course': 1, 'rating': 5})

    def get(self, id):
        return jsonify({'course': 1, 'rating': 5})

    @marshal_with(datapoint_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.DataPoint.update(**args)
        query.execute()
        return ("added")


datapoints_api = Blueprint('resources.datapoints', __name__)
api = Api(datapoints_api)
api.add_resource(
    DataPointList,
    '/datapoints',
    endpoint='datapoints'
)

api.add_resource(
    DataPointList,
    '/datapoints/<int:id>',
    endpoint='datapoint'
)
