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
        self.flights = pd.read_csv('./models/database.csv')

    def does_place_exist(self, destination):
        "Checks if the city has an airport"

        if self.flights.loc[lambda df: df == destination, lambda df: ['DepartureCity', 'ArrivalCity']].empty:
            return False
        return True

    def get_flights(self, departure_city, arrival_city, date):
        "Get flights from departure_city to _arrival_city on specific date"

        result = self.flights.loc[lambda df: df.DepartureCity == departure_city, :] \
                     .loc[lambda df: df.ArrivalCity == arrival_city, :]             \
                     .loc[lambda df: df.DepartureDate == date, :]

        return result

    def does_connections_exist(self, departure_city, arrival_city):
        "Checks if there is any flight between two airports"

        connections = self.flights.loc[lambda df: df.DepartureCity == departure_city, :] \
                          .loc[lambda df: df.ArrivalCity == arrival_city, :]
        if connections.empty:
            return False
        return True
