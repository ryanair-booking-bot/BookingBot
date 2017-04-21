""
"This module handle time intents"
""#pylint: disable = unused - variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
from datetime import *
from date_intents import list_flights
import time as _time

#TODO: if flight is at 15:30, but user say 15:00 ask "Do you mean flight at 15:30. Please confirm"
#TODO: if single flight, confirmation could be yes (now it's only "(...) at {hour}") and skipping confirmation
#TODO: handle all no's answers and alternative dates

def handle_time_intents(ask):
    "Time intents handler"
    result = "Handling time intent"
    print result
    database = Database.Instance()

    def list_flights_short(time_one, opt="before", time_two=0):
        "List flight in (opt values) before, after, between given hour(s)"
        
        shorten_flights_list = constants.SHORTEN_FLIGHTS_LIST in session.attributes
        departure_date_is_set = constants.DEPARTURE_DATE in session.attributes

        #tests
        if constants.TESTS: 
            print "in list_flights_short (before, after, between handling)"
            print "time_one: ", time_one
            print "time_two: ", time_two

        if departure_date_is_set and shorten_flights_list:
            "If there were mulitiple flights at date, list" \
            "constants.LISTED_FLIGHTS_NUMBER flights after given hour"

            flights_list_shorten = []
            for flight in database.flights_at_date:

                flight_departure_time = datetime.strptime(flight[5].split()[1], '%H:%M').time()
                
                #tests
                if constants.TESTS:
                    print "flight_departure_time: ", flight_departure_time

                if opt == "before":
                    if time_one >= flight_departure_time:
                        flights_list_shorten.append(flight)
                elif opt == "after":
                     if time_one <= flight_departure_time:
                        flights_list_shorten.append(flight)
                elif opt == "between":
                    if time_two:
                        if flight_departure_time >= time_one and flight_departure_time <= time_two:
                            flights_list_shorten.append(flight)
                    else:
                        print "Between option requires two time arguments"

                if len(flights_list_shorten) == constants.LISTED_FLIGHTS_NUMBER:
                    break
        session.attributes[constants.SHORTEN_FLIGHTS_LIST] = None
        return list_flights(flights_list_shorten)


    """If there is more than constants.LISTED_FLIGHTS_NUMBER to list, user need to specify time"""
    @ask.intent("FlightsBeforeHourIntent", convert = {'the_time': 'time'})
    def list_flights_before_hour(the_time):
        "e.g 'i want to fly before nine o'clock' or 'before nine o'clock"
        return list_flights_short(the_time)

    @ask.intent("FlightsAfterHourIntent", convert = {'the_time': 'time'})
    def list_flights_after_hour(the_time):
        "e.g 'i want to fly after nine o'clock' or 'after nine o'clock"
        return list_flights_short(the_time, "after")

    @ask.intent("FlightsBetweenHoursIntent", convert = {'time_one': 'time', 'time_two': 'time'})
    def list_flights_between_hours(time_one, time_two):
        "e.g 'i want to fly between nine and sixteen' or 'between nine and sixteen"
        return list_flights_short(time_one, "between", time_two)
    


    @ask.intent("ChooseFlightIntent", convert = {'departure_time': 'time'})
    def choose_flight(departure_time):
        " After listing flights - user chooses the flight time e.g. "     \
        " 'I want to fly at 12:30' or 'at 12:30'. If time isn't exact or" \
        " doesn't match ask to repeat it"

        departure_date_is_set = constants.DEPARTURE_DATE in session.attributes
        return_date_is_set = constants.RETURN_DATE in session.attributes
        
        departure_time_is_set = constants.DEPARTURE_TIME in session.attributes
        return_time_is_set = constants.RETURN_TIME in session.attributes
        shorten_flights_list = constants.SHORTEN_FLIGHTS_LIST in session.attributes
       
        
        if shorten_flights_list is not None:
            "Checks if flight at given hour exist, if so ask for confirmation"
            for flight in database.flights_at_date:
               
                flight_departure_time = datetime.strptime(flight[5].split()[1], '%H:%M').time()

                if departure_time == flight_departure_time:
                    if return_date_is_set:
                        session.attributes[constants.RETURN_TIME] = str(departure_time)
                    elif departure_date_is_set:
                        session.attributes[constants.DEPARTURE_TIME] = str(departure_time)
            
            if return_date_is_set:
                return_time_is_set = constants.RETURN_TIME in session.attributes
            elif departure_date_is_set:
                departure_time_is_set = constants.DEPARTURE_TIME in session.attributes
            
        if departure_time_is_set:
            "Confirmation of date and time"
            return question(render_template('flightTimeChosen').format(             \
                                session.attributes[constants.DEPARTURE_DATE],       \
                                session.attributes[constants.DEPARTURE_TIME]))      \
                                .reprompt(render_template('flightTimeChosen'))
        elif return_time_is_set:
            "Confirmation of date and time - return ticket"
            return question(render_template('flightTimeChosen').format(             \
                                session.attributes[constants.RETURN_DATE],          \
                                session.attributes[constants.RETURN_TIME]))         \
                                .reprompt(render_template('flightTimeChosen'))
        else :
            "No flight at given time, ask to choose valid time"
            return question(render_template('askToRepeatTime').format(str(departure_time))) \
                .reprompt(render_template('didntUnderstandTime'))
