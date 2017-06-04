"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from utils.constants import constants
from intents import moreinfo_intents
from intents import date_intents
from intents import time_intents

def forward_yes_no(sup, value):
    "Forwards bool value"
    if constants.DEPARTURE_DATE in session.attributes:
        "Answer for 'Would you like to book one of these (flights)?'"
        if constants.DEPARTURE_TIME in session.attributes:
            "Answer for 'Flight on {} at {}. Are you sure?'"
            if constants.PASSENGERS_NO in session.attributes:
                "Answer for 'Do you want to choose a seat for ten euros?'"
                if constants.SEAT_RESERVATION in session.attributes:
                    "Answer for 'Do you want to book insurance?'"
                    if constants.INSURANCE in session.attributes:
                        "Booking confirmation"
                        if constants.WILL_CONFIRM_BOOKING in session.attributes:
                            "Booking outcome"
                            return moreinfo_intents.show_booking_outcome(value)
                    
                        return moreinfo_intents.show_flight_summary()
                
                    return moreinfo_intents.response_insurance_reservation(value)
            
                return moreinfo_intents.response_seat_reservation(value)
        
            return time_intents.flight_confirmation(sup, value)

        return date_intents.flights_choosing_confirmation(sup, value)

def handle_yesno_intents(ask, sup):
    "Moreinfo intents handler"

    @ask.intent("AMAZON.YesIntent")
    @sup.guide
    def received_yes():
        "Forwards bool value"
        return forward_yes_no(sup, True)

    @ask.intent("AMAZON.NoIntent")
    @sup.guide
    def received_no():
        "Forwards bool value"
        return forward_yes_no(sup, False)


