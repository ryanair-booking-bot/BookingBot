"""This module does blah blah."""
# pylint: disable=too-few-public-methods
# pylint: disable=unused-variable

import os
import pandas as pd
from utils.decorators.singleton import Singleton

@Singleton
class Database(object):
    "Shared connection to the database"

    def __init__(self):

        self.flights = pd.read_csv('./models/flight-list.csv')
        self.codes = pd.read_csv('./models/airport-codes.csv', usecols=[9, 11]).dropna()

    def does_place_exist(self, destination_name):
        "Chcecks if the city has an airport"
        for index, row in self.codes.iterrows():
            if row[0] == destination_name:
                return True
        return False

    def get_flights(self, departure_station, arrival_station, departure_date):
        "ss"

        result = []
        for index, row in self.flights.iterrows():
            source = row[2]
            destination = row[3]
            date = row[0]
            if source == departure_station and destination == arrival_station \
                and date == departure_date:
                result.append([x for x in row])
        print result

    def get_airport_codes(self, city):
        "ss"

        result = []
        for index, row in self.codes.iterrows():
            if row[0] == city:
                result.append(row[1])
        return result

    def does_connection_exist(self, departure_station_code, arrival_station_code):
        "checks if there is any flight between two airports"

        for index, row in self.flights.iterrows():
            source = row[2]
            destination = row[3]
            if source == departure_station_code and destination == arrival_station_code:
                return True
        return False

    def does_any_connection_exist(self, departure_station_code_list, arrival_station_code_list):
        "checks if there is any flight between two airports lists"

        for departure_station_code in departure_station_code_list:
            for arrival_station_code in arrival_station_code_list:
                if self.does_connection_exist(departure_station_code, arrival_station_code):
                    return [departure_station_code, arrival_station_code]
        return None