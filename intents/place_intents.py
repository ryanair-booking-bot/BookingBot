"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database

DEPARTURE_CITY = "DEPARTURE_CITY"
DESTINATION_CITY = "DESTINATION_CITY"

def handle_place_intents(ask):
    "Place intents handler"
    database = Database.Instance()

    @ask.intent("PlaceIntent")
    def place(name):
        "If user says just name of the city. Eg.'London' or 'Warsaw' "

        destination_is_set = DESTINATION_CITY in session.attributes

        if destination_is_set:
            if database.does_place_exist(name):
                session.attributes[DEPARTURE_CITY] = name
                return statement(
                    render_template(                                    \
                        'destinationAndDepartureCollected').format(     \
                        session.attributes[DEPARTURE_CITY],             \
                        session.attributes[DESTINATION_CITY]))
            return statement(render_template('noSuchDestination').format(name))

        else:
            if database.does_place_exist(name):
                session.attributes[DESTINATION_CITY] = name
                return question(render_template("askForDeparturePlace"))
            else:
                return statement(render_template('noSuchDestination').format(name))

    @ask.intent("DestinationPlaceIntent")
    def detination_place(name):
        "Receives destination place         Eg. 'I want to go to London' or 'to London' "

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
            return statement(
                render_template(                                \
                'destinationAndDepartureCollected').format(     \
                session.attributes[DEPARTURE_CITY],             \
                session.attributes[DESTINATION_CITY]))
        else:
            msg = render_template('noSuchDestination').format(name)
            return statement(msg)
