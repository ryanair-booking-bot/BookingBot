"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants

def handle_place_intents(ask, sup):
    "Place intents handler"

    database = Database.Instance()

    def start_searching_for_flight():
        "Finds a flight and decides if can proceed"

        if database.do_connections_exist(
                session.attributes[constants.DEPARTURE_CITY],
                session.attributes[constants.DESTINATION_CITY]):
            return question(
                render_template(
                    'destinationAndDepartureCollected').format(
                        session.attributes[constants.DEPARTURE_CITY],
                        session.attributes[constants.DESTINATION_CITY]))
        else:
            "If there is no flight connection start booking again"
            sup.move_to_step('booking_choice')
        
            return question(
                render_template('noFlightConnection').format(
                    session.attributes[constants.DEPARTURE_CITY],
                    session.attributes[constants.DESTINATION_CITY]))

    @ask.intent("PlaceIntent")
    @sup.guide
    def place(name):
        "If user says just the name of the city. Eg.'London'. " \
        "Then we need to check what info he already passed"
        destination_is_set = constants.DESTINATION_CITY in session.attributes

        if destination_is_set:
            # checks departure
            if database.does_place_exist(name):
                session.attributes[constants.DEPARTURE_CITY] = name
                return start_searching_for_flight()
            return sup.reprompt_error(
                render_template('noSuchDeaprturePlace_ChooseAnother').format(name))

        else:
            # checks destination
            if database.does_place_exist(name):
                session.attributes[constants.DESTINATION_CITY] = name
                return question(render_template("askForDeparturePlace"))
            else:
                return sup.reprompt_error(
                    render_template('noSuchDestinationPlace_ChooseAnother').format(name))

    @ask.intent("DestinationPlaceIntent")
    @sup.guide
    def destination_place(name):
        "Receives destination place. Eg. 'I want to go to London' or 'to London'." \
        " So we need to ask for the departure city"

        if database.does_place_exist(name):
            session.attributes[constants.DESTINATION_CITY] = name
            return question(render_template("askForDeparturePlace"))

        else:
            return sup.reprompt_error(
                render_template('noSuchDestination').format(name))

    @ask.intent("DeparturePlaceIntent")
    @sup.guide
    def departure_place(name):
        "Receives departure place       Eg. 'from London' "

        if database.does_place_exist(name):
            session.attributes[constants.DEPARTURE_CITY] = name
            return start_searching_for_flight()
        else:
            return sup.reprompt_error(
                render_template('noSuchDeparture').format(name))
