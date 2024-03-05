from datetime import datetime

class MatchDate:
	'''
		Represents a date of a tournament

	'''

	def __init__(self, date: datetime):


		self.date = date

		# Day of the week
		self.day_of_week = self.date.strftime("%A")

		# Day in year
		self.day_in_year = self.date.timetuple().tm_yday
		
		# Number of courts available on the date
		self.available_courts = self.courtsAvailable()
		
		# Time slots available
		self.time_slots = self.timeSlotsAvailable()

	def courtsAvailable(self):
		'''
			Returns the courts available on the date

			Adjust the values based on what is available on the date
		'''

		if self.day_of_week == "Sunday":
			return ["3","4"]
		
		elif self.day_of_week == "Friday":
			return ["5",]
		
		else:
			return 0
		
	
	def timeSlotsAvailable(self):
		'''
			Returns the time slots available on the date
		'''

		if self.day_of_week == "Sunday":
			return ["early", "mid", "late"]
		elif self.day_of_week == "Friday":
			return  ["early", "mid", "late"]
		
		else:
			return []
		
	def __str__(self):
		'''
			Returns the string representation of the date
		'''
		return f"{self.date.date()} - {self.day_of_week}"
	
	def __repr__(self):
		'''
			Returns the string representation of the date, without time component of date
		'''
		return f"{self.date.date()}"
		# return f"{self.date} - {self.day_of_week} - {self.available_courts} - {self.time_slots}"