"""This module handle place intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
import random

def handle_moreinfo_intents(ask, sup):
    "Moreinfo intents handler"

    @ask.intent("HowManySeatsToBook")
    @sup.guide
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

def show_booking_outcome(value):
    "x"
    if value is True:
        return statement(render_template('bookingDone'))
    else:
        return statement(render_template('bookingCancelled'))

def show_flight_summary():
    "Moreinfo intents handler"
    session.attributes[constants.WILL_CONFIRM_BOOKING] = True
    response_date_and_place = render_template('saySummaryAndConfirm').format(   \
                                 session.attributes[constants.DEPARTURE_DATE],  \
                                session.attributes[constants.DEPARTURE_CITY],   \
                                session.attributes[constants.DESTINATION_CITY])

    passenger_number = int(session.attributes[constants.PASSENGERS_NO])
    response_extras = render_template("saySummaryAndConfirmIncludes").format(passenger_number)

    if passenger_number > 1:
        response_extras += "s"

    if session.attributes[constants.SEAT_RESERVATION]:
        response_extras += ", "
        response_extras += render_template('saySummaryAndConfirmSeatReservation')

    if session.attributes[constants.INSURANCE]:
        response_extras += ", " + \
        render_template('saySummaryAndConfirmInsurance')

    response_extras += ". "
    response_price = render_template("saySummaryAndConfirmTotalPrice").format(calculate_price())
    response_confirm = render_template("saySummaryAndConfirmDoYouConfirm")

    return question(response_date_and_place+response_extras+response_price+response_confirm)

def response_booking_confirmation(customer_confirms):
    "Moreinfo intents handler"
    if customer_confirms is None:
        return question(render_template('askForLastConfirmation'))
    elif customer_confirms:
        return statement(render_template('bookingDone'))
    else:
        return statement(render_template('bookingCancelled'))


def calculate_price():
    "Moreinfo intents handler"
    full_price = 0
    passenger_number = int(session.attributes[constants.PASSENGERS_NO])

    if session.attributes[constants.SEAT_RESERVATION]:
        full_price += int(constants.SEAT_PRICE) * passenger_number

    if session.attributes[constants.INSURANCE]:
        full_price += int(constants.INSURANCE_PRICE) * passenger_number

    price_of_flight = passenger_number * random.randint(constants.FLIGHT_MIN_PRICE, \
                                         constants.FLIGHT_MAX_PRICE)

    full_price += price_of_flight
    return full_price

    