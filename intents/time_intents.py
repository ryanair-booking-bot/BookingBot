""
"This module handle time intents"
""#pylint: disable = unused - variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
from date_intents import *
from datetime import *
import time as _time

def handle_time_intents(ask, sup):   
    "Time intents handler"
    result = "Handling time intent"
    print result
    database = Database.Instance()
    
    @ask.intent("ChooseFlightIntent", convert = {'departure_time': 'time'})
    @sup.guide
    def choose_flight(departure_time):
        " After listing flights - user chooses the flight time e.g. "     \
        " 'I want to fly at 12:30' or 'at 12:30'. If time isn't exact or" \
        " doesn't match ask to repeat it"

        departure_date_is_set = constants.DEPARTURE_DATE in session.attributes
        departure_time_is_set = constants.DEPARTURE_TIME in session.attributes
       
        "Checks if flight at given hour exist, if so ask for confirmation"
        flights_at_date = find_flights()

        for flight in flights_at_date:       
            flight_departure_time = datetime.strptime(flight[5].split()[1], '%H:%M').time()

            if departure_time == flight_departure_time:
                if departure_date_is_set:
                    session.attributes[constants.DEPARTURE_TIME] = str(departure_time)
            
        if departure_date_is_set:
            departure_time_is_set = constants.DEPARTURE_TIME in session.attributes

        if departure_time_is_set:
            "Confirmation of date and time"
            return question(render_template('flightTimeChosen').format(             \
                                session.attributes[constants.DEPARTURE_DATE],       \
                                session.attributes[constants.DEPARTURE_TIME]))      \
                                .reprompt(render_template('flightTimeChosen'))
        else :
            "No flight at given time, ask to choose valid time"
            return question(render_template('askToRepeatTime').format(str(departure_time))) \
                .reprompt(render_template('didntUnderstandTime'))
