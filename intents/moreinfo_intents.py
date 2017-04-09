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
        return question(render_template('askForInsurance'))

