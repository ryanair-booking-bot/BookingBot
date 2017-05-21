"""This module handle booking intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
from date_intents import *

database = Database.Instance()

def handle_booking_intents(ask, sup):
    "Booking intents handler"

    @ask.intent("BookingIntent", convert={'departure_date': 'date'})
    @sup.guide
    def book(departure_city, destination_city, departure_date):
        "Finds a flight from departure_city to destiantion_city on departure_date"

        if not database.does_place_exist(departure_city):
            return sup.reprompt_error('noSuchDeparture').format(departure_city)

        if not database.does_place_exist(destination_city):
            return sup.reprompt_error('noSuchDestination').format(destination_city)

        if not database.do_connections_exist(departure_city, destination_city):
            return sup.reprompt_error(
                render_template('noFlightConnection').format(departure_city, destination_city)
            )
        session.attributes[constants.DEPARTURE_CITY] = departure_city
        session.attributes[constants.DESTINATION_CITY] = destination_city

        if not departure_date:
            "If no date given, asks for it"
            sup.move_to_step('departure_date_choice')
            return question(render_template('destinationAndDepartureCollected').format(
                  departure_city, destination_city
              ))

        flights = find_flights(departure_city, destination_city, departure_date)
        
        if flights is None:
            return question(render_template('noSuchFlightAtDate').format(
                departure_city,
                destination_city,
                str(departure_date)
            ))
        else:
            session.attributes[constants.DEPARTURE_DATE] = str(departure_date)

            return list_flights(flights)
            
