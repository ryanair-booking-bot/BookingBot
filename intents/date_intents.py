"""This module handle date intents"""
# pylint: disable=unused-variable

from flask import render_template
from flask_ask import statement, question, session
from models.database import Database
from utils.constants import constants
from datetime import *
import time as _time


#TODO: Do you need a return ticket?
#TODO: if more than 5 flights at given date, ask user to precize the hour 
#TODO: Choosing flight from the list
#TODO: Listing flights when user would say e.g "this week" instead of the day
#TODO: AlternativeDateIntent - there is no flight at date, 
# but we've got four options - there are flights day before and/or after or there are no flights at this days too
# noSuchFlight... templates


def handle_date_intents(ask):
	"Date intents handler"
	result = "Handling date intent"
	print result
	database = Database.Instance()
	global flights_at_date
	
	def convert_date_to_database_format(the_date):
		"From YYYY-MM-DD (datetime.date) to string M/D/YYYY (month and day can be 1 or 2 digits)"
		return (str(the_date.month) + '/' + str(the_date.day) + '/' + str(the_date.year))

	def find_flights_at_date(the_date):
		flights_at_date = (database.get_flights(								 \
						session.attributes[constants.DEPARTURE_CITY],     		 \
						session.attributes[constants.DESTINATION_CITY],	 		 \
						convert_date_to_database_format(the_date)))	
		return flights_at_date
		

	def list_flights(flights_at_date, above_hour = None): # above_hour jeszcze nie dziala
		"List flights with departure and arrival time, if above_hour is set it list 5 flights above it"
		
		if flights_at_date:
			print "Flights1", flights_at_date 		#tests
			"Time formating"
			departure_time = _time.strftime('%I:%M %p', _time.strptime(flights_at_date[0][5].split()[1], '%H:%M'))
			arrival_time = _time.strftime('%I:%M %p', _time.strptime(flights_at_date[0][6].split()[1], '%H:%M'))
	
			if len(flights_at_date) == 1:
				"There is only one flight at date"
				found_flights = render_template('foundFlight').format(					\
									session.attributes[constants.DEPARTURE_CITY],		\
									session.attributes[constants.DESTINATION_CITY], 	\
									session.attributes[constants.DEPARTURE_DATE],		\
									departure_time, arrival_time)	

			else:
				"There are multiple flights at date"
				found_flights = render_template('foundFlightsBeginning').format(				\
									session.attributes[constants.DEPARTURE_CITY], 				\
									session.attributes[constants.DESTINATION_CITY], 			\
									session.attributes[constants.DEPARTURE_DATE]) + " "
				"List hours of flights"
				for flight in flights_at_date:
				# TODO: check if the arrival is the next day, inform about it 

					"Time formating - Alexa understands time in hms12 format"
					departure_time = _time.strftime('%I:%M %p', _time.strptime(flight[5].split()[1], '%H:%M'))
					arrival_time = _time.strftime('%I:%M %p', _time.strptime(flight[6].split()[1], '%H:%M'))
					
					if above_hour: # to jeszcze nic nie robi :)
						d_time_tmp = _time.strptime(flight[5].split()[1], '%H:%M')
						above_hour = _time.mktime(above_hour.timetuple())
						print "d_time: ", d_time_tmp
						print "above_hour: ", above_hour
						if above_hour > d_time_tmp:
							found_flights += render_template('foundFlightsMiddle').format(		\
										departure_time, arrival_time) + " "
					else:
						found_flights += render_template('foundFlightsMiddle').format(		\
											departure_time, arrival_time) + " "
						
				found_flights += render_template('foundFlightsEnd')
					
			return question(found_flights) 
		return None
	


	@ask.intent("DepartureDateIntent", convert={'the_date': 'date'})
	def departure_date(the_date):
		
		session.attributes[constants.DEPARTURE_DATE] = str(the_date)
		departure_date_is_set = constants.DEPARTURE_DATE in session.attributes
	
	   	if departure_date_is_set:
			global flights_at_date
			flights_at_date = find_flights_at_date(the_date)
		
			if flights_at_date:
				"There is one or more flights at date"
				#if len(flights_at_date) <= 5:
				return list_flights(flights_at_date)
				#else:
				#	retu
			else:
				"There is no flight at date. Suggest flights near the date"
			
				#TODO: how to set that, to inform about, not founding a flights? (4 options)
				# 0 for found flights day before and/or after
				# -1 for no found flights

				session.attributes[constants.DEPARTURE_DATE] = 0	
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
					
					return question(render_template('noSuchFlightAtDateButAnother').format(			\
							session.attributes[constants.DEPARTURE_CITY],     		 				\
							session.attributes[constants.DESTINATION_CITY],							\
							str(the_date), suggested_flights))
				else:
					"Ask to look for flight at another date"
					session.attributes[constants.DEPARTURE_DATE] = -1

					return question(render_template('noSuchFlightAtDateNoAnother').format(			\
							session.attributes[constants.DEPARTURE_CITY],     					 	\
							session.attributes[constants.DESTINATION_CITY],							\
							str(the_date)))
	
	@ask.intent("ChooseFlightIntent", convert={'departure_time': 'time'})
	def choose_time(departure_time):

		departure_date_is_set = constants.DEPARTURE_DATE in session.attributes
		departure_time_conv = departure_time.strftime("%H:%M").lstrip('0')

		if departure_date_is_set:
			"Checks if flight at given departure_time exists"
			print "Flights2: ", flights_at_date					#test
			for flight in flights_at_date:
				print "Departure time: ", departure_time_conv	#test
				print "dt2 ", flight[5].split()[1]				#test

				if departure_time_conv == flight[5].split()[1]:
					session.attributes[constants.DEPARTURE_TIME] = departure_time_conv
			
			departure_time_is_set = constants.DEPARTURE_TIME in session.attributes

			if departure_time_is_set:
				"Confirmation of date and time"	
				return question(render_template('flightTimeChosen').format(			\
					session.attributes[constants.DEPARTURE_DATE], 					\
					session.attributes[constants.DEPARTURE_TIME]))
			else:
				"No flight at given time, ask to choose valid time"
				return question(render_template('askToRepeatTime').format(departure_time_conv))


	#@ask.intent("AlternativeDateIntent")
	#def alternative_date(value):