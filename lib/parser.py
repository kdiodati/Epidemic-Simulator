"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This file is in charge of parsing configuration files for the program to simulate organic life on earth to be
affected by a contagion. The parser class is in charge of parsing 2 configuration files:
    1) cities 
    2) planes
"""
import os
from collections import namedtuple

class parser:
    """
    This class is in charge of obtaining a configuration file and parsing it to obtain
    all city information that will be mapped in the U.I.
    """
    def __init__(self):
        """
        self, None -> None
        This function serves to initialize the parser module. This module will keep track of cities and planes
        by storing them in lists.
        """
        self.cities_list = list() #create a list for all the cities to be placed
        self.planes_list = list() #list of all planes from the configuration file
    
    def open_and_read_city_file(self, file):
        """
        str (file) -> None
        This function is in charge of iterating through a configuration file
        and parsing each line to find all the data for each city to be initialized.
        This function is looking to find contagion growth information as well as all the cities
        being placed in the epidemic simulator.
        The first line of this city input file will be the contagion in the format <R_0>/t<life_time>/t<death_rate>
        the remaining lines will be city information in the format <city_name>/t<lat>/t<lon>/t<pop>.
        """
        with open(file, "r") as configfile: #open the file
            line_count = 1 #init a variable to keep track of the line number being parsed
            #collect contagion information
            lines = configfile.readlines() #put all the lines into a list
            if(len(lines) < 3):
                os.system('cls' if os.name == 'nt' else 'clear')
                raise Exception("ERROR: Configuration File does not have enough cities to create an epidemic simulation. At least two cities must be provided.")
            else:
                # Pop the first line from the list because it is the column labels.
                lines.pop(0)
                for line in lines:           
                    #get the city information from each line     
                    city = self.get_city_info(line, line_count)
                    if(city != None):
                        self.cities_list.append(city)
                    # try to get all the proper parameters of each line
                    line_count+=1
            #if the cities list is empty raise an error 
            if(len(self.cities_list) == 0):
                raise Exception("ERROR: Plane configuration file is empty.")
        return 

    def open_and_read_plane_file(self, file):
        """
        self, str (file) -> None
        This function is in charge of iterating through a plane configuration file.
        Each line will contain the following information <plane_model>/t<min_dist>/t<max_dist>/t<airspeed>.
        Any error in the configuration file will cause an exception error to report to the user.
        """
        with open(file, "r") as plane_file:
            #set line count for this file
            line_count = 1
            #read all the lines
            lines = plane_file.readlines()
            #if the file is empty
            if(len(lines) == 0):
                os.system('cls' if os.name == 'nt' else 'clear')
                raise Exception("ERROR: Plane configuration file is empty.")
            else:
                # Pop the first line from the list because it is the column labels.
                lines.pop(0)
                for line in lines: #iterate through each line
                    plane = self.get_plane_info(line, line_count) #obtain plane info
                    #if the plane is not None then add it to the list of planes
                    if(plane != None):
                        self.planes_list.append(plane) #add plane info to attribute list
                    line_count += 1
            #if the list of planes is empty raise error
            if(len(self.planes_list) == 0):
                os.system('cls' if os.name == 'nt' else 'clear')
                raise Exception("ERROR: Plane configuration file is empty.")
        return 

    def get_city_info(self, city_info, line_count):
        """
        self, list(city information) -> namedtuple (city information)
        This function is in charge of collecting city information and placing it into a namedtuple container.
        """
        city = namedtuple('city', 'city_name lat lon pop')  #create a city using the namedtuple data type
        if(city_info == "\n"):
            return None
        city_info = city_info.strip("\n") #strip the new line characer
        city_info = city_info.split("\t") #split the string by tabs
        #check if the city info line is empty or is a \n char
        if(len(city_info) == 1):
            if(len(city_info[0]) == 0):
                return None
        elif(len(city_info) < 4 or len(city_info) > 4): #check for invalid number of attributes
            os.system('cls' if os.name == 'nt' else 'clear')
            raise Exception("ERROR: City Configuration line {} invalid number of inputs.".format(line_count))
        try:
            #convert the attribute to the needed type
            city.city_name = city_info[0]
            city.lat = float(city_info[1])
            city.lon = float(city_info[2])
            city.pop = abs(int(city_info[3]))
        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            #if an attribute can not be converted, raise attribute error
            raise Exception("TYPE ERROR: Given wrong variable type on line {} in City Configuration File.".format(line_count))
    
        return city

    def get_plane_info(self, plane_info, line_count):
        """
        self, list(plane information), int (line count) -> namedtuple (plane information)
        This function is in charge of collecting plane information and placing it into a namedtuple container.
        """
        #plane container 
        plane = namedtuple('plane', 'model min_flight_dist max_flight_dist airspeed capacity')
        if(plane_info == "\n"):
            return None
        plane_info = plane_info.strip("\n") #strip new line
        plane_info = plane_info.split("\t") #seperate by tabs
        #if the line is empty return None
        if(len(plane_info) == 1):
            if(len(plane_info[0]) == 0):
                return None
        #if the length does not meet the required attributes
        elif(len(plane_info) < 5 or len(plane_info) > 5):
            os.system('cls' if os.name == 'nt' else 'clear')
            raise Exception("ERROR: Plane Configuration line {} invalid number of inputs.".format(line_count))
        try:
            #try to convert all read strings into the proper variablle type
            plane.model = plane_info[0]
            plane.min_flight_dist = abs(int(plane_info[1]))
            plane.max_flight_dist = abs(int(plane_info[2]))
            plane.airspeed = abs(int(plane_info[3]))
            plane.capacity = abs(int(plane_info[4]))
        except:
            #if one attribute is not of the right type, raise an error accordingly
            os.system('cls' if os.name == 'nt' else 'clear')
            raise Exception("TYPE ERROR: Given wrong variable type on line {} in Plane Configuration File.".format(line_count))
        return plane
