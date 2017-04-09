"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants




def handle_moreinfo_intents(ask):
    "Moreinfo intents handler"

    @ask.intent("HowManySeatsToBook")
    def how_many_seats_to_book(number):
        "Receives number of passangers"

        if number is None:
            return question(question(render_template('askToRepeatAmount')))

        session.attributes[constants.PASSENGERS_NO] = number
        return question(render_template('askForSeat'))


def response_seat_reservation(should_reserve_seats):
    "Moreinfo intents handler"
    if should_reserve_seats is None:
        return question(render_template('askToRepeatAmount'))

    else:
        session.attributes[constants.SEAT_RESERVATION] = should_reserve_seats
        return question(render_template('askForInsurance'))

def response_insurance_reservation(should_reserve_insurance):
    "Moreinfo intents handler"
    if should_reserve_insurance is None:
        return question(render_template('askToRepeatInsurance'))

    else:
        session.attributes[constants.INSURANCE] = should_reserve_insurance
        return show_flight_summary()


def ask_for_insurance():
    "Moreinfo intents handler"
    return question(render_template('askForInsurance'))

def show_flight_summary():
    "Moreinfo intents handler"
    return question(render_template('saySummaryAndConfirm'))

def response_booking_confirmation(customer_confirms):
    "Moreinfo intents handler"
    if customer_confirms is None:
        return question(render_template('askForLastConfirmation'))
    elif customer_confirms:
        return statement(render_template('bookingDone'))
    else:
        return statement(render_template('bookingCancelled'))


