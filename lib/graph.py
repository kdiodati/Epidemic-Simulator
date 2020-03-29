"""
03/01/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This file is for creating graphical time series outputs that visualize program data.
"""

import matplotlib.pyplot as plt
import random

#Globals that represent different plots, their values need to be different
#in order for the plots to know which figure is being used.
PLOT_1 = 121
PLOT_2 = 122

class graph:
    
    def __init__(self):
        """
        self, None -> None
        This function is initializing the a list of colors/markers used for the cities graph.
        There is also an attribute that keeps track of what colors have used which markers.
        """
        self.colors = ["blue", "green", "red", "cyan", "magenta", "gold", "black", "olive", "saddlebrown", "purple"]
        self.markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"]
        self.used_dict = dict()
    
    def create_and_show_graphs(self, days, immune, infected, dead, healthy_lists, flights, infected_travelers):
        """
        self, list(), list(), list(), list() dict(), list(), list() -> None
        This is a high level function that generates graphs based on collected data. 
        """
        self.generate_flight_graphs(days, flights, infected_travelers)
        self.generate_population_graphs(days, immune, infected, dead, healthy_lists)
        plt.show()
        return

    def generate_population_graphs(self, days, immune, infected, dead, healthy_lists):
        """
        self, list (integers), list (integers), list (integers), list (integers), dict (key: city name (string): Value: list of daily healthy people-> None
        This creates a time series graph of the results of the simulation.
        This function makes two graphs, one showing the change in immune, dead and infected numbers, as 
        well as a graph showing the change in healthy counts for each city.
        """
        #plot all the immune, infected and dead individuals over the days of the simulation
        plt.figure("Population Graphs", figsize = (12, 6))
        plt.subplot(PLOT_1)
        #set the x tick labels to be size 14
        plt.xticks(fontsize = 14)
        #set the y labels to a size 14 font
        plt.yticks(fontsize = 14)
        #label the y axis with size 14 font
        plt.ylabel('Frequency of People', fontsize = 14)
        #label the x axis with size 14 font
        plt.xlabel('Number of Days', fontsize = 14)
        #label the graph
        plt.title('Epidemic Time Series', fontsize = 14)
        #allow the graph to have a grid in the backgound
        plt.grid(True)
        #set the legend and place the legend. 
        plt.plot(days, immune, c='black', marker = "o", linestyle = '-', label = "immune")
        plt.plot(days, infected, c='gold', marker = "p", linestyle = '-.', label = "infected")
        plt.plot(days, dead, c='red', marker = "x", linestyle = '-', label = "dead")
        plt.legend(bbox_to_anchor=(.2, 1), loc='upper center')

        #fit the plot so it is proportional and everything is visable  
        plt.tight_layout()
        ###############################################################################
        plt.subplot(PLOT_2) #the plot for all healthy people over time in cities
        #iterate through all the locations
        #set the x tick labels to be size 14
        plt.xticks(fontsize = 14)
        #set the y labels to a size 14 font
        plt.yticks(fontsize = 14)
        #label the y axis with size 14 font
        plt.ylabel('Frequency of People', fontsize = 14)
        #label the x axis with size 14 font
        plt.xlabel('Number of Days', fontsize = 14)
        #label the graph
        plt.title('Epidemic Time Series (Healthy only)', fontsize = 14)
        #allow the graph to have a grid in the backgound
        plt.grid(True)

        #iterate through all the locations 
        for location in healthy_lists.keys():
            #get the list of population counts for that city
            city_list = healthy_lists[location]
            #get the color and marker style to plot the information
            color, marker = self.get_line_style()
            plt.plot(days, city_list, c=color, marker = marker, linestyle = '-', label = '{}'.format(location))
        plt.legend(bbox_to_anchor=(.2, 1), loc='upper center')
        #fit the plot so it is proportional and everything is visable  
        plt.tight_layout()

        return

    def generate_flight_graphs(self, days, flights, infected_travelers):
        """
        self, list (integers), list (flights), list (infected travelers) -> None
        This function has the sole purpose of creating graphs that are involved with
        air traffic information. This function will display one window with two graphs.
        """
        plt.figure("Flight Graphs", figsize = (12, 6)) #create a new window
        plt.subplot(PLOT_1) #add the first plot of flights per day
        plt.title('Flights per Day')
        plt.ylabel('Frequency of flights', fontsize = 14)
        plt.xlabel('Number of Days', fontsize = 14)
        plt.xticks(fontsize = 14) #set the x tick mark labels to a size 14 font
        plt.yticks(fontsize = 14)
        #label the y axis with size 14 font
        plt.grid(True) #show the grid of the graph
        #plot the frequency of flights over the number of days
        plt.plot(days, flights, c='blue', marker = "4", linestyle = '-', label = "flights")
        plt.legend(bbox_to_anchor=(.2, 1), loc='upper center')
        #fit the plot so it is proportional and everything is visable  
        plt.tight_layout()
        ###################################################################################
        plt.subplot(PLOT_2) #create the second plot
        #set chart features
        plt.title('Infected Travelers per Day')
        plt.ylabel('Frequency of Infected Travelers', fontsize = 14)
        plt.xlabel('Number of Days', fontsize = 14)
        plt.xticks(fontsize = 14) #set x ticks
        #set the y labels to a size 14 font
        plt.yticks(fontsize = 14)
        plt.grid(True)
        #plot the number of infected travelors over the number of days the simulation ran
        plt.plot(days, infected_travelers, c="olive", marker = 'x', linestyle='-', label="infected travelers")
        #create a legend
        plt.legend(bbox_to_anchor=(.2, 1), loc='upper center')
        #fit the plot so it is proportional and everything is visable  
        plt.tight_layout()

        return
    
    def get_line_style(self):
        """
        self, None -> str(color), str(marker)
        This function has the primary goal of finding a color that has not yet
        been used for a city in the graph. If the color HAS been used, the program 
        will look for a marker that has not been used with that color so that city 
        is still distinguishable.
        """
        #loop until there is no duplicate line/marker
        while True:
            #initialize color and marker to be none
            color = None
            marker = None
            #check if the colors list is empty
            if(len(self.colors) == 0):
                #if it is empty all colors have been used
                #since the used_dict has keys that are colors and values
                #of all used markers for that color
                #get a random key (color) and a random marker
                color = random.choice(self.used_dict.keys())
                marker = random.choice(self.markers)
                #get the list of all markers used with that color
                markers = self.used_dict[color]
                #if the marker chosen has been used, go to the top of the loop
                if(marker in markers):
                    continue
            else:
                #if theree are still colors in the list get a random color
                color = random.choice(self.colors)
                #get a random marker
                marker = random.choice(self.markers)
                #remove the color from the unused colors list
                self.colors.remove(color)
                #add the color as a key to that dict with an emtpy list as its value
                self.used_dict[color] = list()
            #add the used marker to the list of that color
            self.used_dict[color].append(marker)
            return color, marker
        
