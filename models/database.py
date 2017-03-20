"""This module does blah blah."""
# pylint: disable=too-few-public-methods

class Database(object):
    "Shared connection to the database"

    def __init__(self, filename):
        self.filename = filename
        self.cities = ["Warsaw", "Manchester", "Berlin"]

    def does_place_exist(self, destination_name):
        "Checks if place exists"
        if destination_name in self.cities:
            return True
        return False
