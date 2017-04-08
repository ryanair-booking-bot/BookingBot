"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from datetime import date

DEPARTURE_DATE = "DEPARTURE_DATE"
DEPARTURE_CITY = "DEPARTURE_CITY"
DESTINATION_CITY = "DESTINATION_CITY"

def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()
	
	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):

		
		session.attributes[DEPARTURE_DATE] = str(the_date)
		departure_date_is_set = DEPARTURE_DATE in session.attributes
	
	   	if departure_date_is_set:
			# Zapis do formatu bazy danych M/D/YYYY (miesiac i dzien moga byc jedna cyfra)
			the_date_str = str(the_date.month) + '/' + str(the_date.day) + '/' + str(the_date.year)	
			
			flights = (database.get_flights(			 \
				session.attributes[DEPARTURE_CITY],      \
				session.attributes[DESTINATION_CITY],	 \
				the_date_str))		# format w bazie jest inny niz amazon.date
			
			if flights:
				return statement(render_template('foundFlights').format(		\
					session.attributes[DEPARTURE_CITY], 						\
					session.attributes[DESTINATION_CITY],						\
					session.attributes[DEPARTURE_DATE]))
		
			return statement(render_template('noSuchFlightAtDate').format(		\
				session.attributes[DEPARTURE_DATE]))
		