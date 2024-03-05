from datetime import timedelta, datetime

from DateClass import MatchDate
from PlayerClass import Player
from MatchClass import Match

from ortools.linear_solver import pywraplp


# NOTE - The current implementation works for a tournament that is played on Friday and Sunday, within a calendar year.


# Create list of dates for the tournament
# Dates must be on Friday and Sundays only

def create_dates(start_date:str, end_date:str):
	'''
	Creates the dates for the tournament

	Args:
		start_date: Start date of the tournament
		end_date: End date of the tournament
	'''
	
	# List of dates
	dates = []
	
	# Convert the string to date
	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	end_date = datetime.strptime(end_date, "%Y-%m-%d")


	# Iterate through the dates
	for n in range(int ((end_date - start_date).days)+1):
		date = start_date + timedelta(n)
		if date.strftime("%A") in ["Friday", "Sunday"]:
			dates.append(MatchDate(date))
	
	return dates


def schedule_matches(match_list: list[Match], match_date_list: list[MatchDate]):
	'''
	Schedules the matches based on the dates

	Args:
		match_list: List of matches
		date_list: List of dates
	'''

	time_slots = {"early":0.1, "mid":0.2, "late":0.3}

	# Create the solver
	solver = pywraplp.Solver.CreateSolver('SCIP')

	# Create the variables
	x = {}

	for match in match_list:
		for match_date in match_date_list:
			for court in match_date.available_courts:
				for time_slot in time_slots:
					x[(match.match_id, match_date.date.date(), court, time_slot)] = solver.IntVar(0, 1, f"x_{match.match_id}_{match_date.date.date()}_{court}_{time_slot}")




	# # Add the constraints for restricted days and time slots
	# for match in match_list:
	# 	for match_date in match_date_list:

	# 		# If date is restricted, set the coefficient to 0
	# 		if match_date.date.date() in match.restricted_dates:
	# 			for time_slot in time_slots:
	# 				constraint = solver.Constraint(0, 0)
	# 				constraint.SetCoefficient(x[(match.match_id, match_date.date.date(), time_slot)], 1)

			# # If date is not restricted, set the coefficient to 1
			# else:
			# 	for time_slot in time_slots:
			# 		constraint = solver.Constraint(1, 1)
			# 		constraint.SetCoefficient(x[(match.match_id, match_date.date.date(), time_slot)], 1)
				
	# Add constraints for restricted days
	for match in match_list:
		for match_date in match_date_list:
			if match_date.date.date() in match.restricted_dates:

				for court in match_date.available_courts:
					for time_slot in time_slots:

						solver.Add(x[(match.match_id, match_date.date.date(), court, time_slot)] == 0, 
						f"match_{match.match_id}_date_{match_date.date.date()}_restricted")


	# TODO
	# Add constraints for preferred days


	
	# Add the constraints for the number of matches per time slot per court
	for match_date in match_date_list:
		for court in match_date.available_courts:
			for time_slot in time_slots:
				solver.Add(solver.Sum(x[(match.match_id, match_date.date.date(), court, time_slot)] for match in match_list) <= 1, 
			   f"date_{match_date.date.date()}_court_{court}_time_slot_{time_slot}")


	
	# Add the constraints specifying every match must be played once
	for match in match_list:
		solver.Add(solver.Sum(x[(match.match_id, match_date.date.date(), court, time_slot)] for match_date in match_date_list for court in match_date.available_courts for time_slot in time_slots) == 1, 
			 f"match_{match.match_id}_played_once")

	

	# Add the objective function - Minimise the sum of day_in_year across all match days... Play the match as early as possible
	objective = solver.Objective()
	for match in match_list:
		for match_date in match_date_list:
			for court in match_date.available_courts:
				for time_slot in time_slots:
					objective.SetCoefficient(x[(match.match_id, match_date.date.date(), court, time_slot)], match_date.day_in_year + time_slots[time_slot]) 

	objective.SetMinimization()

	# Solve the problem
	status = solver.Solve()

	# Write the solution
	print('Number of variables =', solver.NumVariables())
	print('Number of constraints =', solver.NumConstraints())
	
	# Write the problem to a file
	with open("problem.lp", "w") as file:
		file.write(solver.ExportModelAsLpFormat(False))
		

	# Check the status
	if status == pywraplp.Solver.OPTIMAL:
		print('Solution:')
		print('Objective value =', objective.Value())
		for match in match_list:
			for match_date in match_date_list:
				for court in match_date.available_courts:
					for time_slot in time_slots:
						if x[(match.match_id, match_date.date.date(), court, time_slot)].solution_value() == 1:
							print(f"Match {match.match_id} - {match.match_players} - is scheduled on {match_date.date.date()} - Court {court} - {time_slot} ")

	else:
		print('The problem does not have an optimal solution.')



if __name__ == "__main__":

	match_date_list = create_dates(start_date = "2024-03-04", end_date = "2024-04-08")



	# Create the players
	player1 = Player("Alex", 1, ["Sunday"], ["2024-03-24",], 1, 1)
	player2 = Player("Bryan", 2, ["Sunday", "Friday"], [], 2, 2)
	player3 = Player("Charlie", 3, ["Sunday","Friday",], [], 3, 3)
	player4 = Player("David", 4, ["Sunday","Friday",], [], 4, 4)
	player5 = Player("Evan", 5, ["Sunday"], [], 5, 5)
	player6 = Player("Frank", 6, ["Sunday","Friday",], [], 6, 6)
	player7 = Player("George", 7, ["Sunday","Friday",], ["2024-03-15"], 7, 7)
	player8 = Player("Harry", 8, ["Sunday","Friday"], ["2024-03-17"], 8, 8)
	player9 = Player("Ivan", 9, ["Sunday","Friday"], ["2024-03-15"], 9, 9)
	player10 = Player("John", 10, ["Sunday","Friday"], ["2024-03-17"], 10, 10)
	player11 = Player("Kevin", 11, ["Sunday","Friday"], [], 11, 11)
	player12 = Player("Liam", 12, ["Sunday","Friday"], [], 12, 12)
	player13 = Player("Michael", 13, ["Sunday","Friday"], ["2024-03-15"], 13, 13)
	player14 = Player("Nathan", 14, ["Friday"], [], 14, 14)
	player15 = Player("Oscar", 15, ["Sunday","Friday"], [], 15, 15)
	player16 = Player("Peter", 16, ["Sunday","Friday"], ["2024-03-17"], 16, 16)

	player_list = [player1, player2, 
				player3, player4, 
				player5, player6, 
				player7, player8, 
				player9, player10, 
				player11, player12, 
				player13, player14, 
				player15, player16
				]


	# for player in player_list:
	# 	print(player)


	# Create the matches
	match1 = Match(1, "singles")
	match2 = Match(2, "singles")
	match3 = Match(3, "singles")
	match4 = Match(4, "singles")
	match5 = Match(5, "singles")
	match6 = Match(6, "singles")
	match7 = Match(7, "singles")
	match8 = Match(8, "singles")

	match_list = [match1, match2, 
			   match3, 
			   match4, 
				match5, match6,
				  match7, match8
				  ]

	# Add players to the match
	match1.addPlayers(player1)
	match1.addPlayers(player2)

	match2.addPlayers(player3)
	match2.addPlayers(player4)

	match3.addPlayers(player5)
	match3.addPlayers(player6)

	match4.addPlayers(player7)
	match4.addPlayers(player8)

	match5.addPlayers(player9)
	match5.addPlayers(player10)

	match6.addPlayers(player11)
	match6.addPlayers(player12)

	match7.addPlayers(player13)
	match7.addPlayers(player14)

	match8.addPlayers(player15)
	match8.addPlayers(player16)



	# Add restricted dates to the matches
	for match in match_list:
		match.addRestrictedDates()
	

	# Find the preferred match days
	for match in match_list:
		match.findPreferredMatchDay()
		match.validateMatch()


	# Print the restricted dates
	for match in match_list:
		print(match.match_id)
		print(match.restricted_dates)
		print(match.prefered_match_days)
		print(match.match_validity)


	# Schedule the matches
	schedule_matches(match_list, match_date_list)
	