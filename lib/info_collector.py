"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This file is in charge of collecting daily information on populations influenced by the contagion.
"""

class collector:

    def __init__(self):
        """
        self, None -> None
        This is the initialization function for the collector class. This class has
        a primary purpose of storing daily populational data:
            1) Current day
            2) Number of people dead
            3) Number of people immune
            4) Number of people infected
            5) People statistics in flight
            6) Total healthy population list
            7) Key: "<city>" : Value: List() 
                - where the list is of daily healthy individuals (counts, numerical values) for that city.
            8) Number of infected travelers per day.
            
        This information is then given to the graph module to create a time series graph.
        """
        self.days_plot = list() #1
        self.dead_plot = list() #2
        self.immune_plot = list() #3
        self.infected_plot = list() #4
        self.flight_info = list() #5
        self.total_healthy = list() #6
        self.healthy_city_info = dict() #7
        self.infected_travelers_plot = list() #8

    def add_to_daysplot(self, i):
        """
        self, int (number of days) -> None
        This function is incharge of adding the number of days that have passed.
        """
        self.days_plot.append(i)
        return

    def add_to_dplot(self, i):
        """
        self, int (number dead) -> None
        This function is incharge of adding the number of dead
        individuals to its containers list
        """
        self.dead_plot.append(i)
        return

    def add_to_implot(self, i):
        """
        self, int (number immune) -> None
        This function is incharge of adding the number of immune
        individuals to its containers list
        """
        self.immune_plot.append(i)
        return 

    def add_to_iplot(self, i):
        """
        self, int (number infected) -> None
        This function is incharge of adding the number of infected
        individuals to its containers list
        """
        self.infected_plot.append(i)
        return
    
    def add_flights(self, flight_count):
        """
        self, int(number of flights on a given day) -> None
        This function has the purpose of adding the total number of outgoing flights.
        """
        #add the daily value of flight traffic
        self.flight_info.append(flight_count)
        return

    def track_healthy(self, daily_healthy_pop, city_name):
        """
        self, int (difference in healthy population), str (city name) -> None
        This function is in charge adding the number of the daily healthy population
        to later be used for graphical visualization.
        """
        #if the city is not yet a key, add it
        if(city_name not in self.healthy_city_info.keys()):
            self.healthy_city_info[city_name] = list()
        #add the daily number of healthy individuals for that city
        self.healthy_city_info[city_name].append(daily_healthy_pop)
        return
    
    def add_infected_travelers(self, num_infected_travelers):
        """
        self, int -> None
        This will add the number of infected travelers for a specific day during the simulation.
        """
        self.infected_travelers_plot.append(num_infected_travelers)
        return
