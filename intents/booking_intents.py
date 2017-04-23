"""This module handle booking intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants

database = Database.Instance()

def handle_booking_intents(ask):
    "Booking intents handler"

    @ask.intent("BookingIntent", convert={'departure_date': 'date'})
    def book(departure_city, destination_city, departure_date):
        "Finds a flight from departure_city to destiantion_city on departure_date"

        if not database.does_place_exist(departure_city):
            return statement(render_template('noSuchDeparture').format(departure_city))

        if not database.does_place_exist(destination_city):
            return statement(render_template('noSuchDestination').format(destination_city))

        if not database.do_connections_exist(departure_city, destination_city):
            return statement(
                render_template('noFlightConnection').format(departure_city, destination_city)
            )

        flights = database.get_flights(
            departure_city,
            destination_city,
            '{d.month}/{d.day}/{d.year}'.format(d=departure_date)
        )
        if flights is None:
            return question(render_template('noSuchFlightAtDate').format(
                departure_city,
                destination_city,
                str(departure_date)
            ))
        else:
            
            session.attributes[constants.DEPARTURE_CITY] = departure_city
            session.attributes[constants.DESTINATION_CITY] = destination_city
            session.attributes[constants.DEPARTURE_DATE] = str(departure_date)

            if len(flights) == 1:

                return question(render_template('foundFlight').format(
                    departure_city,
                    destination_city,
                    str(departure_date)
                ))
            else:
                return question(
                    render_template('foundFlightsBeginning').format(
                        len(flights),
                        departure_city,
                        destination_city,
                        str(departure_date)
                    ) + render_template('foundFlightsEnd')
                )
