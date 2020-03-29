"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This module is in charge of creating and maintaining vessel objects (planes) that are used transport person objects
between cities.
"""

import lib.city
import lib.person
import lib.statistics
import lib.parser

import random

from random import choices

class vessel:

    def __init__(self, people, distance, sourceCity, destinationCity, vesselParam, contagionParams):
        """
        self, list, namedTuple, city, city, namedTuple -> None
        Vessel represents an airplane that can travel city to city. Vessel contains
        passengers that are Person objects. The self.tick() method is called for every
        update of the vessel.
        """
        self.people = people # Store the people in the vessel.
        self.distance = distance # Keep the distance to the destination.
        self.sourceCity = sourceCity # The name of the departure city.
        self.destinationCity = destinationCity # The name of the destination city.
        self.vesselParam = vesselParam # The vessel parameters.
        self.distanceTraveled = 0 # A counter to keep track of how far a vessel has traveled.
        self.active = True # A flag for whether the vessel is still in the air or has arrived.

        self.contagionParams = contagionParams # The parameters for the contagion that could be on the vessel.
    
    def __passInfection(self):
        """
        self, None -> None
        This function calculates the infections that occur over the course of a tick(hour)
        If the infection check passes it will attempt to randomly infect a person in the city
        """
        #Look into rE modifier to calculate how infection rate changes over course of epidemic
        #chance for infected person to infect other over tick(hour)
        infection_per_tick = self.contagionParams.R_0 / (self.contagionParams.life_time * 24.0)
        for person in self.people:
            if person.infected:
                # if chance is less than or equal to infection per tick chance try to infect
                if choices([True, False], [infection_per_tick, 1-infection_per_tick])[0]:
                    # print("infecting!!!")
                    contact = False
                    while (contact == False):
                        #attempt to infect random person from the list, if they are
                        contact = random.choice(self.people).infect()
        return
    
    def has_infected_person(self):
        """
        self, None -> bool
        This function has the primary purpose of determining if 
        a city has a infected individual in its population.
        """
        has_inf_person = True
        no_inf_person = False
        #iterate through the list of people in that city
        for person in self.people:
            if person.infected: 
                return has_inf_person
        return no_inf_person

    def tick(self):
        """
        self, None -> bool
        This is the update method for the vessel class. The infection logic
        for the people objects inside the vessel is done in this method. False
        is returned while the vessel is traveling and True is returned when the
        vessel is stationary.
        """
        #pass the infection
        self.__passInfection()
        self.tick_inf_person()
        
        # add to the total distance traveled.
        self.distanceTraveled += self.vesselParam.airspeed * 1 # each tick is an hour.

        # check if the vessel has traveled the minimun distance to destination.
        if(self.distanceTraveled >= self.distance):
            # send passengers to destination city.
            self.destinationCity.receive_journey(self.people)
            # done traveling.
            self.active = False
            return True
        
        # still traveling.
        return False

    def tick_inf_person(self):
        """
        self, None -> None
        This function has the purpose of ticking each infected person on the vessel
        to move the contagion lifetime in their host.
        """
        (person.tick() for person in self.people if person.infected)
        return 