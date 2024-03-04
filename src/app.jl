
using DataFrames
using CSV
using JuMP
using HiGHS

# Matches to Play
matches = DataFrame(
	Team1 = ["A", "B", "C", "D",],
)




# Day Restrictions
day_restrictions = DataFrame(
	Team1 = ["A", "B", "C", "D",],
	Day = ["Sunday", "Sunday", "Friday", "Sunday",]
)


# Weeks to Play
weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Setting time slots for each day
time_slots = [1, 2, 3]


# Setting available courts for each day
available_courts_sunday = 1
available_courts_friday = 1

# Generating Court List 
courts_sunday = [1:available_courts_sunday]
courts_friday = [1:available_courts_friday]






