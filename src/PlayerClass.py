from datetime import datetime

class Player:
	'''
	Class for the player object
	'''

	def __init__(self, name, u_id,   preferred_day, restricted_dates, singles_rank, doubles_rank,):
		self.name = name
		self.u_id = u_id
		self.preferred_day = preferred_day

		# Convert the restricted dates to datetime objects
		raw_restricted_dates = restricted_dates
		self.restricted_dates = [datetime.strptime(date, "%Y-%m-%d").date() for date in raw_restricted_dates]

		self.singles_rank = singles_rank
		self.doubles_rank = doubles_rank

	
	def __str__(self):
		'''
		Returns the string representation of the player
		'''
		return f"{self.name} - {self.u_id} - {self.preferred_day} - {self.restricted_dates}"
	
	def __repr__(self):
		'''
		Returns the string representation of the player
		'''
		return f"{self.name} - {self.u_id}"