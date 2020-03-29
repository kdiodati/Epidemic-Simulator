"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This module is in charge of collecting and producing statistics on the simulation and the data it collected from
the contagions influence on the population.
"""

import os
import sys

import lib.city
import lib.person
import lib.vessel


class statistics:

    def __init__(self):
        """
        self, None -> None
        This function has the purpose of initializing the statistics module. 
        This module keeps track of all statistical calculations/displays that the program makes.
        """
        self.cities = list() #list of all the cities in the simulation
        self.activevessels = list() # list of flights that are ready to leave
        self.inactivevessels = list() # list of flights not ready to leave
        #number of dead, immune, infected and healthy individuals
        self.dead = 0
        self.immune = 0
        self.inf = 0
        self.healthy = 0

        self.Re = 100
        self.totalPop = 0

    def add_vessels(self, newVessels):
        """
        self, list(new vessels) -> None
        This function adds new vessels to the active planes we can track.
        """
        self.activevessels += newVessels
        return

    def add_city(self, newcity):
        """
        self, city (city object) -> None
        This function adds cities to the statistics cities list.
        """
        self.cities.append(newcity)
        # Add to the total population.
        self.totalPop += len(newcity.people)
        return 

    def curr_contagion_info(self, hour, run_time):
        """
        self, int (hour), int (run time) -> None
        This function has a purpose of printing the current information of the contagions impact 
        on the population for that specific day: hour. This function is solely used for printing to console
        to visually show the trends in the contagion contamination.
        """

        #print header day and hour values
        formated_completon_perc = str((hour/run_time) * 100)
        formated_completon_perc = formated_completon_perc[:5]
        print("\033[0;0H", end="")
        print("\rSimulation Completion at {}%\n".format(formated_completon_perc), end="\n")
        print("\r\33[1mDay {}\tHour {}:".format(int(hour/24), hour), end="\n")
        #iterate through all the cities and get the total counts for contagion information
        for location in self.cities:
            inf = location.inf_count
            hlth = location.healthy_count
            immu = location.immune_count
            dead = location.dead_count
            #print the information to the console
            print("\r \033[K", end="") # Fixes healthy having character duplicates
            print("\r \33[1m {}\33[0m:\t\t\33[32m{} Healthy\33[0m\t {} Immune\t\33[93m{} Infected \33[0m\t\33[31m {} Dead \33[0m".format(location.name, hlth, immu, inf, dead), end="\n")
        
        print("\r\nEffective Reproduction Number: {}".format(self.Re), end="\n")

        print("\r\nPress CTRL^C to exit the simulation early.")
        return 
    
    def get_total_counts(self):
        """
        self, None -> None
        This function is responsible for getting the total amount of the given attribute (inf, dead etc) people 
        from each city to report statistics.
        """
        for city in self.cities: #iterate through all the cities
            self.healthy += city.healthy_count
            self.dead += city.dead_count
            self.immune += city.immune_count
            self.inf += city.inf_count
        
        # Get counts for people still in flight when the program finishes.
        for flight in self.activevessels:
            for person in flight.people:
                if person.immune:
                    self.immune += 1
                elif person.dead:
                    self.dead += 1
                elif person.infected:
                    self.inf += 1
                else:
                    self.healthy += 1
        return

    def get_percentage(self, count, init_population):
        """
        self, int (count of people), int (healthy person count) -> float
        This function is in charge of calculating the percentage of individuals that 
        die, get infected or become immune compared to the overall population.
        """
        #try to calculate percentage
        try:
            return ((count/init_population) * 100)
        except ZeroDivisionError:
            #if there is a division by zero error for some reason
            return 0

    def print_time_series_table(self, days, immune, infected, dead):
        """
        self, list, list, list, list -> None
        This function is in charge of printing a table that shows all the time series data
        that has been collected. This will be exececuted at the end of the program.
        """
        #dict for labels and rows
        table = [days, infected, immune, dead]
        #list of all header labels
        headers = ["Days", "Infected", "Immune", "Dead"]
        for item in headers:
            print("\33[1m{:>10}\33[0m".format(item).strip("\n"), end="")
        print("")
        #iterate through table keys
        i = 0
        while(i<len(days)):
            for row in table:
                #print the necessary item in the index given by i
                print("{: >10}".format(row[i]).strip("\n"), end="")
            #print a new line for the next day
            print("")
            i += 1
        return

    def average_stats(self, days, attribute):
        """
        self, int (days), int (attribute) -> float
        This function has a purpose of determining the average number of
        individuals that die, immune or are infected each day. 
        """
        return attribute/days

    def print_stats(self, days, initial_pop):
        """
        self, int (days the simulation ran for), int (initial population) -> None
        This function has the sole function of printing all final statistics after
        the execution of the main program.
        """
        #get the total counts of infected, dead, immune and healthy individuals
        self.get_total_counts()
        #get the percentage of those dead, immune and infected
        dead_perc = self.get_percentage(self.dead, initial_pop)
        immune_perc = self.get_percentage(self.immune, initial_pop)
        inf_perc = self.get_percentage(self.inf, initial_pop)
        healthy_perc = self.get_percentage(self.healthy, initial_pop)
        average_deaths = self.average_stats(days,self.dead)
        average_infected = self.average_stats(days, self.inf)
        average_immune = self.average_stats(days, self.immune)
        #print the total counts after the amount of time the simulation has run
        print("\n\nAfter {} days, these are the results of the contagions impact on the population with {} individuals.".format(days, initial_pop))
        print("\33[1mTotal Counts ---->\33[0m\33[32m Healthy: {},\33[0m\33[93m Infected: {},\33[0m \33[31mDead: {},\33[0m Immune: {}".format(self.healthy, self.inf, self.dead, self.immune))
        print("Each day on average: \33[93m{} people are infected\33[0m, \33[31m{} die\33[0m and {} become immune.".format(average_infected, average_deaths, average_immune))
        #print the total amount of healthy people, dead, infected and immune
        print("Out of the {} people in the total population.".format(initial_pop))
        print("{}% are \33[31mdead.\33[0m".format(dead_perc))
        print("{}% are immune.".format(immune_perc))
        print("{}% were \33[93minfected.\33[0m".format(inf_perc))
        print("{}% are still \33[32mhealthy.\33[0m".format(healthy_perc))
        return
