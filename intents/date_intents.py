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
		flights = []
		flights.extend(database.get_flights(			 \
				 session.attributes[DEPARTURE_CITY],     \
				 session.attributes[DESTINATION_CITY],	 \
				 session.attributes[DEPARTURE_DATE]))
		if flights:
			return statement(render_template('foundFlights').format(	\
			session.attributes[DEPARTURE_CITY], 						\
			session.attributes[DESTINATION_CITY],						\
			session.attributes[DEPARTURE_DATE]))
			
		return statement(render_template('noSuchFlightsAtDate').format(the_date))
		