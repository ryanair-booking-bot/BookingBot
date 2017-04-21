"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
from datetime import *
import time as _time


#TODO: Do you need a return ticket?
#TODO: Listing flights when user would say e.g "this week" instead of the day
#TODO: AlternativeDateIntent - there is no flight at date, 
# but we've got four options - there are flights day before and/or after or there are no flights at this days too
# noSuchFlightAtDate... templates
#TODO: checking if date is available (don't book historic flights), 
#TODO: checking if return ticket isn't earlier than first flight

def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()
	
	def convert_date_to_database_format(the_date):
		"From YYYY-MM-DD (datetime.date) to string M/D/YYYY (month and day can be 1 or 2 digits)"
		return (str(the_date.month) + '/' + str(the_date.day) + '/' + str(the_date.year))


	def find_flights_at_date(the_date, return_ticket=0):
		if not return_ticket:
			"Looking for flights at the_date"
			departure_city = session.attributes[constants.DEPARTURE_CITY]
			destination_city = session.attributes[constants.DESTINATION_CITY]
		else:
			"Looking for return ticket - cities from session are switched"
			departure_city = session.attributes[constants.DESTINATION_CITY]
			destination_city = session.attributes[constants.DEPARTURE_CITY]

		database.flights_at_date = (database.get_flights(						\
								departure_city, destination_city,	 		 	\
								convert_date_to_database_format(the_date)))	
		
		print "flights 1: ", database.flights_at_date
		return database.flights_at_date
		

	def alternative_date_check(the_date):
		"Day before and day after flights check"
		day_before_date = day_after_date = the_date
				
		day_before_date -= timedelta(days = 1)
		day_after_date += timedelta(days = 1)

		flights_day_before = find_flights_at_date(day_before_date)	
		flights_day_after = find_flights_at_date(day_after_date)

		if (flights_day_before or flights_day_after):
			"Suggest found flights day before and/or after"
			if (flights_day_before and flights_day_after):
				suggested_flights = "day before and day after"
			elif flights_day_before:
				suggested_flights = "day before"
			elif flights_day_after:
				suggested_flights = "day after"
					
			return question(render_template('noSuchFlightAtDateButAnother').format(					\
							session.attributes[constants.DEPARTURE_CITY],     		 				\
							session.attributes[constants.DESTINATION_CITY],							\
							str(the_date), suggested_flights))										\
							.reprompt(render_template('didntUnderstandThat'))
		else:
			"Ask to look for flight at another date"
			session.attributes[constants.DEPARTURE_DATE] = None
			return question(render_template('noSuchFlightAtDateNoAnother').format(					\
							session.attributes[constants.DEPARTURE_CITY],     					 	\
							session.attributes[constants.DESTINATION_CITY],							\
							str(the_date))).														\
							reprompt(render_template('didntUnderstandThat'))



	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):
		"Choosing departure date or return ticket date"

		if constants.RETURN_TICKET in session.attributes:
			"Return ticket date setting"
			session.attributes[constants.RETURN_DATE] = str(the_date)
			database.flights_at_date = find_flights_at_date(the_date, True)

		elif not (constants.DEPARTURE_DATE in session.attributes):
			"Departure date setting" 
			session.attributes[constants.DEPARTURE_DATE] = str(the_date)
			database.flights_at_date = find_flights_at_date(the_date)
		 
		if database.flights_at_date:
			"There is one or more flights at date. If five or less list all, otherwise ask to precize hour"
			if len(database.flights_at_date) <= constants.LISTED_FLIGHTS_NUMBER:
				return list_flights(database.flights_at_date)
			else:
				session.attributes[constants.SHORTEN_FLIGHTS_LIST] = True

				return question(render_template('precizeDepartureTime').format(			\
								len(database.flights_at_date),								\
								session.attributes[constants.DEPARTURE_DATE]))				\
								.reprompt(render_template('askToPrecizeAgain'))
		else:
			"There is no flight at date. Suggest flights near the date, if exist"
			return alternative_date_check(the_date)
		
		
def confirm_return_ticket(should_book_return_ticket):
	session.attributes[constants.RETURN_TICKET] = should_book_return_ticket
		
	if should_book_return_ticket is None:
		return question(render_template('askForSeatsAmount'))
	else:
		return question(render_template('askForReturnTicket'))

	
def list_flights(_flights): 
	"List flights with departure and arrival time"
		
	shorten_flights_list = constants.SHORTEN_FLIGHTS_LIST in session.attributes

	if _flights:
		"Time formating - Alexa pronounce time correctly in hms12 format"
		departure_time = _time.strftime('%I:%M %p', _time.strptime(_flights[0][5].split()[1], '%H:%M'))
		arrival_time = _time.strftime('%I:%M %p', _time.strptime(_flights[0][6].split()[1], '%H:%M'))
	
		if len(_flights) == 1:
			"There is only one flight at date"
			found_flights = render_template('foundFlight').format(						\
									session.attributes[constants.DEPARTURE_CITY],		\
									session.attributes[constants.DESTINATION_CITY], 	\
									session.attributes[constants.DEPARTURE_DATE],		\
									departure_time, arrival_time)	

		else:
			"There are multiple flights at date"
			found_flights = render_template('foundFlightsBeginning').format(					\
									len(_flights),												\
									session.attributes[constants.DEPARTURE_CITY], 				\
									session.attributes[constants.DESTINATION_CITY], 			\
									session.attributes[constants.DEPARTURE_DATE]) + " "

			"List hours of flights"
			for flight in _flights:
			# TODO: check if the arrival is the next day, inform about it 

				"Time formating - Alexa pronounce time correctly in hms12 format"
				departure_time = _time.strftime('%I:%M %p', _time.strptime(flight[5].split()[1], '%H:%M'))
				arrival_time = _time.strftime('%I:%M %p', _time.strptime(flight[6].split()[1], '%H:%M'))
					
				found_flights += render_template('foundFlightsMiddle').format(			\
													departure_time, arrival_time) + " "
						
			found_flights += render_template('foundFlightsEnd')
					
		return question(found_flights).reprompt(render_template('didntUnderstandTime')) 
	return None	