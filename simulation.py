"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This is the main file of the program. It contains the main loop and function.
"""

import time
import sys
import threading
import random
from lib.city import city
from lib.person import person
from lib.statistics import statistics
from lib.vessel import vessel
from lib.parser import parser
from lib.argparser import argparser
from lib.info_collector import collector
from lib.graph import graph
import os

def main():
    """
    None -> None
    This serves as the main program.
    """

    # Initialize classes. Argparser, statistics, information collector, graph and parser.
    arg_parser = argparser()
    stats_record = statistics()
    info_collector = collector()
    epi_graph = graph()
    file_parser = parser()

    # Get the options from the arguments passed in by the user.
    print("Gathering simulation parameters...")
    options = arg_parser.collect_and_return_args()
    options.R_0 = abs(float(options.R_0))
    options.life_time = abs(float(options.life_time))
    options.death_rate = abs(float(options.death_rate))
    options.infected_count = abs(int(options.infected_count))
    options.daily_travel_percentage = abs(float(options.daily_travel_percentage))
    travel_p = options.daily_travel_percentage
    if(travel_p >= .003):
        os.system('cls' if os.name == 'nt' else 'clear')
        raise Exception("ERROR: Daily travel percentage must be less than .003.")
    # Get the total amount of initially infected people.
    initial_inf_count = abs(options.infected_count)
    file_parser.open_and_read_city_file(options.cities_file) # Read the city file and save info into parser.
    file_parser.open_and_read_plane_file(options.planes_file) # Read the plane file and save info into parser.
    # Get the total number of hours the program should simulate based on the number of days it should run.
    days_to_run = abs(int(round(float(options.sim_time))))

    if(options.life_time == 0):
        os.system('cls' if os.name == 'nt' else 'clear')
        raise Exception("ERROR: Life time must be greater than zero.")
    hours_to_run = (days_to_run * 24)

    cities = list() # Create a list to hold all city classes used in simulation.
    # Declare rate of reproduction, hour, and day variables for the main loop.
    hour = 1
    day = 1
    total_person_count = 0
    if(days_to_run < 2):
        os.system('cls' if os.name == 'nt' else 'clear')
        raise Exception("ERROR: Epidemic simulation needs to run longer than 2 days.")
    # Create list of cities.
    for c in file_parser.cities_list:
        nc = city(c, file_parser.planes_list, travel_p, options)
        cities.append(nc)
        stats_record.add_city(nc)
    
    # Add cities as locations to visit and calculate distance between cities.
    for i in cities:
        for j in cities:
            i.add_cities(j)
        total_person_count += len(i.people)
    # Infect the correct amount of people.
    num_inf = 0
    while (num_inf < initial_inf_count):
        # Choose the city and person randomly to infect.
        city_to_inf = random.choice(cities)
        #choose a random person to infect in that city
        person_to_inf = random.choice(city_to_inf.people)
        #check to make sure that person is not already infected
        if(person_to_inf.infected == True): 
            #if that person is already infected continue and find somebody who is not
            continue
        #once you found somebody infect them
        person_to_inf.infect()
        #add to the infected count and decrease the healthy count for that city
        city_to_inf.inf_count += 1
        city_to_inf.healthy_count -= 1
        num_inf += 1

    # Clear the system to display proper program information.
    os.system('cls' if os.name == 'nt' else 'clear')

    # indexes for totals, used in people totals
    dead_count_ind = 0
    infected_count_ind = 1
    immune_count_ind = 2
    healthy_count_ind = 3

    infected_travelers_per_day = 0

    try:
        while(stats_record.Re > 0.3):

            # Program has run for the total number of hours requested, exit.
            if(hours_to_run == hour):
                break

            # Increment hour after checking if the simulation reached the end.
            hour += 1
            
            # totals of people status
            people_totals = [0, 0, 0, 0]
            flight_total = 0
            healthy_each_day = 0
            # Call update methods for city objects and record data.
            for location in cities:
                stats_record.add_vessels(location.tick())
                # If end of day, add totals for each location.
                people_totals[dead_count_ind] += location.dead_count
                people_totals[infected_count_ind] += location.inf_count
                people_totals[immune_count_ind] += location.immune_count
                people_totals[healthy_count_ind] += location.healthy_count
                healthy_each_day += location.healthy_count
                flight_total += location.flights_counter
                if(hour % 24 == 0):
                    info_collector.track_healthy(location.healthy_count, location.name)
                    infected_travelers_per_day += location.sent_infected_people
                    location.sent_infected_people = 0
                    location.flights_counter = 0

            stats_record.Re = float(people_totals[healthy_count_ind]/stats_record.totalPop) * options.R_0
            if not people_totals[infected_count_ind]:
                break
                
            # Collect daily contagion information for graphing purposes.        

            if(hour % 24 == 0):
                info_collector.add_to_daysplot(day)
                info_collector.add_to_dplot(people_totals[dead_count_ind])
                info_collector.add_to_iplot(people_totals[infected_count_ind])
                info_collector.add_to_implot(people_totals[immune_count_ind])
                info_collector.add_flights(flight_total)
                info_collector.add_infected_travelers(infected_travelers_per_day)
                infected_travelers_per_day = 0

                info_collector.total_healthy.append(healthy_each_day)
                day += 1

            # Call update method for vƒessel objects and update the active and inactive vessel lists.
            for vessel in stats_record.activevessels:
                if vessel.tick():
                    stats_record.activevessels.remove(vessel) #remove an active flight from actives list
                    stats_record.inactivevessels.append(vessel) #add flight to inactive flights list
            
            # Display the current contagion information
            stats_record.curr_contagion_info(hour, hours_to_run)

    except:
        print("\nWARNING: Keyboard interrupt. Printing statistics...")
        stats_record.print_stats(days_to_run, total_person_count)
        sys.stdout.write("\n")
        return

    #print overal simulation statistics
    stats_record.print_stats(days_to_run, total_person_count)
    sys.stdout.write("\n")
    #produce a time series graph of the contagion spreading over the period of time the simulation modeled.
    stats_record.print_time_series_table(info_collector.days_plot, info_collector.immune_plot, info_collector.infected_plot, info_collector.dead_plot)
    epi_graph.create_and_show_graphs(info_collector.days_plot, info_collector.immune_plot, info_collector.infected_plot, info_collector.dead_plot, info_collector.healthy_city_info, info_collector.flight_info, info_collector.infected_travelers_plot)
    sys.stdout.write("\n")

    return

# When the program is run, call the main function.
if(__name__ == "__main__"):
    main()
