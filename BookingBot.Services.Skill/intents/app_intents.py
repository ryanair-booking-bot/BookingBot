"""This module handle app intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session


def handle_app_intents(ask, sup):
    "app intents handler"

    @ask.launch
    @sup.guide
    def new_booking():
        "On the app launch"
        welcome_msg = render_template('welcome')
        return question(welcome_msg)

    @ask.intent('AMAZON.HelpIntent')
    def help_user():
        context_help = sup.get_help()
        return question(context_help)
