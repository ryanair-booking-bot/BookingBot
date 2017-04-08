"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database

DEPARTURE_CITY = "DEPARTURE_CITY"
DESTINATION_CITY = "DESTINATION_CITY"


# database = Database.Instance()

# def connections_between_cities(departure_city_name, destination_city_name):
#     "Returns list of airport codes if true, otherwise None"
#     dep_codes = database.get_airport_codes(departure_city_name)
#     des_codes = database.get_airport_codes(destination_city_name)
#     return database.does_any_connection_exist(dep_codes, des_codes)


def handle_place_intents(ask):
    "Place intents handler"

    database = Database.Instance()

    def start_searching_for_flight():
        "Finds a flight and decides if can proceed"

        if database.do_connections_exist(
                session.attributes[DEPARTURE_CITY],
                session.attributes[DESTINATION_CITY]):
            return question(
                render_template(
                    'destinationAndDepartureCollected').format(
                    session.attributes[DEPARTURE_CITY],
                    session.attributes[DESTINATION_CITY]))
        else:
            return statement(
                render_template('noFlightConnection').format(
                    session.attributes[DEPARTURE_CITY],
                    session.attributes[DESTINATION_CITY]))

    @ask.intent("PlaceIntent")
    def place(name):
        "If user says just the name of the city. Eg.'London'. " \
        "Then we need to check what info he already passed"
        destination_is_set = DESTINATION_CITY in session.attributes

        if destination_is_set:
            # checks departure
            if database.does_place_exist(name):
                session.attributes[DEPARTURE_CITY] = name
                return start_searching_for_flight()
            return question(render_template('noSuchDeaprturePlace_ChooseAnother').format(name))

        else:
            # checks destination
            if database.does_place_exist(name):
                session.attributes[DESTINATION_CITY] = name
                return question(render_template("askForDeparturePlace"))
            else:
                return question(render_template('noSuchDestinationPlace_ChooseAnother').format(name))

    @ask.intent("DestinationPlaceIntent")
    def detination_place(name):
        "Receives destination place. Eg. 'I want to go to London' or 'to London'." \
        " So we need to ask for the departure city"

        if database.does_place_exist(name):
            session.attributes[DESTINATION_CITY] = name
            msg = render_template("askForDeparturePlace")
            return question(msg)

        else:
            msg = render_template('noSuchDestination').format(name)
            return statement(msg)

    @ask.intent("DeparturePlaceIntent")
    def departure_place(name):
        "Receives departure place       Eg. 'from London' "

        if database.does_place_exist(name):
            session.attributes[DEPARTURE_CITY] = name
            return start_searching_for_flight()
        else:
            msg = render_template('noSuchDestination').format(name)
            return statement(msg)
