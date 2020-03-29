"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This module has the role of creating person objects for the simulation to work with.
"""

import math
from random import choices

import lib.city
import lib.statistics
import lib.vessel
import lib.parser

#strings for tick function to remove hard coded strings in the function itself
DEAD = "dead"
RECOVERED = "recovered"
NO_CHANGE = "no change"

class person:

    def __init__(self, contagionParams):
        """
        self, namedTuple -> None
        This initializes the person class. Each person has flags for being
        infected, dead and immune to the contagion. They are also given the contagion infection 
        parameters from the argparser module. Finally, a person has a attribute called liferemaining. This represents the
        amount of time the disease has been present in the host.
        """
        self.r0 = contagionParams.R_0 # variable of infection rate between people
        self.life = contagionParams.life_time # average lifetime someone will have virus
        self.life_in_hours = math.floor(self.life * 24)
        self.death = contagionParams.death_rate # average death rate of virus (%) inverted
        self.death_in_hours = 1-((1-self.death)**float(1/self.life_in_hours))

        # flags to keep track of person status. They can be infected, dead, or immune.
        self.infected = False
        self.dead = False
        self.immune = False

        self.life_remaining_in_hours = -1

    def __kill(self):
        """
        self, None -> None
        This is an internal method. It updates the state of the
        person to dead.
        """
        # change state of person to dead
        self.infected = False
        self.dead = True
        return

    def tick(self):
        """
        self, None -> str(one of the global strings at the top of the module)
        The update function for a person object. It will return any change of status
        for the person. This could be death, recovering, or no change.
        """
        # Check if dies
        if(self.infected):
            # person is infected to decide if they should die.
            should_idie = choices([True, False], [self.death_in_hours, 1-self.death_in_hours])[0]
            if should_idie:
                # if they die, call to kill method to update state then return new state.
                self.__kill()
                return DEAD
            else:
                # they don't die so update remaining life hours.
                self.life_remaining_in_hours -= 1
                if self.life_remaining_in_hours <= 0:
                    # virus is gone so update to immune and return new state.
                    self.infected = False
                    self.immune = True
                    return RECOVERED

        # person is not infected so nothing happens.
        return NO_CHANGE

    def infect(self):
        """
        self, None -> bool
        This function is called by a city instance which is using a person to infect others. This functions
        determines if they can be interacted with by other infected/non-infected individuals. If a person is dead
        they are not able to interact with others. If a person is immune they can still spread the disease to
        others that they come into contact with. 
        """
        cant_interact = False
        can_interact = True
        # if the person is dead they can not interact with others 
        if(self.dead):
            return cant_interact
        # if they are immune they can interact with others but cannot get the virus
        # regardless of interactions they may have.
        # if they are infected they can interact and spread the contagion.
        if(self.infected or self.immune):
            return can_interact
        # set state to infected because they are infected.
        # update remaining life in hours.
        self.life_remaining_in_hours = self.life_in_hours
        self.infected = can_interact

        return can_interact

