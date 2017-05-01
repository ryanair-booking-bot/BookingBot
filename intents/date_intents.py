"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date
from utils.constants import constants
import time as _time

global flights_at_date
flights_at_date = []
database = Database.Instance()

def handle_date_intents(ask, sup):
	"Date intents handler"
	result = "Handling date intent"
	print result
	

	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	@sup.guide
	def departure_date(the_date):
		departure_date = str(the_date)

		departure_date_is_set = departure_date
	
	   	if departure_date_is_set:
			
			find_flights(session.attributes[constants.DEPARTURE_CITY], 		\
						session.attributes[constants.DESTINATION_CITY],		\
																the_date)		

			print "Flights at date: ", flights_at_date
			
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
def find_flights(departure_city, destination_city, the_date):
	global flights_at_date
	flights_at_date = (database.get_flights(								\
						departure_city, destination_city, 					\
						'{d.month}/{d.day}/{d.year}'.format(d=the_date)))
	return flights_at_date

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
								len(_flights),												\
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


def init_confirmation(customer_confirms):

	if constants.DEPARTURE_TIME in session.attributes:
		if customer_confirms:
			"Ask For Seats Amount"
			return question(render_template('askForSeatsAmount'))
		else:
			"Go through flight booking again"
			return statement(render_template('chooseFlightAgain')) 
	else:
		if customer_confirms:
			"Ask to choose flight time"
			return question(render_template('askForFlightTime'))
		else:
			"Go through flight booking again"
			return statement(render_template('chooseFlightAgain'))
