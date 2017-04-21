"""This module does blah blah."""
# pylint: disable=too-few-public-methods
# pylint: disable=unused-variable

import pandas as pd
from utils.decorators.singleton import Singleton
@Singleton
class Database(object):
    "Shared connection to the database"
    
    def __init__(self):
        self.flights = pd.read_csv('./models/database.csv')
        global flights_at_date   #TODO: #CHECK is this the best place to declare it?
        flights_at_date = []
    def does_place_exist(self, destination):
        "Checks if the city has an airport"

        departures = self.flights.loc[lambda df: df.DepartureCity == destination,
                                      lambda df: ['DepartureCity']]
        arrivals = self.flights.loc[lambda df: df.ArrivalCity == destination,
                                    lambda df: ['ArrivalCity']]

        if departures.empty and arrivals.empty:
            return False
        return True

    def get_flights(self, departure_city, arrival_city, date):
        "Get flights from departure_city to _arrival_city on specific date"

        result = self.flights.loc[lambda df: df.DepartureCity == departure_city, :] \
                     .loc[lambda df: df.ArrivalCity == arrival_city, :]             \
                     .loc[lambda df: df.DepartureDate == date, :]
        if result.empty:
            return None             
        return result.values.tolist()

    def do_connections_exist(self, departure_city, arrival_city):
        "Checks if there is any flight between two airports"

        connections = self.flights.loc[lambda df: df.DepartureCity == departure_city, :] \
                          .loc[lambda df: df.ArrivalCity == arrival_city, :]
        if connections.empty:
            return False
        return True
