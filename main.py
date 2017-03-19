"""This module does blah blah."""

import logging


from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import database

DEPARTURE_CITY = "DEPARTURE_CITY"
DESTINATION_CITY = "DESTINATION_CITY"


app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


database = database.Database("filename")


@ask.launch
def new_booking():
    "On the app launch"

    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("PlaceIntend")
def place(name):
    "If user says just name of the city. Eg.'London' or 'Warsaw' "

    destination_isset = DESTINATION_CITY in session.attributes

    if destination_isset:
        if database.does_place_exist(name):
            session.attributes[DEPARTURE_CITY] = name
            return statement(
                render_template(                                    \
                    'destinationAndDepartureCollected').format(     \
                    session.attributes[DEPARTURE_CITY],             \
                    session.attributes[DESTINATION_CITY]))
        return statement(render_template('noSuchDestination').format(name))


    else:
        if database.does_place_exist(name):
            session.attributes[DESTINATION_CITY] = name
            return question(render_template("askForDeparturePlace"))
        else:
            return statement(render_template('noSuchDestination').format(name))



@ask.intent("DestinationPlaceIntend")
def detination_place(name):
    "Receives destination place         Eg. 'I want to go to London' or 'to London' "

    if database.does_place_exist(name):
        session.attributes[DESTINATION_CITY] = name
        msg = render_template("askForDeparturePlace")
        return question(msg)

    else:
        msg = render_template('noSuchDestination').format(name)
    return statement(msg)

@ask.intent("DeparturePlaceIntend")
def departure_place(name):
    "Receives departure place       Eg. 'from London' "

    if database.does_place_exist(name):
        session.attributes[DEPARTURE_CITY] = name
        return statement(
            render_template(                                \
            'destinationAndDepartureCollected').format(     \
            session.attributes[DEPARTURE_CITY],             \
            session.attributes[DESTINATION_CITY]))
    else:
        msg = render_template('noSuchDestination').format(name)
    return statement(msg)


@ask.intent("YesIntent")
def next_round():
    "xx"

    numbers = [randint(0, 9) for _ in range(3)]
    round_msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    "xx"

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:
        msg = render_template('win')

    else:
        msg = render_template('lose')

    return statement(msg)



if __name__ == '__main__':
    app.run(debug=True)
