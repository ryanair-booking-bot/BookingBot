"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from utils.constants import constants
from intents import moreinfo_intents
from intents import date_intents

#TODO: #CHECK after setting DEPARTURE_TIME its jumps over the 'askForSeatsAmount' to 'askForInsurance'. Why?

def forward_yes_no(value):
    "Forwards bool value"

    if constants.INSURANCE in session.attributes:
        return moreinfo_intents.show_flight_summary()

    elif constants.SEAT_RESERVATION in session.attributes:
        return moreinfo_intents.response_insurance_reservation(value)

    elif constants.PASSENGERS_NO:
        return moreinfo_intents.response_seat_reservation(value)
    
    elif constants.DEPARTURE_TIME in session.attributes:
        return question(render_template('askForSeatsAmount'))
    
    #TODO: #CHECK if there is no flight, DEPARTURE_DATE is set to None, should ask again for another date
    # Maybe we will solve this with setting ALTERNATIVE_FLIGHTS flag
    """elif (constants.DEPARTURE_CITY in session.attributes) and (constants.DESTINATION_CITY in session.attributes):
        return question(render_template('destinationAndDepartureCollected').format(         \
                                session.attributes[DEPARTURE_CITY],                         \
                                session.attributes[DESTINATION_CITY]))"""

def handle_yesno_intents(ask):
    "Moreinfo intents handler"

    @ask.intent("AMAZON.YesIntent")
    def received_yes():
        "Forwards bool value"
        return forward_yes_no(True)


    @ask.intent("AMAZON.NoIntent")
    def received_no():
        "Forwards bool value"
        return forward_yes_no(False)


