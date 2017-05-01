"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from utils.constants import constants
from intents import moreinfo_intents
from intents import date_intents

def forward_yes_no(value):
    "Forwards bool value"

    if constants.WILL_CONFIRM_BOOKING in session.attributes:
        return moreinfo_intents.show_booking_outcome(value)

    elif constants.INSURANCE in session.attributes:
        return moreinfo_intents.show_flight_summary()

    elif constants.SEAT_RESERVATION in session.attributes:
        return moreinfo_intents.response_insurance_reservation(value)

    elif constants.PASSENGERS_NO in session.attributes:
        return moreinfo_intents.response_seat_reservation(value)

    elif constants.DEPARTURE_TIME in session.attributes:
        return date_intents.init_confirmation(value)

    elif constants.DEPARTURE_DATE in session.attributes:
        return date_intents.init_confirmation(value)

def handle_yesno_intents(ask, sup):
    "Moreinfo intents handler"

    @ask.intent("AMAZON.YesIntent")
    @sup.guide
    def received_yes():
        "Forwards bool value"
        return forward_yes_no(True)

    @ask.intent("AMAZON.NoIntent")
    @sup.guide
    def received_no():
        "Forwards bool value"
        return forward_yes_no(False)


