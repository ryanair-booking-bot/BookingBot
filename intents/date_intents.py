"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date
from utils.constants import constants


#TODO: Do you need a return ticket?
#TODO: Choosing flight from the list
#TODO: Listing flights when user would say e.g "this week" instead of the day

def convert_date_to_database_format(the_date):
    "From YYYY-MM-DD (datetime.date) to string M/D/YYYY (month and day can be 1 or 2 digits)"
    return str(the_date.month) + '/' + str(the_date.day) + '/' + str(the_date.year)

def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()
	
	def list_flights(flights_at_date):
		"List flights with departure and arrival time"
		
			
			
		if len(flights_at_date) == 1:
			"There is only one flight at date"
			found_flights = render_template('foundFlight').format(		\
								session.attributes[constants.DEPARTURE_CITY],		\
								session.attributes[constants.DESTINATION_CITY], 	\
								session.attributes[constants.DEPARTURE_DATE],		\
								flights_at_date[0][5].split()[1])
			return question(found_flights)
		else:
			"There are multiple flights at date"
			found_flights = render_template('foundFlightsBeginning').format(		\
								session.attributes[constants.DEPARTURE_CITY], 				\
								session.attributes[constants.DESTINATION_CITY], 				\
								session.attributes[constants.DEPARTURE_DATE]) + " "
    			# "List hours of flights"
				# for flight in flights_at_date:
				# # TODO: check if the arrival is the next day, inform about it 
				# 	departure_hour = flight[5].split()[1]
				# 	arrival_hour = flight[6].split()[1]
				# 	found_flights += render_template('foundFlightsMiddle').format(		\
				# 					departure_hour, arrival_hour) + " "
						
			found_flights += render_template('foundFlightsEnd')				
			return question(found_flights) 



	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):
		departure_date = str(the_date)

		departure_date_is_set = departure_date
	
	   	if departure_date_is_set:
			
			flights_at_date = (database.get_flights(					 \
						session.attributes[constants.DEPARTURE_CITY],     		 \
						session.attributes[constants.DESTINATION_CITY],	 		 \
						convert_date_to_database_format(the_date)))		
			
			if flights_at_date:
				"There is one or more flights at date"
				session.attributes[constants.DEPARTURE_DATE] = departure_date

				return list_flights(flights_at_date)

			else:
				"There is no flight at date. Suggest flights near the date"
				session.attributes[constants.DEPARTURE_DATE] = None

				return statement(render_template('noSuchFlightAtDate').format(	\
							session.attributes[constants.DEPARTURE_CITY],     		 	\
							session.attributes[constants.DESTINATION_CITY],				\
							session.attributes[constants.DEPARTURE_DATE]))
		else:
			pass

def go_to_summary():
    "Ask For Seats Amount"
    return question(render_template('askForSeatsAmount')) 

	#@ask.intent("AlternativeDateIntent")
	#def alternative_date():
