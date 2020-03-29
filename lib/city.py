"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This file contains the city class which is in charge of initializing and maintaining city objects
"""

from lib.parser import parser
from lib.person import person
from lib.statistics import statistics
from lib.vessel import vessel
import math
import random
import sys
import time
from random import choices

#Global variables for dead and recovered individuals
DEAD = "dead"
RECOVERED = "recovered"

class city:

    def __init__(self, cities, vessels, travel_p, contagion_params):
        """
        self, list, list, float (travel percentage), Namespace (system parameters) -> None
        This initializes all of the city class attributes name, latitude, longitude and population.
        """
        self.percent_travel_daily = travel_p
        self.travel_dict = dict()
        self.name = cities.city_name # string of city name
        self.lat = float(cities.lat) # latitude for distance calculations
        self.lon = float(cities.lon) # longitude for distance calculations
        self.pop = int(cities.pop) # initial population of city (will update as people leave/arrive)
        self.dead_count = 0 # count of dead people in that city from the contagion
        self.immune_count = 0 # count of immune people to the contagion in that city
        self.inf_count = 0 # count of all immune people to that contagion in that city
        self.healthy_count = int(cities.pop) # health count of all people in the city
        self.received_infected_people = 0 # count all infected people that travel to the city
        self.sent_infected_people = 0 # count all sent infected people
        self.flights_counter = 0

        self.contagion_params = contagion_params

        # Initialize people in city.
        self.people = list()
        for i in range(self.pop):
            self.people.append(person(self.contagion_params))

        # Initialize city with list of planes available in simulation.
        self.vessels = vessels
        vessels.sort(key=lambda vessel: vessel.capacity)

        # Initialize list to hold cities and their locations.
        self.locations = list()
        self.locationspop = list()
        self.distances = dict()

    def __pass_infection(self):
        """
        self, None -> None
        This function calculates the infections that occur over the course of a tick(hour)
        If the infection check passes it will attempt to randomly infect a person in the city
        """
        #Look into rE modifier to calculate how infection rate changes over course of epidemic
        #chance for infected person to infect other over tick(hour)
        infection_per_tick = self.contagion_params.R_0 / (self.contagion_params.life_time * 24.0)
        for person in self.people:
            if person.infected:
                # if chance is less than or equal to infection per tick chance try to infect
                if choices([True, False], [infection_per_tick, 1-infection_per_tick])[0]:
                    contact = False
                    while (contact == False):
                        # attempt to infect random person from the list, if they are
                        person = random.choice(self.people)
                        # if the person is healthy, then adjust the infected and healthy count
                        # for the city
                        if not person.immune and not person.dead and not person.infected:
                            self.inf_count += 1
                            self.healthy_count -= 1
                        contact = person.infect()
        return

    def __append_travel_dict(self):
        """
        self, None -> None
        This function is responsible for determining which person object will travel next
        and adding them to the list of other people who are set to travel with their destinations.
        """
        # Obtain the number of individuals who are being selected.
        num_people = self.percent_travel_daily * len(self.people)
        for i in range(int(num_people)):

            # find a valid person to add to outgoing lists
            valid_person = False
            new_person = None
            while not valid_person:
                new_person = random.choice(self.people)
                if not new_person.dead:
                    notinlist = True
                    for key in self.travel_dict:
                        if new_person in self.travel_dict[key]:
                            notinlist = False
                    valid_person = notinlist
            
            # Determine a destination and add the person and destination to the travel dictionary.
            destination = choices(self.locations, self.locationspop)[0]
            self.travel_dict[destination.name].append(new_person)
        return


    def __build_vessels(self):
        """
        self, None -> list (new flights)
        This method builds the vessels for each tick of the self.tick() method.
        """
        # Create a list for the new flights.
        new_flights = list()

        # Iterate through each location.
        for location in self.locations:
            # Add planes that can reach the destination to a list.
            valid_planes = list()
            for vessel in self.vessels:
                if vessel.min_flight_dist <= self.distances[location.name] and vessel.max_flight_dist >= self.distances[location.name]:
                    valid_planes.append(vessel)

            # Loop through the valid planes.
            while valid_planes[0].capacity * .5 < len(self.travel_dict[location.name]):
                # Add flights to the new flights list.
                new_flights.append(self.__choose_plane(location, valid_planes))

        # Return the new flights.
        return new_flights
                        
    def __choose_plane(self, location, valid_planes):
        """
        self, city obj , list (plane obj's) -> plane obj
        This method chooses a plane for the __buildVessels method.
        """
        # Iterate for the length of the valid planes list.
        for i in range(1, len(valid_planes)):
            if len(self.travel_dict[location.name]) >= valid_planes[len(valid_planes) - i].capacity:
                return self.__send_flight(location, valid_planes[len(valid_planes) - i])
        return self.__send_flight(location, valid_planes[0])

    def __send_flight(self, location, plane):
        """
        self, location, plane -> vessel
        This method is used when a vessel is sent to another location.
        """
        # Declare the send list for people going on the flight.
        send_list = list()
        # Get the boarding number
        boarding_number = min(plane.capacity, len(self.travel_dict[location.name]))
        for i in range(boarding_number):
            # Add the correct number of people to the send list.
            sent = self.travel_dict[location.name].pop(0)
            send_list.append(sent)
            # Remove the person from the population.
            self.people.remove(sent)
            
        # Update count for each type of person in the city
        for person in send_list:
            if person.immune:
                self.immune_count -= 1
            elif person.infected:
                self.inf_count -= 1
                self.sent_infected_people += 1
            elif person.dead:
                self.dead_count -= 1
            else:
                self.healthy_count -= 1
        self.flights_counter += 1

        # Return the vessel to be sent.
        return vessel(send_list, self.distances[location.name], self, location, plane, self.contagion_params)

    def add_cities(self, new_city):
        """
        self, city obj -> None
        adds a city to the list of neighboring cities held in the city files
        """
        # Check if the city is itself.
        if new_city.name != self.name:
            # If not, add the city to the locations list, calculate the distance, add to travel dictionary, and
            # add to locations population list.
            self.locations.append(new_city)
            self.calculate_distance(new_city)
            self.travel_dict[new_city.name] = list()
            self.locationspop.append(new_city.pop)
        return

    def calculate_distance(self, new_city):
        """
        self, city obj -> None
        Using the Harversine formula, calculates the distance between this city and another city (newCity)
        Uses the latitude and longitude from each city to create a single distance in nautical miles
        """
        lat1 = math.radians(self.lat) # latitiude of city A in radians
        lon1 = math.radians(self.lon) # Longitude of city A in radians
        lat2 = math.radians(new_city.lat) # latitiude of city B in radians
        lon2 = math.radians(new_city.lon) # Longitude of city B in radians

        dlon = lon2 - lon1 # generates the difference in longitudes from city A to B
        dlat = lat2 - lat1 # generates the difference in latitudes from city A to B

        # calculates the distance using the Haversine Formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        distance = 3958.8 * c # multiplies distance to nautical miles to correlate with nautical miles planes can travel and speed planes cruise at

        # Checks to see if distance is reachable by any plane passed in
        reachable = False
        for plane in self.vessels:
            if(plane.min_flight_dist <= distance and plane.max_flight_dist >= distance):
                reachable = True
        if(reachable):
            self.distances[new_city.name] = distance
        else:
            raise Exception("ERROR: City {} not reachable by any plane in the simulation. Please edit the configuration cities file {}".format(new_city.name, self.contagion_params.cities_file))
        return

    def tick(self):
        """
        self, None -> list (vessels)
        This is the main update method for the city class. It is called each iteration of the simulation.
        """
        # First call the __pass_infection() method to spread the virus on each tick of the simulation.
        self.__pass_infection()

        # Loop through the people in the location and update them.
        for person in self.people:
            if(not person.infected):
                continue
            change = person.tick()
            # Once they are updated, if their status changes, reflect that change in the location attributes.
            if change == DEAD:
                self.inf_count -= 1
                self.dead_count += 1
            elif change == RECOVERED:
                self.inf_count -= 1
                self.immune_count += 1
        
        # Update the travel dictionary.
        self.__append_travel_dict()
        # Return vessels.
        return self.__build_vessels()

    def receive_journey(self, new_people):
        """
        self, list() people for journey -> None
        This functions purpose is to add people from incoming flights into the population
        """
        # Create a temporary list for the people in the city.
        temp = list()
        temp = self.people[:]
        # Add the new people to the people in the city.
        self.people = temp + new_people
        # Iterate through each person from the arriving plane and update counters.
        for person in new_people:
            if person.immune:
                self.immune_count += 1
            elif person.infected:
                self.inf_count += 1
                self.received_infected_people += 1
            elif person.dead:
                self.dead_count += 1
            else:
                self.healthy_count += 1
        return
