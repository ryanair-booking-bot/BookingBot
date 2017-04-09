"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date

DEPARTURE_DATE = "DEPARTURE_DATE"
DEPARTURE_CITY = "DEPARTURE_CITY"
DESTINATION_CITY = "DESTINATION_CITY"

#TODO: Do you need a return ticket?
#TODO: Choosing flight from the list
#TODO: Listing flights when user would say e.g "this week" instead of the day

def convert_date_to_database_format(the_date):
	"From YYYY-MM-DD (datetime.date) to string M/D/YYYY (month and day can be 1 or 2 digits)"
	return (str(the_date.month) + '/' + str(the_date.day) + '/' + str(the_date.year))	

def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()
	
	def list_flights(flights_at_date):
		"List flights with departure and arrival time"
		if flights_at_date:
			print "Flights", flights_at_date
			
			
			if len(flights_at_date) == 1:
				"There is only one flight at date"
				found_flights = render_template('foundFlight').format(		\
									session.attributes[DEPARTURE_CITY],		\
									session.attributes[DESTINATION_CITY], 	\
									session.attributes[DEPARTURE_DATE],		\
									flights_at_date[0][5].split()[1])	
			else:
				"There are multiple flights at date"
				found_flights = render_template('foundFlightsBeginning').format(		\
									session.attributes[DEPARTURE_CITY], 				\
									session.attributes[DESTINATION_CITY], 				\
									session.attributes[DEPARTURE_DATE]) + " "
				"List hours of flights"
				for flight in flights_at_date:
				# TODO: check if the arrival is the next day, inform about it 
					departure_hour = flight[5].split()[1]
					arrival_hour = flight[6].split()[1]
					found_flights += render_template('foundFlightsMiddle').format(		\
									departure_hour, arrival_hour) + " "
						
				found_flights += render_template('foundFlightsEnd')
					
			return question(found_flights) 
		return None

	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):
		session.attributes[DEPARTURE_DATE] = str(the_date)
		departure_date_is_set = DEPARTURE_DATE in session.attributes
	
	   	if departure_date_is_set:

			flights_at_date = (database.get_flights(					 \
						session.attributes[DEPARTURE_CITY],     		 \
						session.attributes[DESTINATION_CITY],	 		 \
						convert_date_to_database_format(the_date)))		
			
			if flights_at_date:
				"There is one or more flights at date"
				return list_flights(flights_at_date)

			else:
				"There is no flight at date. Suggest flights near the date"
				#TODO: Suggest flights near the date
				#alternative_date = the_date
				#alternative_date.day -= 1


				return question(render_template('noSuchFlightAtDate').format(	\
							session.attributes[DEPARTURE_CITY],     		 	\
							session.attributes[DESTINATION_CITY],				\
							session.attributes[DEPARTURE_DATE]))
		else:
			pass

	#@ask.intent("AlternativeDateIntent")
	#def alternative_date():
