from PlayerClass import Player

class Match:
	'''
	Match class for storing match details
	'''
	def __init__(self, match_id, match_type,):
		self.match_id = match_id
		self.match_date = None
		self.match_type = match_type
		self.match_venue = None
		self.match_players = []
		self.restricted_dates = []
		self.prefered_match_days = []
		self.match_validity = True

	# Add players in the match
	def addPlayers(self, player: Player):
		'''
		Adds players to the match
		'''
		self.match_players.append(player)

	
	def validateMatch(self):
		'''
		Validates the match
		'''

		# If no common days, invalidate the match
		if len(self.prefered_match_days) == 0:
			# No common days so the match is invalid
			self.match_validity = False


		if self.match_type == "singles":
			if len(self.match_players) != 2:
				return False
		elif self.match_type == "doubles":
			if len(self.match_players) != 4:
				return False
	
	def addRestrictedDates(self,):
		'''
		Adds restricted dates from each player to the match
		'''
		
		for player in self.match_players:
			for date in player.restricted_dates:
				
				# Add the date to the restricted dates
				self.restricted_dates.append(date)


	def findPreferredMatchDay(self,):
		'''
		Finds the match day based on players preferred days
		'''

		# Find the common days
		common_days = set(self.match_players[0].preferred_day).intersection(*[player.preferred_day for player in self.match_players])

		# Add the common days to the preferred match days
		self.prefered_match_days = list(common_days)



