"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date
from utils.constants import constants
import time as _time

#TODO: Do you need a return ticket?
#TODO: Choosing flight from the list
#TODO: Listing flights when user would say e.g "this week" instead of the day


def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()


	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):
		departure_date = str(the_date)

		departure_date_is_set = departure_date
	
	   	if departure_date_is_set:
			
			flights_at_date = (database.get_flights(							 \
						session.attributes[constants.DEPARTURE_CITY],     		 \
						session.attributes[constants.DESTINATION_CITY],	 		 \
						'{d.month}/{d.day}/{d.year}'.format(d=the_date)))		
			
			if flights_at_date:
				"There is one or more flights at date"
				session.attributes[constants.DEPARTURE_DATE] = departure_date

				return list_flights(flights_at_date)

			else:
				"There is no flight at date. Suggest flights near the date"
				session.attributes[constants.DEPARTURE_DATE] = None

				return statement(render_template('noSuchFlightAtDate').format(			\
							session.attributes[constants.DEPARTURE_CITY],     		 	\
							session.attributes[constants.DESTINATION_CITY],				\
							session.attributes[constants.DEPARTURE_DATE]))
		else:
			pass

def list_flights(_flights):
		"List flights with departure and arrival time"

		"Time formating - Alexa pronounce time correctly in hms12 format"
		departure_time = _time.strftime('%I:%M %p', _time.strptime(_flights[0][5].split()[1], '%H:%M'))
		arrival_time = _time.strftime('%I:%M %p', _time.strptime(_flights[0][6].split()[1], '%H:%M'))
			
		if len(_flights) == 1:
			"There is only one flight at date"
			found_flights = render_template('foundFlight').format(					\
								session.attributes[constants.DEPARTURE_CITY],		\
								session.attributes[constants.DESTINATION_CITY], 	\
								session.attributes[constants.DEPARTURE_DATE],		\
								_flights[0][5].split()[1])
			return question(found_flights)
		else:
			"There are multiple flights at date"
			found_flights = render_template('foundFlightsBeginning').format(
								len(_flights),															\
								session.attributes[constants.DEPARTURE_CITY], 				\
								session.attributes[constants.DESTINATION_CITY], 			\
								session.attributes[constants.DEPARTURE_DATE]) + " "
    				
			"List hours of flights"
			for flight in _flights:
				
				"Time formating - Alexa pronounce time correctly in hms12 format"
				departure_time = _time.strftime('%I:%M %p', _time.strptime(flight[5].split()[1], '%H:%M'))
				arrival_time = _time.strftime('%I:%M %p', _time.strptime(flight[6].split()[1], '%H:%M'))
				 	
				found_flights += render_template('foundFlightsMiddle').format(		\
									departure_time, arrival_time) + " "
						
			found_flights += render_template('foundFlightsEnd')		

			return question(found_flights) 

def go_to_summary():
    "Ask For Seats Amount"
    return question(render_template('askForSeatsAmount')) 

