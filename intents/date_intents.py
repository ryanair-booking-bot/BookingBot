"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date
from utils.constants import constants
import time 

database = Database.Instance()

def handle_date_intents(ask, sup):
	"Date intents handler"
	result = "Handling date intent"
	print result
	
	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	@sup.guide
	def departure_date(the_date):
		departure_date = str(the_date)
			
		flights_at_date = find_flights(session.attributes[constants.DEPARTURE_CITY], 		\
										session.attributes[constants.DESTINATION_CITY],		\
																			the_date)		
		session.attributes[constants.DEPARTURE_DATE] = departure_date
		
		if flights_at_date :
			"There is at least one flight at date"
			return list_flights(flights_at_date)

		else:
			"There is no flight at date. Suggest flights near the date"
			session.attributes[constants.DEPARTURE_DATE] = None

			return sup.reprompt_error(render_template('noSuchFlightAtDate').format(		\
							session.attributes[constants.DEPARTURE_CITY],     		 	\
							session.attributes[constants.DESTINATION_CITY],				\
							str(the_date)))
		

def find_flights(departure_city = None, destination_city = None, the_date = None):
	
	flights_at_date = []
	
	if departure_city and destination_city and the_date:
		"Finds flights from departure_city to _arrival_city on specific date" 	\
		"Saves their id's in current session"
		session.attributes[constants.FLIGHTS_ID] = None
		flights_at_date = (database.get_flights(departure_city, destination_city, \
											('{d.month}/{d.day}/{d.year}'.format(d=the_date))))
		if flights_at_date:
			flights_id = []
			for flight in flights_at_date:
				flights_id.append(flight[0]) 	

			session.attributes[constants.FLIGHTS_ID] = flights_id
	else:
		"If no arguments specified, finds flights from their id saved in current session"
		if constants.FLIGHTS_ID in session.attributes:
			flights_id = session.attributes[constants.FLIGHTS_ID]
		
			for f_id in flights_id:
				flights_at_date += database.get_single_flight(f_id)
		else:
			"There is no flights id saved in current session"
			return None
	return flights_at_date


def list_single_flight(flight):
	"List single flight with departure and arrival time"
	departure_time = time.strftime('%I:%M %p', time.strptime(flight[0][5].split()[1], '%H:%M'))
			
	found_flights = render_template('foundFlight').format(						\
							session.attributes[constants.DEPARTURE_CITY],		\
							session.attributes[constants.DESTINATION_CITY], 	\
							session.attributes[constants.DEPARTURE_DATE],		\
							flight[0][5].split()[1])
	return question(found_flights)

def list_flights(flights):

	if len(flights) == 1:
		"There is only one flight at date"
		return list_single_flight(flights)
	else:
		"There are multiple flights at date"
		found_flights = render_template('foundFlightsBeginning').format(
							len(flights),												\
							session.attributes[constants.DEPARTURE_CITY], 				\
							session.attributes[constants.DESTINATION_CITY], 			\
							session.attributes[constants.DEPARTURE_DATE]) + " "	
	
		for flight in flights:
			"List hours of flights"
			departure_time = time.strftime('%I:%M %p', time.strptime(flight[5].split()[1], '%H:%M'))
				 	
			found_flights += render_template('foundFlightsMiddle').format(		\
									departure_time) + " "
						
		found_flights += render_template('foundFlightsEnd')		
		return question(found_flights) 


def flights_choosing_confirmation(sup, customer_confirms):
	if customer_confirms:
		"Ask to choose flight time"
		return question(render_template('askForFlightTime'))
	else:
		"Go through flight booking again"
		sup.move_to_step('booking_choice')
		session.clear()
		return question(render_template('chooseFlightAgain'))
